import os

from dotenv import load_dotenv

from fetch_hh import get_vacancies_hh, predict_rub_salary_for_hh
from fetch_superjob import get_vacancies_superjob


def fetch_language_info(language):
    """Получить среднюю зарплату по вакансиям по языку"""
    vacancies, vacancies_found = get_vacancies_hh(language)
    # salaries = [predict_rub_salary_for_hh(v) for v in vacancies]
    salaries = list(
        filter(
            None,
            [predict_rub_salary_for_hh(v) for v in vacancies]
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
    superjob_key = os.environ['SUPERJOB_KEY']
    get_vacancies_superjob('Python', superjob_key)
    '''
    languages = ['Python', 'Java', 'Javascript', 'ABAP']
    languages_found = {
        language: fetch_language_info(language)
        for language in languages
    }
    print(languages_found)
    '''


if __name__ == '__main__':
    main()
