from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id, LETTERS, URL

LETTERS_COUNT = 16


@app.route('/api/id/', methods=['POST'])
def get_short_link():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if 'custom_id' not in data:
        short = get_unique_short_id()
    elif data['custom_id'] == '' or data['custom_id'] is None:
        short = get_unique_short_id()
    else:
        short = data['custom_id']
        for letter in short:
            if letter not in LETTERS:
                raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if len(short) > LETTERS_COUNT:
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if URLMap.query.filter_by(short=short).first() is not None:
            raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
    urlmap = URLMap(
        original=data['url'],
        short=short
    )
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(
        url=urlmap.original,
        short_link=f'{URL + urlmap.short}'
    ), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/')
def redirect_to_original_link(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if link is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': link.original}), HTTPStatus.OK
