from flask import Flask, render_template, session, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from flask_script import Manager, Shell
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.mssql import  \
    BIGINT, BINARY, BIT, CHAR, DATE, DATETIME, DATETIME2, \
    DATETIMEOFFSET, DECIMAL, FLOAT, IMAGE, INTEGER, MONEY, \
    NCHAR, NTEXT, NUMERIC, NVARCHAR, REAL, SMALLDATETIME, \
    SMALLINT, SMALLMONEY, SQL_VARIANT, TEXT, TIME, \
    TIMESTAMP, TINYINT, UNIQUEIDENTIFIER, VARBINARY, VARCHAR
from sqlalchemy import CheckConstraint,ForeignKey,PrimaryKeyConstraint
import os
from sql_for_lab import *
# import pandas as pd
from form import *
import time
app = Flask(__name__)
# app.run(debug=True)
manager = Manager(app)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
user = 'sa'
pwd = 'admin'
server = 'localhost'
dbname = 'DB_laboratory'
driver = "ODBC Driver 17 for SQL Server"
app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc://{user}:{pwd}@{server}/{dbname}?driver={driver}"
basedir = os.path.abspath(os.path.dirname(__file__))
# db_engine, tables = get_database()
db = SQLAlchemy(app)

def make_shell_context():
    return dict(app=app, db=db, Adminitrator=Adminitrator, Teacher=Teacher)
    # pass

manager.add_command("shell", Shell(make_context=make_shell_context))

# stop visitor
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'basic'
login_manager.login_view = 'login'
login_manager.login_message = u"请先登录。"

class Adminitrator(db.Model,UserMixin): 
    __tablename__='Adminitrator'
# 简单起见 管理员都是全权限
    id = db.Column(CHAR(16), primary_key=True)
    pwd = db.Column(CHAR(128),nullable=False)
    aName = db.Column(NVARCHAR(32),nullable=False)


    def __init__(self, id, pwd, aName):
        self.id = id
        self.aName = aName
        self.pwd = pwd
        # self.right = right

    def get_id(self):
        return self.id

    def verify_password(self, pwd):
        # pwd_hash=generate_password_hash(pwd)
        if check_password_hash(self.pwd.strip(),pwd.strip()):
            return True
        else:
            return False

    def __repr__(self):
        return '<Adminitrator %r>' % self.aName

class Teacher(db.Model,UserMixin):
    __tablename__='Teacher'
    id = db.Column(CHAR(16), primary_key=True)
    pwd = db.Column(CHAR(128),nullable=False)
    tName = db.Column(NVARCHAR(32),nullable=False) 
    Dept = db.Column(NVARCHAR(64),nullable=False) # 系别
    Position = db.Column(NVARCHAR(8),nullable=False) # 职位: 教授 副教授 助理教授 讲师 辅导员

    def __init__(self, id,pwd,tName,dept,position):
        self.id = id
        self.tName = tName
        self.pwd = pwd
        self.dept = dept
        self.position = position
        # self.right = right

    def get_id(self):
        return self.id

    def verify_password(self, pwd):
        # pwd_hash=generate_password_hash(pwd)
        if check_password_hash(self.pwd.strip(),pwd.strip()):
            return True
        else:
            return False

    def __repr__(self):
        return '<Teacher %r>' % self.tName

class Software(db.Model):
    __tablename__='Software'
    id = db.Column(CHAR(16),primary_key=True)
    sName = db.Column(NVARCHAR(None),nullable=False)
    version = db.Column(NVARCHAR(8),nullable=True)
    sysType = db.Column(CHAR(16),nullable=False) # win7 ubuntu16.04 centos 7
    aId = db.Column(CHAR(16),ForeignKey('Adminitrator.id'),nullable=False)

    def __repr__(self):
        return '<Software %r>' % self.sName

class Laboratory(db.Model):
    __tablename__='Laboratory'
    id = db.Column(CHAR(16),primary_key=True)
    lName = db.Column(NVARCHAR(32),nullable=False)
    aId = db.Column(CHAR(16),ForeignKey('Adminitrator.id'),nullable=False)
    cCount = db.Column(INTEGER,nullable=False)

    def __repr__(self):
        return '<Laboratory %r>'%self.lName

class Computer(db.Model):
    __tablename__='Computer'
    id = db.Column(CHAR(16),primary_key=True)
    cName = db.Column(NVARCHAR(16),nullable=False)
    producer = db.Column(NVARCHAR(16),nullable=False)
    aId = db.Column(CHAR(16),ForeignKey('Adminitrator.id'),nullable=False) # 入库管理员
    lId = db.Column(CHAR(16),ForeignKey('Laboratory.id')) # 所在lab编号
    normal = db.Column(BIT,nullable=False,default=1) # 正常与否

    def __repr__(self):
        return '<Computer %r>'%self.cName
    
