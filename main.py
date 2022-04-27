import os
import json

from dotenv import load_dotenv
from terminaltables import SingleTable

from fetch_hh import get_vacancies_hh
from fetch_superjob import get_vacancies_superjob


def predict_salary(salary_from, salary_to):
    """Получить ожидаемую зарплату"""
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8


def fetch_language_info(language,
                        get_vacancies_func,
                        **params):
    """Получить среднюю зарплату по вакансиям по языку"""
    vacancies, vacancies_found = get_vacancies_func(language, **params)
    salaries = []
    for vacancy in vacancies:
        if vacancy.get('currency') == 'rub':
            salaries.append(
                predict_salary(
                    vacancy['payment_from'],
                    vacancy['payment_to']
                )
            )
        elif vacancy['salary'].get('currency') == 'RUR':
            salaries.append(
                predict_salary(
                    vacancy['salary']['from'],
                    vacancy['salary']['to']
                )
            )
    result_salaries = list(filter(None, salaries))
    salaries_found = len(result_salaries)
    if salaries_found > 0:
        language_info = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': salaries_found,
            'average_salary': int(sum(result_salaries) / salaries_found)
        }
        return language_info


def get_data_as_table(language_salary, title):
    """Получить данные в табличном виде"""
    table_header = [
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата',
    ]
    table_data = [table_header]

    for language_name, language_data in language_salary.items():
        row = []
        row.append(language_name)
        for language_data_item in language_data.items():
            row.append(language_data_item[1])
        table_data.append(row)

    table_instance = SingleTable(table_data, title)
    table_instance.justify_columns[2] = 'right'
    return table_instance.table


def main():
    load_dotenv()
    key = os.environ['SUPERJOB_KEY']
    with open('config.json') as config_file:
        config = json.load(config_file)

    languages = config['languages']
    language_salary_hh = {
        language: fetch_language_info(
            language,
            get_vacancies_hh)
        for language in languages
    }
    language_salary_superjob = {
        language: fetch_language_info(
            language,
            get_vacancies_superjob,
            key=key)
        for language in languages
    }
    print(get_data_as_table(language_salary_hh, 'HeadHunter Moscow'))
    print()
    print(get_data_as_table(language_salary_superjob, 'SuperJob Moscow'))
    print()


if __name__ == '__main__':
    main()
