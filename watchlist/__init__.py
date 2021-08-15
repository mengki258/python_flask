# !usr/bin/env python 
# -*- coding:utf-8 _*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # 导入扩展类
import os
import sys

from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')  # 等同于 app.secret_key = 'dev'
# 数据库连接配置
WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app
login_manager = LoginManager(app)  # 实例化扩展类
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    from watchlist.models import User  # 必须放到里面引用 ，否则会造成循环引用 ，而启动失败
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象

#上下文处理哭喊：可定义会话变量
@app.context_processor
def inject_user():  # 函数名可以随意修改
    from watchlist.models import User # 必须放到里面引用 ，否则会造成循环引用 ，而启动失败
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于 return {'user': user}

from watchlist import views, errors, commands