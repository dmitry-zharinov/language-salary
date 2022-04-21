from dotenv import load_dotenv
import os

from fetch_hh import get_vacancies_hh, predict_rub_salary_for_hh
from fetch_superjob import get_vacancies_superjob, \
                        predict_rub_salary_for_superjob


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


def main():
    load_dotenv()
    key = os.environ['SUPERJOB_KEY']

    '''
    vacancies, vacancies_found = get_vacancies_superjob('Python', superjob_key)
    salaries_ = [predict_rub_salary_for_superjob(v) for v in vacancies]
    salaries = list(filter(None, salaries))
    print(salaries)
    '''

    languages = ['Python', 'Java', 'Javascript', 'ABAP']
    languages_found_hh = {
        language: fetch_language_info(
            language,
            get_vacancies_hh,
            predict_rub_salary_for_hh)
        for language in languages
    }
    languages_found_superjob = {
        language: fetch_language_info(
            language,
            get_vacancies_superjob,
            predict_rub_salary_for_superjob,
            key=key)
        for language in languages
    }
    print(languages_found_hh)
    print(languages_found_superjob)


if __name__ == '__main__':
    main()
