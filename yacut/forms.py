from string import ascii_lowercase, ascii_uppercase, digits

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, URLField
from wtforms.validators import DataRequired, Length, Optional


class URlMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 256)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(form, field):
        for letter in field.data:
            if letter not in ascii_lowercase + ascii_uppercase + digits:
                raise ValidationError('Указано недопустимое имя для короткой ссылки')
