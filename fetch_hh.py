import requests


def get_vacancies_hh(text):
    """Получить вакансии HH по запросу"""
    url = 'https://api.hh.ru/vacancies'
    params = {
        'area': 1,
        'text': text,
        'only_with_salary': True,
    }
    # response = requests.get(url, params)
    # response.raise_for_status()
    vacancies = []
    page = 0
    pages_number = 1
    while page < pages_number:
        params['page'] = page
        response = requests.get(url, params)
        response.raise_for_status()

        pages_number = response.json()['pages']
        page += 1

        vacancies_found = response.json()['found']
        for vacancy in response.json()['items']:
            vacancies.append(vacancy)

    return (vacancies, vacancies_found)


def predict_rub_salary_for_hh(vacancy):
    """Получить ожидаемую зарплату по вакансии HH"""
    try:
        salary = vacancy['salary']
        if salary['currency'] == 'RUR':
            if salary['from'] is None:
                predicted_salary = salary['to'] * 0.8
            elif salary['to'] is None:
                predicted_salary = salary['from'] * 1.2
            else:
                predicted_salary = (salary['to'] + salary['from']) / 2
        else:
            return None
    except TypeError:
        return None
    return predicted_salary
