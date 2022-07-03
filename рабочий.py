# получение словаря специализаций для поиска индекса нужной специализации в запросе
# url = 'https://api.hh.ru//specializations'
# headers = {'User-Agent': 'api-test-agent'}
#
# response = requests.get(url, headers=headers)
# response.raise_for_status()
# pprint(response.json())

# получение словаря регионов для поиска индекса нужного региона в запросе
# url = 'https://api.hh.ru//areas'
# headers = {'User-Agent': 'api-test-agent'}
#
# response = requests.get(url, headers=headers)
# response.raise_for_status()
# pprint(response.json())

# Вакансии программистов python в Москве с указанием адреса
# url = 'https://api.hh.ru/vacancies'
# payload = {'text': 'python',
#            'per_page': 100,
#            'area': 1,
#            'period': 20
#            }
#
# headers = {'User-Agent': 'api-test-agent'}
#
# response = requests.get(url, headers=headers, params=payload)
# response.raise_for_status()
# pprint(response.json())
# with open('HH.json', 'w', encoding='utf-8') as my_file:
#     json.dump(response.json(), my_file)
# print(response.json()['found'])
# for i in response.json()['items']:
#     print(i['name'])
#     if i['address']:
#         print('   ', i['address']['city'], i['address']['street'])
#     else:
#         continue

# Рейтинг языков программирования по Москве
# programming_languages = ['JavaScript', 'Java','Python', 'Ruby', 'PHP', 'C++', 'CSS', 'C#', 'Go', 'Shell']
# url = 'https://api.hh.ru/vacancies'
# headers = {'User-Agent': 'api-test-agent'}
# programming_languages_rating = {}
# for language in programming_languages:
#     payload = {'text': f'Программист {language}',
#                # 'per_page': 100,
#                'area': 1,
#                'period': 20,
#                'specialization': 1
#                }
#     response = requests.get(url, headers=headers, params=payload)
#     response.raise_for_status()
#     programming_languages_rating[language] = response.json()['found']
#
# sorted_tuples = dict(sorted(programming_languages_rating.items(), reverse = True,  key=lambda item: item[1]))
# for i,j in sorted_tuples.items():
#     print(i, j)

# Зарплаты программистов Python в Москве
#


# def seach_salary_in_vacancy(vacancy):
#     if vacancy['salary']:
#         if vacancy['salary']['currency'] == 'RUR':
#             salary_from = vacancy['salary']['from']
#             salary_to = vacancy['salary']['to']
#             return calculat_salary(salary_from, salary_to)
#         else:
#             return None
#     else:
#         return None
#
# def predict_rub_salary(vacancies):
#     vacancies_processed = 0
#     average_salaries = 0
#     for vacancy in vacancies:
#         if seach_salary_in_vacancy(vacancy):
#             vacancies_processed +=1
#             average_salary = seach_salary_in_vacancy(vacancy)
#             average_salaries += average_salary
#     average_salaries = int(average_salaries/vacancies_processed)
#     return vacancies_processed, average_salaries
#
# def process_pages_request(page, language, pages=1):
#     full_vacancies_processed = 0
#     full_average_salaries = 0
#     while page < pages:
#         payload = {'text': f'Программист {language}',
#                    'per_page': 100,
#                    'page': page,
#                    'area': 1,
#                    'period': 10,
#                    'specialization': 1
#                    }
#         response = requests.get(url, headers=headers, params=payload)
#         response.raise_for_status()
#         pages = response.json()['pages']
#         page += 1
#         processed, salaries = predict_rub_salary(vacancies=response.json()['items'])
#         full_vacancies_processed += processed
#         full_average_salaries += salaries
#     vacancies_found = response.json()['found']
#     full_average_salaries = full_average_salaries/pages
#     return full_vacancies_processed,\
#            full_average_salaries,\
#            vacancies_found
#
#
# programming_languages = ['JavaScript', 'Java','Python', 'Ruby', 'PHP', 'C++', 'CSS', 'C#', 'Go', 'Shell']
# programming_languages_rating = {}
#
# url = 'https://api.hh.ru/vacancies'
# headers = {'User-Agent': 'api-test-agent'}
#
#
# for language in programming_languages:
#     programming_languages_rating[language] = {}
#     full_vacancies_processed, full_average_salaries, vacancies_found = process_pages_request(page=0, language=language)
#     programming_languages_rating[language]["vacancies_found"] = vacancies_found
#     programming_languages_rating[language]["vacancies_processed"] = full_vacancies_processed
#     programming_languages_rating[language]["average_salary"] = int(full_average_salaries)
#
# pprint(programming_languages_rating)