class InstallList(db.Model): 
    __tablename__='InstallList'
    id = db.Column(CHAR(32),primary_key=True) # 格式:in<date>/<nums>：in20170901/1
    aId = db.Column(CHAR(16),ForeignKey('Adminitrator.id'),nullable=False)
    cId = db.Column(CHAR(16),ForeignKey('Computer.id'),nullable=False)
    sId = db.Column(CHAR(16),ForeignKey('Software.id'),nullable=False)

    def __repr__(self):
        return '<InstallList %r>' % self.id

class LabManage(db.Model):
    __tablename__='LabManage'
    id = db.Column(INTEGER,autoincrement=True,primary_key=True)
    lId = db.Column(CHAR(16),ForeignKey('Laboratory.id'),nullable=False)
    aId = db.Column(CHAR(16),ForeignKey('Adminitrator.id'),nullable=False)

    def __repr__(self):
        return '<LabManage %r>' % self.id

class Demand(db.Model):
    __tablename__='Demand'
    id = db.Column(CHAR(32),primary_key=True) # 格式:de<date>/<nums>
    tId = db.Column(CHAR(16),ForeignKey('Teacher.id'),nullable=False)
    lId = db.Column(CHAR(16),ForeignKey('Laboratory.id'),nullable=False) # 目标实验室号
    aId = db.Column(CHAR(16),ForeignKey('Adminitrator.id'))
    content = db.Column(NVARCHAR(None)) # 
    response = db.Column(NVARCHAR(None)) # 回复可选
    inDate = db.Column(DATE,server_default='GETDATE()')
    closeDate = db.Column(DATE) #null:待处理 not null:已经解决
    
    def __repr__(self):
        return '<Demand %r>' %self.id

class ComputerSys(db.Model):
    __tablename__='ComputerSys'
    __table_args__ = (
        PrimaryKeyConstraint('cId', 'sys'),
    )
    cId = db.Column(CHAR(16),ForeignKey('Computer.id'),nullable=False)
    sys = db.Column(CHAR(16),nullable=False)
    def __repr__(self):
        return '<ComputerSys computer_%r,system_%r>' %(self.cId,self.sys)
# web
@login_manager.user_loader
def load_admin(id):
    if session['role']=='admin':
        return Adminitrator.query.get(str(id))
    elif session['role']=='teacher':
        return Teacher.query.get(str(id))


