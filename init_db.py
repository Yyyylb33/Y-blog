from flask import Flask

from config import Config

from models import db

from models import Category

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

with app.app_context():

    db.drop_all()

    db.create_all()

    categories = [

        Category(name="技术分享"),

        Category(name="学习笔记"),

        Category(name="生活随笔"),

        Category(name="读书心得")

    ]

    for c in categories:

        db.session.add(c)

    db.session.commit()

    print("数据库创建成功")