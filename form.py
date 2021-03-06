from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField,RadioField,TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length


class Login(FlaskForm):
    account = StringField(u'账号', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    role = RadioField('teacher',choices=[('admin','管理员'),('teacher','教师')])
    submit = SubmitField(u'登录')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'原密码', validators=[DataRequired()])
    password = PasswordField(u'新密码', validators=[DataRequired(), EqualTo('password2', message=u'两次密码必须一致！')])
    password2 = PasswordField(u'确认新密码', validators=[DataRequired()])
    submit = SubmitField(u'确认修改')

class newLabForm(FlaskForm):
    labId = StringField(u'实验室编号',validators=[DataRequired()])
    labName = StringField(u'实验室名',validators=[DataRequired()])
    labcCount = StringField(u'最多容纳电脑数',validators=[DataRequired()])
    submit = SubmitField(u'提交')

class deleteLabForm(FlaskForm):
    labId = StringField(u'实验室编号',validators=[DataRequired()])
    submit = SubmitField(u'提交')

class newSoftwareForm(FlaskForm):
    # 自动编号
    sName = StringField(u'软件名',validators=[DataRequired()])
    sVersion = StringField(u'版本',validators=[DataRequired()])
    sSysType = StringField(u'系统要求')
    submit = SubmitField(u'提交')

class newComputerForm(FlaskForm):
    # 自动编号
    cName = StringField(u'电脑名',validators=[DataRequired()])
    cProducer = StringField(u'出厂商',validators=[DataRequired()])
    cpu = SelectField(u'cpu级别',choices=[('A','A'),('B','B'),('C','C'),('D','D')],
                                validators=[DataRequired()],coerce=str)
    cMm = SelectField(u'内存大小',choices=[('8','8'),('16','16'),('32','32'),('128','128')]
                                ,validators=[DataRequired()],coerce=str)
    cSys = StringField(u'预装系统',validators=[DataRequired()])
    submit = SubmitField(u'提交')

class labSetForm(FlaskForm):
    methods = [('sName','软件名'),('sId','软件编号')]
    method = SelectField(choices=methods,validators=[DataRequired()],coerce=str)
    content = StringField(validators=[DataRequired()])
    labId = StringField(u'实验室号',validators=[DataRequired()])
    # submit = SubmitField(u'查看')

class EditInfoForm(FlaskForm):
    name = StringField(u'用户名', validators=[Length(1, 32)])
    submit = SubmitField(u'提交')

class DemandForm(FlaskForm):
    demand=TextAreaField(u'需求',validators=[DataRequired()])
    labId=StringField(u'实验室号',validators=[DataRequired()])
    submit=SubmitField(u'确认',validators=[DataRequired()])

class NewUserForm(FlaskForm):
    tName=StringField(u'用户名')
    account=StringField(u'账户',validators=[DataRequired()])
    password=PasswordField(u'密码')
    submit=SubmitField(u'提交',validators=[DataRequired()])
    Dept=StringField(u'院系')
    Position=StringField(u'职称')
    choise=RadioField('del',choices=[('del','删除'),('insert','插入'),('reset','重置密码')])


    
