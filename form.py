#这个是表单的类
from flask_ckeditor import CKEditorField
from flask_wtf import  FlaskForm
from flask_wtf.file import FileRequired, FileField, FileAllowed

from wtforms import  StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length
class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired(),Length(3,128)])
    remeber = BooleanField('Remember')
    submit = SubmitField('Log in')


class UploadForm (FlaskForm):  #这个是文件上传表单
    photo = FileField("Upload Image",validators=[FileRequired(),FileAllowed(['jpg','jpeg','png','gif'])])
    submit = SubmitField()  #提交按钮也要的表单


class RichTextForm(FlaskForm):  #flask-ckeditor的富文本框的东西
    title = StringField('Title',validators=[DataRequired(),Length(1,50)])
    body = CKEditorField('Body',validators=[DataRequired()])
    submit=SubmitField("发布！")