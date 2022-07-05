from terminaltables import DoubleTable


def seach_salary_in_vacancy_hh(vacancy):
    if vacancy['salary']:
        if vacancy['salary']['currency'] == 'RUR':
            return calculate_salary(salary_from=vacancy['salary']['from'],
                                   salary_to=vacancy['salary']['to'])
        else:
            return None
    else:
        return None


def seach_salary_in_vacancy_sj(vacancy):
    if vacancy['currency'] == 'rub':
        salary_from = vacancy['payment_from']
        salary_to = vacancy['payment_to']
        if calculate_salary(salary_from, salary_to) == 0:
            return None
        else:
            return calculate_salary(salary_from, salary_to)
    else:
        return None


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


def predict_rub_salary(vacancies, function):
    vacancies_processed = 0
    average_salaries = 0
    for vacancy in vacancies:
        if function(vacancy):
            vacancies_processed += 1
            average_salary = function(vacancy)
            average_salaries += average_salary
    if vacancies_processed == 0:
        average_salaries = int(average_salaries / 1)
    else:
        average_salaries = int(average_salaries / vacancies_processed)
    return vacancies_processed, average_salaries


def create_languages_rating(programming_languages, function):
    programming_languages_rating = {}
    for language in programming_languages:
        programming_languages_rating[language] = {}
        full_vacancies_processed, full_average_salary, vacancies_found = function(page=0, language=language)
        programming_languages_rating[language]["vacancies_found"] = vacancies_found
        programming_languages_rating[language]["vacancies_processed"] = full_vacancies_processed
        programming_languages_rating[language]["average_salary"] = int(full_average_salary)
    return programming_languages_rating


def create_table_from_dict(dict, title):
    column_names = ['Язык программирования', 'Средняя зарплата', 'Вакансий найдено', 'Вакансий обработано']
    final_table = []
    final_table.append(column_names)
    for key, value in dict.items():
        strings = []
        strings.append(key)
        strings.append(value['average_salary'])
        strings.append(value['vacancies_found'])
        strings.append(value['vacancies_processed'])
        final_table.append(strings)

    table = DoubleTable(final_table, title=title)
    print(table.table)
