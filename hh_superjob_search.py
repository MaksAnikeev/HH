import os

import requests
from dotenv import load_dotenv

from salary_helper import (create_languages_rating,
                           create_table_from_dictionary,
                           predict_rub_salary,
                           seach_salary_in_vacancy_hh,
                           seach_salary_in_vacancy_sj)


def process_hh_pages_request(page, language):
    full_vacancies_processed = 0
    full_average_salary = 0
    while True:
        payload = {'text': f'Программист {language}',
                   'per_page': 100,  # колличество вакансий на странице
                   'page': page,  # с какой страницы начать обработку (по умолчанию с 0)
                   'area': 1,  # область поиска Москва (для СПБ 2) https://api.hh.ru/areas
                   'period': 20,  # вакансии за последние 20 дней
                   'specialization': 1  # профессия ИТ
                   }
        response = requests.get(hh_url,
                                headers=hh_headers,
                                params=payload)
        response.raise_for_status()
        vacancies_page = response.json()
        pages_quantity = vacancies_page['pages']
        page += 1
        processed, salaries = predict_rub_salary(vacancies=vacancies_page['items'],
                                                 seach_salary_in_vacancy=seach_salary_in_vacancy_hh)
        full_vacancies_processed += processed
        full_average_salary += salaries
        if page >= pages_quantity:
            break
    vacancies_found = vacancies_page['found']
    full_average_salary = full_average_salary / pages_quantity
    return full_vacancies_processed, \
           full_average_salary, \
           vacancies_found


def process_sj_pages_request(page, language):
    full_vacancies_processed = 0
    full_average_salary = 0
    while True:
        payload = {'keyword': f'Программист {language}',
                   'count': 10,  # колличество вакансий на странице
                   'page': page,  # с какой страницы начать обработку (по умолчанию с 0)
                   'town': 4,  # область поиска Москва (для СПБ 14) 	https://api.superjob.ru/2.0/towns/
                   'period': 0,  # вакансии за весь доступный период (1 - за день, 7 за неделю)
                   }
        response = requests.get(sj_url, headers=sj_headers, params=payload)
        response.raise_for_status()
        vacancies_page = response.json()
        if vacancies_page['total'] // payload['count'] > 0:
            pages_quantity = vacancies_page['total'] // payload['count']
        else:
            pages_quantity = 1
        page += 1
        processed, salaries = predict_rub_salary(vacancies=vacancies_page['objects'],
                                                 seach_salary_in_vacancy=seach_salary_in_vacancy_sj)
        full_vacancies_processed += processed
        full_average_salary += salaries
        if page >= pages_quantity:
            break
    vacancies_found = vacancies_page['total']
    full_average_salary = full_average_salary / pages_quantity
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
                                           process_pages_request=process_sj_pages_request)
    print(create_table_from_dictionary(dictionary=sj_vacancies,
                                       title='SuperJob Moscow'))

    hh_vacancies = create_languages_rating(programming_languages=programming_languages,
                                           process_pages_request=process_hh_pages_request)
    print(create_table_from_dictionary(dictionary=hh_vacancies,
                                       title='HeadHunter Moscow'))
