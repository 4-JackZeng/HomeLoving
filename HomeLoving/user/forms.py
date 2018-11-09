from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from user.models import User


class UserRegisterForm(FlaskForm):
    mobile = StringField('手机号', validators=[DataRequired()])
    imagecode=StringField('图片验证码',validators=[DataRequired()])
    password = StringField('密码', validators=[DataRequired()])
    password2 = StringField('确认密码', validators=[DataRequired(), EqualTo('password', '二次密码填写不一致')])
    submit = SubmitField('立即注册')


    def validate_mobile(self, field):
        mobile = User.query.filter(User.phone==field.data).first()
        if mobile:
            raise ValidationError('该手机号已注册')
        if len(field.data)>11:
            raise ValidationError('手机号长度为11位数字，请重新输入')
