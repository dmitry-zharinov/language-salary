import requests
import os


def get_vacancies_superjob(text):
    """Получить вакансии Superjob по запросу"""
    key = os.environ['SUPERJOB_KEY']

    url = 'https://api.superjob.ru/2.0/vacancies'
    headers = {
        'X-Api-App-Id': key,
    }
    params = {
        'town': 4,
        'keyword': text,
    }
    vacancies = []
    page = 0
    more = True
    while more is True:
        params['page'] = page
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        more = response.json()['more']
        page += 1

        vacancies_found = response.json()['total']
        for vacancy in response.json()['objects']:
            vacancies.append(vacancy)

    return (vacancies, vacancies_found)


def predict_rub_salary_for_superjob(vacancy):
    """Получить ожидаемую зарплату по вакансии Superjob"""
    try:
        if vacancy['currency'] == 'rub':
            salary_from = vacancy['payment_from']
            salary_to = vacancy['payment_to']
            if salary_from == 0:
                predicted_salary = salary_to * 0.8
            elif salary_to == 0:
                predicted_salary = salary_from * 1.2
            else:
                predicted_salary = (salary_to + salary_from) / 2
        else:
            return None
    except TypeError:
        return None
    return predicted_salary
