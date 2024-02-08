from string import ascii_lowercase, ascii_uppercase, digits
from random import choices

from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import URlMapForm
from .models import URLMap

URL = 'http://localhost/'


def get_unique_short_id():
    return ''.join(choices(
        ascii_lowercase + ascii_uppercase + digits, k=6
    ))


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URlMapForm()
    if form.validate_on_submit():
        if form.custom_id.data:
            custom_id = form.custom_id.data
            if URLMap.query.filter_by(short=custom_id).first():
                flash('Предложенный вариант короткой ссылки уже существует.', 'error')
                return render_template('get_short_link.html', form=form)
        else:
            custom_id = get_unique_short_id()
        urlmap = URLMap(
            original=form.original_link.data,
            short=custom_id
        )
        db.session.add(urlmap)
        db.session.commit()
        flash(f'{URL + custom_id}', 'short-link')
    return render_template('get_short_link.html', form=form)


@app.route('/<string:short>')
def redirect_view(short):
    link = URLMap.query.filter_by(short=short).first()
    if link is None:
        abort(404)
    return redirect(link.original)
