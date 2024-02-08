# YACUT

## Описание:

<h4>YaCut - это сайт, а также api, предоставляющий возможность укорачивания ссылок.

Он позволит использовать более читаемые и компактные ссылки, такие как
http://localhost/cats и http://localhost/GU3w7l вместо привычных длинных [https://www.yandex.ru/images/search?from=tabbar&text=%D0%BA%D0%BE%D1%88%D0%BA%D0%B8](https://www.yandex.ru/images/search?from=tabbar&text=%D0%BA%D0%BE%D1%88%D0%BA%D0%B8)
</h4>

Доступны следующие функции: создание связи между укороченным вариантом и оригинальной ссылкой, получение полной ссылки по короткому id.

---

## Как скачать и запустить проект:
1. **Клонировать репозиторий и перейти в папку с ним:**

```bash
git clone git@github.com:dasha2000vas/yacut.git
cd yacut
```

2. **Создать и активировать виртуальное окружение:**

```bash
python -m venv venv
source venv/Scripts/activate
```

3. **Установить зависимости из файла requirements.txt:**

```bash
pip install -r requirements.txt
```

4. **С помощью интерактивной оболочки Flask создать базу данных и таблицу URLmap:**

```bash
flask shell 
>>> from yacut import db
>>> db.create_all() 
```

5. **Запустить проект на локальном сервере:**

```bash
flask run
```

---

## Примеры запросов:


1. **Эндпоинт: http://localhost/api/id/<br>Метод запроса: POST**

    При передаче следующих данных:

    * "url": "string" (required),
    * "custom_id": "string"(optional)

    Вы получите ответ о создании связи между url и custom_id и короткую ссылку, предоставляющую доступ к оригинальной:

    * "url": "string",
    * "short_link": "string"

    >*Если не указать поле custom_id в запросе, то для него будет сгенерирована строка из шести случайных элементов. В качестве элементов будут использованы заглавные и строчные латинские буквы и цифры от 0 до 9.*

<br>

2. **Эндпоинт: http://localhost/api/id/{short_id}/<br>Метод запроса: GET**

   При передаче следующего поля в параметрах запроса:

   * "short_id ": "string" (required)
  
   Вам в ответе будет возвращена полная оригинальная ссылка:

   * "url": "string"

---

## Технический стек:
* flask2.0.2
* flask-sqlalchemy2.5.1
* flask-wtf1.0.0
* flask-migrate3.1.0
* python-dotenv0.19.2
* sqlalchemy1.4.29
* werkzeug2.0.2

---

## Автор:
Василевская Дарья
