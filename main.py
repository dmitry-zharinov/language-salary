import os

from dotenv import load_dotenv
from terminaltables import SingleTable

from fetch_hh import get_vacancies_hh, predict_rub_salary_for_hh
from fetch_superjob import (get_vacancies_superjob,
                            predict_rub_salary_for_superjob)


def fetch_language_info(language,
                        get_vacancies_func,
                        predict_rub_salary_func,
                        **params):
    """Получить среднюю зарплату по вакансиям по языку"""
    vacancies, vacancies_found = get_vacancies_func(language, **params)
    salaries = list(
        filter(
            None,
            [predict_rub_salary_func(v) for v in vacancies]
        )
    )
    if len(salaries) > 0:
        language_info = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': len(salaries),
            'average_salary': int(sum(salaries) / len(salaries))
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

    languages = ['Python', 'Java', 'Javascript', 'ABAP']
    language_salary_hh = {
        language: fetch_language_info(
            language,
            get_vacancies_hh,
            predict_rub_salary_for_hh)
        for language in languages
    }
    language_salary_superjob = {
        language: fetch_language_info(
            language,
            get_vacancies_superjob,
            predict_rub_salary_for_superjob,
            key=key)
        for language in languages
    }
    print(get_data_as_table(language_salary_hh, 'HeadHunter Moscow'))
    print()
    print(get_data_as_table(language_salary_superjob, 'SuperJob Moscow'))
    print()


if __name__ == '__main__':
    main()