# import requests
# import json
# from pprint import pprint
# from salary_helper import predict_rub_salary
# from salary_helper import seach_salary_in_vacancy_sj
# from salary_helper import create_languages_rating
#
#
# def process_pages_request(page, language, pages=1):
#     full_vacancies_processed = 0
#     full_average_salaries = 0
#     while page < pages:
#         payload = {'keyword': f'Программист {language}',
#                    'count': 20,
#                    'page': page,
#                    'town': 4,
#                    'period': 20,
#                    }
#         response = requests.get(url, headers=headers, params=payload)
#         response.raise_for_status()
#         if response.json()['total']//payload['count']>0:
#             pages = response.json()['total']//payload['count']
#         else:
#             pages = 1
#         page += 1
#         processed, salaries = predict_rub_salary(vacancies=response.json()['objects'],
#                                                  function=seach_salary_in_vacancy_sj)
#         full_vacancies_processed += processed
#         full_average_salaries += salaries
#     vacancies_found = response.json()['total']
#     full_average_salaries = full_average_salaries/pages
#     return full_vacancies_processed,\
#            full_average_salaries,\
#            vacancies_found
#
# # pprint(response.json()['objects'])
# # pprint(predict_rub_salary(vacancies=response.json()['objects'],
# #                       function=seach_salary_in_vacancy_sj))
#
# programming_languages = ['JavaScript', 'Java','Python', 'Ruby', 'PHP', 'C++', 'CSS', 'C#', 'Go', 'Shell']
#
# secret_key = 'v3.r.11760168.7e0f9a0d27ae75a9c6c8aabc7174f0a0c2f6799c.ffaef2e4e79804e67546216e64c1c2cdabc1909a'
# url = 'https://api.superjob.ru/2.0/vacancies/'
# headers = {'X-Api-App-Id': secret_key}
#
# pprint(create_languages_rating(programming_languages=programming_languages,
#                             function=process_pages_request))

from pprint import pprint
from terminaltables import AsciiTable, DoubleTable

list = {'JavaScript': {'vacancies_found': 86, 'vacancies_processed': 61, 'average_salary': 218666},
        'Java': {'vacancies_found': 33, 'vacancies_processed': 21, 'average_salary': 254809},
        'Python': {'vacancies_found': 59, 'vacancies_processed': 37, 'average_salary': 206939},
        'Ruby': {'vacancies_found': 6, 'vacancies_processed': 4, 'average_salary': 233500},
        'PHP': {'vacancies_found': 54, 'vacancies_processed': 38, 'average_salary': 150868},
        'C++': {'vacancies_found': 30, 'vacancies_processed': 24, 'average_salary': 200240},
        'CSS': {'vacancies_found': 38, 'vacancies_processed': 25, 'average_salary': 154778},
        'C#': {'vacancies_found': 17, 'vacancies_processed': 9, 'average_salary': 175555},
        'Go': {'vacancies_found': 17, 'vacancies_processed': 9, 'average_salary': 329333},
        'Shell': {'vacancies_found': 5, 'vacancies_processed': 4, 'average_salary': 200500}}

list2 = [['language', 'average_salary', 'vacancies_found', 'vacancies_processed']]
for key, value in list.items():
    list3 = []
    list3.append(key)
    list3.append(value['average_salary'])
    list3.append(value['vacancies_found'])
    list3.append(value['vacancies_processed'])
    list2.append(list3)

table = AsciiTable(list2, title='Moscow')
table2 = DoubleTable(list2, title='SPB')
print(table.table)
print(table2.table)