@app.route('/',methods=['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        if form.role.data == 'admin':
            user = Adminitrator.query.filter_by(id=form.account.data).first()
            if user is None or not user.verify_password(form.password.data):
                flash('账号或密码错误！')
                return redirect(url_for('login'))
            else:
                status = login_user(user)
                session['id'] = user.id
                session['name'] = user.aName
                session['role'] = 'admin'
                return redirect(url_for('admin_view'))


        elif form.role.data == 'teacher':
            user = Teacher.query.filter_by(id=form.account.data).first()
            # TODO 教师界面跳转
            if user is None or not user.verify_password(form.password):
                flash('账号或密码错误！')
                return redirect(url_for('login'))
            else:
                login_user(user)
                session['id'] = user.id
                session['name'] = user.tName
                session['role'] = 'teacher'
                return redirect(url_for('teacher_view'))
            
    return render_template('login.html', form=form)

# 本系统没有注册系统，但是有增加教师用户的功能



# def importComputerFromCSV(csv_pth,aId):
#     df = pd.read_csv(csv_pth)
#     # err = open('importComputerErr.csv','w')
#     err_df = pd.DataFrame(columns=df.columns)
#     for i,row in df.iterrows():
#         try:
#             item=Computer()
#             item.id = row['id']
#             item.cName = row['cName']
#             item.producer = row['producer']
#             item.lId = row['lId']
#             item.normal = row['normal']
#             item.aId = aId
#             db.session.add(item)
#             db.session.commit()
            
#         except:
#             err_df.loc[len(err_df)]=dict(row)
#     if(len(err_df)>0):
#         err_df.to_csv('importComputerErr.csv')
#     return len(df)-len(err_df),len(err_df) # 成功数，失败数
# # T

@app.route('/admin')
@login_required
def admin_view():
    # TODO 管理员视图
    return render_template('admin-index.html',name=session.get('name'),role=session['role'])
    

@app.route('/teacher')
@login_required
def teacher_view():
    # TODO 老师视图
    return render_template('teacher-index.html',name=session.get('name'),role=session['role'])
    pass



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经登出！')
    return redirect(url_for('login'))

@app.route('/new_lab', methods=['GET', 'POST'])
@login_required
def newLab():
    form = newLabForm()
    if form.validate_on_submit():
        exist = Laboratory.query.filter_by(id=request.form.get('labId')).first()
        if exist is not None:
            flash(u'该实验室编号已经存在,请重新填写')
        else:
            try:
                lab = Laboratory()
                lab.id = request.form.get('labId')
                lab.lName = request.form.get('labName')
                lab.aId = current_user.id
                lab.cCount = int(request.form.get('labcCount'))
                db.session.add(lab)
                flash(u'实验室信息添加成功！')
                db.session.commit()
            except :
                db.session.rollback()
                flash(u'实验室信息添加失败:(')
                
            finally:
                return redirect(url_for('newLab'))
    return render_template('new-lab.html', name=session.get('name'),role=session['role'], form=form)    

@app.route('/delete_lab', methods=['GET', 'POST'])
@login_required
def deleteLab():
    form = deleteLabForm()
    flash(u'注意:该实验室电脑将被设置为闲置')
    if form.validate_on_submit():
        exist = Laboratory.query.filter_by(id=request.form.get('labId')).first()
        if exist is None:
            flash(u'该实验室编号不存在,请重新填写')
        else:
            try:
                # 移除电脑
                db.session.execute(remove_computer_from(exist.id.strip()))
                db.session.commit()
                db.session.delete(exist)
                flash(u'实验室信息删除成功！')
                db.session.commit()
            except :
                db.session.rollback()
                flash(u'实验室信息添加失败:(')
                
            finally:
                return redirect(url_for('deleteLab'))
    return render_template('delete-lab.html', name=session.get('name'),role=session['role'], form=form)    

# TODO 查找已有实验室

@app.route('/new_software',methods = ['GET','POST'])
@login_required
def newSoftware():
    form = newSoftwareForm()
    if form.validate_on_submit():
        exist = Software.query.filter_by(sName=request.form.get('sName'),version=request.form.get('sVersion')).first() #根据版本和名字确定
        if exist is not None:
            flash(u'该版本软件已经存在,请重新填写')
        else:
            try:
                # 获取id
                result = db.session.execute(count_software)
                count = result.fetchall()[0][0]+1
                sId = f's{time.strftime("%Y%m%d",time.localtime())}/{count}'
                software = Software()
                software.id = sId
                software.aId=current_user.id
                software.sysType = request.form.get('sSysType')
                software.sName = request.form.get('sName')
                software.version = request.form.get('sVersion')
                db.session.add(software)
                flash(u'软件信息添加成功！')
                db.session.commit()
            except:
                db.session.rollback()
                flash(u'软件添加失败:(')
                
            finally:
                return redirect(url_for('newSoftware'))
    return render_template('new-software.html', name=session.get('name'),role=session['role'], form=form)    


@app.route('/new_computer',methods = ['GET','POST'])
@login_required
def newComputer():
    form = newComputerForm()
    if form.validate_on_submit():
        try:
            # 获取id
            result = db.session.execute(count_computer)
            count = result.fetchall()[0][0]+1
            cId = f's{time.strftime("%Y%m%d",time.localtime())}/{count}'
            flash(u'新电脑编号:'+cId)
            computer = Computer()
            computer.id = cId
            computer.aId=current_user.id
            computer.cName = request.form.get('cName')
            computer.producer = request.form.get('cProducer')
            db.session.add(computer)
            flash(u'软件信息添加成功！')
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'软件添加失败:(')
            
        finally:
            return redirect(url_for('newComputer'))
    return render_template('new-computer.html', name=session.get('name'),role=session['role'], form=form)    
    

# TODO 实验室配置
@app.route('/lab<id>_Set',methods=['GET','POST'])
@login_required
def labSet(id):
    form=labSetForm()
    # 设置
    if request.form['setType'] == 'software':
        # TODO 查找本实验室安装该软件的电脑
        pass
    elif request.form['setType'] == 'computer':
        # TODO 查找本实验室安装了改系统的电脑
        pass

    if form.validate_on_submit():
        if form.method.data == "software":
            # TODO 修改对应的数据
            pass
        elif form.method.data == "computer":
            # TODO 增加系统
            pass
    # lab-set.html
    pass


# TODO 计算机录入界面设计
# TODO 软件安装
# TODO 需求解决
# TODO 计算机资源查找
# TODO 计算机资源统计


