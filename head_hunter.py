import requests

from salary_helper import (create_table_from_dict,
                           create_languages_rating,
                           predict_rub_salary,
                           seach_salary_in_vacancy_hh)


def process_pages_request_hh(page, language, pages=1):
    full_vacancies_processed = 0
    full_average_salaries = 0
    while page < pages:
        payload = {'text': f'Программист {language}',
                   'per_page': 100,
                   'page': page,
                   'area': 1,
                   'period': 20,
                   'specialization': 1
                   }
        response = requests.get(url,
                                headers=headers,
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


if __name__ == '__main__':
    programming_languages_rating = {}
    programming_languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'CSS', 'C#', 'Go', 'Shell']

    url = 'https://api.hh.ru/vacancies'
    headers = {'User-Agent': 'api-test-agent'}

    vacancy_dict = create_languages_rating(programming_languages=programming_languages,
                                           function=process_pages_request_hh)
    create_table_from_dict(dict=vacancy_dict,
                           title='HeadHunter Moscow')
