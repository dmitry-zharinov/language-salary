# Сравниваем вакансии программистов

Консольная утилита, выводящая статистику по вакансям разработчиков с HeadHunter и SuperJob.

### Запуск

1. Предварительно должен быть установлен Python3.
2. Для установки зависимостей:
```
pip install -r requirements.txt
```
3. Для запуска скрипта:
```
$ python main.py
```

### Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `main.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны следущие переменные:
- `SUPERJOB_KEY` — секретный ключ API SuperJob. Для получения, необходимо [зарегистрировать приложение на сайте SuperJob](https://api.superjob.ru/register)

### Конфигурационный файл

Конфигурация приложения хранится в файле `config.json`. 
**Для запуска проекта эти настройки не требуются**, значения уже проставлены по умолчанию.

Доступные параметры:
- `languages` - список языков программирования, по которым будет собрана статистика