from string import ascii_lowercase, ascii_uppercase, digits

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id, URL


@app.route('/api/id/', methods=['POST'])
def get_short_link():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if 'custom_id' in data:
        short = data['custom_id']
        if short == '' or short is None:
            short = get_unique_short_id()
        else:
            for letter in short:
                if letter not in ascii_lowercase + ascii_uppercase + digits:
                    raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
            if len(short) > 16:
                raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
            if URLMap.query.filter_by(short=short).first() is not None:
                raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
    else:
        short = get_unique_short_id()
    urlmap = URLMap(
        original=data['url'],
        short=short
    )
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(
        url=urlmap.original,
        short_link=f'{URL + urlmap.short}'
    ), 201


@app.route('/api/id/<string:short_id>/')
def redirect_to_original_link(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if link is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': link.original}), 200
