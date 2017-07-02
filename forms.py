#-*- coding: UTF-8 -*-
from __future__ import unicode_literals
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField
from wtforms.validators import DataRequired, Length

class DanmuForm(FlaskForm):
    content = StringField('请随便吐槽', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('吐')
