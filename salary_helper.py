from terminaltables import DoubleTable


def seach_salary_in_vacancy_hh(vacancy):
    if not vacancy['salary']:
        return
    if vacancy['salary']['currency'] != 'RUR':
        return
    return calculate_salary(salary_from=vacancy['salary']['from'],
                            salary_to=vacancy['salary']['to'])


def seach_salary_in_vacancy_sj(vacancy):
    salary_from = vacancy['payment_from']
    salary_to = vacancy['payment_to']
    average_salary = calculate_salary(salary_from, salary_to)
    if vacancy['currency'] != 'rub':
        return
    elif average_salary != 0:
        return average_salary
    return


def calculate_salary(salary_from=None, salary_to=None):
    if salary_from and salary_to:
        average_salary = (salary_from + salary_to) / 2
    elif not salary_to or salary_to == 0:
        average_salary = salary_from * 1.2
    elif not salary_from or salary_from == 0:
        average_salary = salary_to * 0.8
    else:
        return None
    return average_salary


def predict_rub_salary(vacancies, seach_salary_in_vacancy):
    vacancies_processed = 0
    average_salaries = 0
    for vacancy in vacancies:
        average_salary = seach_salary_in_vacancy(vacancy)
        if average_salary:
            vacancies_processed += 1
            average_salaries += average_salary
    if vacancies_processed == 0:
        average_salaries = int(average_salaries / 1)
    else:
        average_salaries = int(average_salaries / vacancies_processed)
    return vacancies_processed, average_salaries


def create_languages_rating(programming_languages, process_pages_request):
    programming_languages_rating = {}
    for language in programming_languages:
        full_vacancies_processed, full_average_salary, vacancies_found = process_pages_request(page=0,
                                                                                               language=language)
        programming_languages_rating[language] = {"vacancies_found": vacancies_found,
                                                  "vacancies_processed": full_vacancies_processed,
                                                  "average_salary": int(full_average_salary)
                                                  }
    return programming_languages_rating


def create_table_from_dictionary(dictionary, title):
    column_names = ['Язык программирования', 'Средняя зарплата', 'Вакансий найдено', 'Вакансий обработано']
    final_table = []
    final_table.append(column_names)
    for key, value in dictionary.items():
        rows = [key,
                value['average_salary'],
                value['vacancies_found'],
                value['vacancies_processed']
                ]

        final_table.append(rows)

    table = DoubleTable(final_table, title=title)
    return table.table
