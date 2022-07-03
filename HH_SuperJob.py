import os

import requests
from dotenv import load_dotenv

from salary_helper import (create_languages_rating,
                           create_table_from_dict,
                           predict_rub_salary,
                           seach_salary_in_vacancy_hh,
                           seach_salary_in_vacancy_sj)

def process_pages_request_hh(page, language, pages=1):
    full_vacancies_processed = 0
    full_average_salaries = 0
    while page < pages:
        payload = {'text': f'Программист {language}',
                   'per_page': 100,
                   'page': page,
                   'area': 1,
                   'period': 5,
                   'specialization': 1
                   }
        response = requests.get(url_hh,
                                headers=headers_hh,
                                params=payload)
        response.raise_for_status()
        pages = response.json()['pages']
        page += 1
        processed, salaries = predict_rub_salary(vacancies=response.json()['items'],
                                                 function=seach_salary_in_vacancy_hh)
        full_vacancies_processed += processed
        full_average_salaries += salaries
    vacancies_found = response.json()['found']
    full_average_salaries = full_average_salaries / pages
    return full_vacancies_processed, \
           full_average_salaries, \
           vacancies_found


def process_pages_request_sj(page, language, pages=1):
    full_vacancies_processed = 0
    full_average_salaries = 0
    while page < pages:
        payload = {'keyword': f'Программист {language}',
                   'count': 10,
                   'page': page,
                   'town': 4,
                   'period': 30,
                   }
        response = requests.get(url_sj, headers=headers_sj, params=payload)
        response.raise_for_status()
        if response.json()['total'] // payload['count'] > 0:
            pages = response.json()['total'] // payload['count']
        else:
            pages = 1
        page += 1
        processed, salaries = predict_rub_salary(vacancies=response.json()['objects'],
                                                 function=seach_salary_in_vacancy_sj)
        full_vacancies_processed += processed
        full_average_salaries += salaries
    vacancies_found = response.json()['total']
    full_average_salaries = full_average_salaries / pages
    return full_vacancies_processed, \
           full_average_salaries, \
           vacancies_found


if __name__ == '__main__':
    programming_languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'CSS', 'C#', 'Go', 'Shell']

    load_dotenv()
    super_job_key = os.environ['SECRET_KEY_SUPER_JOB']
    url_sj = 'https://api.superjob.ru/2.0/vacancies/'
    headers_sj = {'X-Api-App-Id': super_job_key}

    url_hh = 'https://api.hh.ru/vacancies'
    headers_hh = {'User-Agent': 'api-test-agent'}

    vacancy_dict_sj = create_languages_rating(programming_languages=programming_languages,
                                           function=process_pages_request_sj)
    create_table_from_dict(dict=vacancy_dict_sj,
                           title='SuperJob Moscow')

    vacancy_dict_hh = create_languages_rating(programming_languages=programming_languages,
                                           function=process_pages_request_hh)
    create_table_from_dict(dict=vacancy_dict_hh,
                           title='HeadHunter Moscow')
