import requests
import pprint

def get_vacancies(text):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'area': 1,
        'text': text
    }
    response = requests.get(url, params)
    response.raise_for_status()
    return response.json()


def predict_rub_salary(vacancy):
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


def fetch_language_info(language):
    vacancies = get_vacancies(language)
    salaries_subq = [predict_rub_salary(v) for v in vacancies['items']]
    salaries = list(filter(None, salaries_subq))
    if len(salaries) > 0:
        language_info = {
            'vacancies_found': vacancies['found'],
            'vacancies_processed': len(salaries),
            'average_salary': int(sum(salaries) / len(salaries))
        }
        return language_info


def main():
    languages = ['Python', 'Java', 'Javascript', 'ABAP']
    languages_found = {
        language: fetch_language_info(language)
        for language in languages
    }
    pprint(languages_found)
    # for vacancy in get_vacancies('Python')['items']:
    #    print(predict_rub_salary(vacancy))


if __name__ == '__main__':
    main()
