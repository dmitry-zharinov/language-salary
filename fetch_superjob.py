import requests


def get_vacancies_superjob(text, key):
    """Получить вакансии Superjob по запросу"""
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


'''
def predict_rub_salary_for_superjob(vacancy):
    return predicted_salary

'''
