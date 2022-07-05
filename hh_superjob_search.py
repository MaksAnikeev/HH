import os

import requests
from dotenv import load_dotenv

from salary_helper import (create_languages_rating,
                           create_table_from_dict,
                           predict_rub_salary,
                           seach_salary_in_vacancy_hh,
                           seach_salary_in_vacancy_sj)

def process_hh_pages_request(page, language):
    full_vacancies_processed = 0
    full_average_salary = 0
    while True:
        payload = {'text': f'Программист {language}',
                   'per_page': 100,                      # колличество вакансий на странице
                   'page': page,                         # с какой страницы начать обработку (по умолчанию с 0)
                   'area': 1,                            # область поиска Москва (для СПБ 2) https://api.hh.ru/areas
                   'period': 20,                         # вакансии за последние 20 дней
                   'specialization': 1                   # профессия ИТ
                   }
        response = requests.get(hh_url,
                                headers=hh_headers,
                                params=payload)
        response.raise_for_status()
        response_json = response.json()
        quantity_pages = response_json['pages']
        page += 1
        processed, salaries = predict_rub_salary(vacancies=response_json['items'],
                                                 function=seach_salary_in_vacancy_hh)
        full_vacancies_processed += processed
        full_average_salary += salaries
        if page >= quantity_pages:
            break
    vacancies_found = response_json['found']
    full_average_salary = full_average_salary / quantity_pages
    return full_vacancies_processed, \
           full_average_salary, \
           vacancies_found


def process_sj_pages_request(page, language):
    full_vacancies_processed = 0
    full_average_salary = 0
    while True:
        payload = {'keyword': f'Программист {language}',
                   'count': 10,                           # колличество вакансий на странице
                   'page': page,                          # с какой страницы начать обработку (по умолчанию с 0)
                   'town': 4,                             # область поиска Москва (для СПБ 14) 	https://api.superjob.ru/2.0/towns/
                   'period': 0,                           # вакансии за весь доступный период (1 - за день, 7 за неделю)
                   }
        response = requests.get(sj_url, headers=sj_headers, params=payload)
        response.raise_for_status()
        response_json = response.json()
        if response_json['total'] // payload['count'] > 0:
            quantity_pages = response_json['total'] // payload['count']
        else:
            quantity_pages = 1
        page += 1
        processed, salaries = predict_rub_salary(vacancies=response_json['objects'],
                                                 function=seach_salary_in_vacancy_sj)
        full_vacancies_processed += processed
        full_average_salary += salaries
        if page >= quantity_pages:
            break
    vacancies_found = response_json['total']
    full_average_salary = full_average_salary / quantity_pages
    return full_vacancies_processed, \
           full_average_salary, \
           vacancies_found


if __name__ == '__main__':
    programming_languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'CSS', 'C#', 'Go', 'Shell']

    load_dotenv()
    super_job_key = os.environ['SUPER_JOB_SECRET_KEY']
    sj_url = 'https://api.superjob.ru/2.0/vacancies/'
    sj_headers = {'X-Api-App-Id': super_job_key}

    hh_url = 'https://api.hh.ru/vacancies'
    hh_headers = {'User-Agent': 'api-test-agent'}

    sj_vacancies = create_languages_rating(programming_languages=programming_languages,
                                           function=process_sj_pages_request)
    create_table_from_dict(dict=sj_vacancies,
                           title='SuperJob Moscow')

    hh_vacancies = create_languages_rating(programming_languages=programming_languages,
                                           function=process_hh_pages_request)
    create_table_from_dict(dict=hh_vacancies,
                           title='HeadHunter Moscow')
