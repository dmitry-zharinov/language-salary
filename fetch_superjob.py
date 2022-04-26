import requests


def get_vacancies_superjob(text, **params):
    """Получить вакансии Superjob по запросу"""
    url = 'https://api.superjob.ru/2.0/vacancies'
    headers = {
        'X-Api-App-Id': params['key'],
    }
    params = {
        'town': 4,
        'keyword': text,
    }
    vacancies = []
    page = 0
    more = True
    while more:
        params['page'] = page
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        vacancies_from_api = response.json()

        more = vacancies_from_api['more']
        page += 1

        vacancies_found = vacancies_from_api['total']
        for vacancy in vacancies_from_api['objects']:
            vacancies.append(vacancy)

    return (vacancies, vacancies_found)
