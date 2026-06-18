from flask import (

    Flask,

    render_template,

    request,

    redirect,

    url_for,

    flash,

    session,

    jsonify

)

from werkzeug.security import (

    generate_password_hash,

    check_password_hash

)

from config import Config

from models import (

    db,

    User,

    Post,

    Category,

    Comment,

    Like

)

import markdown

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

# =========================

# 首页

# =========================

@app.route("/")

def index():

    posts = Post.query.order_by(

        Post.create_time.desc()

    ).all()

    categories = Category.query.all()

    return render_template(

        "index.html",

        posts=posts,

        categories=categories

    )

# =========================

# 注册

# =========================

@app.route("/register", methods=["GET", "POST"])

def register():

    if request.method == "POST":

        username = request.form["username"]

        email = request.form["email"]

        password = request.form["password"]

        user = User.query.filter_by(

            username=username

        ).first()

        if user:

            flash("用户名已存在")

            return redirect(url_for("register"))

        new_user = User(

            username=username,

            email=email,

            password=generate_password_hash(password)

        )

        db.session.add(new_user)

        db.session.commit()

        flash("注册成功")

        return redirect(url_for("login"))

    return render_template("register.html")

# =========================

# 登录

# =========================

@app.route("/login", methods=["GET", "POST"])

def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        user = User.query.filter_by(

            username=username

        ).first()

        if user and check_password_hash(

                user.password,

                password):

            session["user_id"] = user.id

            session["username"] = user.username

            flash("登录成功")

            return redirect(url_for("index"))

        flash("用户名或密码错误")

    return render_template("login.html")

# =========================

# 退出

# =========================

@app.route("/logout")

def logout():

    session.clear()

    return redirect(url_for("index"))

# =========================

# 发布文章

# =========================

@app.route("/add", methods=["GET", "POST"])

def add_post():

    if "user_id" not in session:

        return redirect(url_for("login"))

    categories = Category.query.all()

    if request.method == "POST":

        title = request.form["title"]

        content = request.form["content"]

        category_id = request.form["category"]

        post = Post(

            title=title,

            content=content,

            user_id=session["user_id"],

            category_id=category_id

        )

        db.session.add(post)

        db.session.commit()

        flash("文章发布成功")

        return redirect(url_for("index"))

    return render_template(

        "add_post.html",

        categories=categories

    )

# =========================

# 文章详情

# =========================

@app.route("/post/<int:post_id>")

def detail(post_id):

    post = Post.query.get_or_404(post_id)

    post.views += 1

    db.session.commit()

    html_content = markdown.markdown(

        post.content,

        extensions=["fenced_code"]

    )

    comments = Comment.query.filter_by(

        post_id=post_id

    ).order_by(

        Comment.create_time.desc()

    ).all()

    likes = Like.query.filter_by(

        post_id=post_id

    ).count()

    return render_template(

        "detail.html",

        post=post,

        html_content=html_content,

        comments=comments,

        likes=likes

    )

# =========================

# 编辑文章

# =========================

@app.route("/edit/<int:id>", methods=["GET", "POST"])

def edit_post(id):

    post = Post.query.get_or_404(id)

    if request.method == "POST":

        post.title = request.form["title"]

        post.content = request.form["content"]

        post.category_id = request.form["category"]

        db.session.commit()

        flash("修改成功")

        return redirect(

            url_for("detail", post_id=id)

        )

    categories = Category.query.all()

    return render_template(

        "edit_post.html",

        post=post,

        categories=categories

    )

# =========================

# 删除文章

# =========================

@app.route("/delete/<int:id>")

def delete_post(id):

    post = Post.query.get_or_404(id)

    db.session.delete(post)

    db.session.commit()

    flash("删除成功")

    return redirect(url_for("index"))

# =========================

# 评论

# =========================

@app.route("/comment/<int:post_id>", methods=["POST"])

def add_comment(post_id):

    if "user_id" not in session:

        return redirect(url_for("login"))

    content = request.form["content"]

    comment = Comment(

        content=content,

        user_id=session["user_id"],

        post_id=post_id

    )

    db.session.add(comment)

    db.session.commit()

    return redirect(

        url_for("detail", post_id=post_id)

    )

# =========================

# 点赞

# =========================

@app.route("/like/<int:post_id>")

def like(post_id):

    if "user_id" not in session:

        return jsonify({

            "status": "login"

        })

    user_id = session["user_id"]

    exist = Like.query.filter_by(

        user_id=user_id,

        post_id=post_id

    ).first()

    if exist:

        db.session.delete(exist)

        db.session.commit()

        count = Like.query.filter_by(

            post_id=post_id

        ).count()

        return jsonify({

            "liked": False,

            "count": count

        })

    like_obj = Like(

        user_id=user_id,

        post_id=post_id

    )

    db.session.add(like_obj)

    db.session.commit()

    count = Like.query.filter_by(

        post_id=post_id

    ).count()

    return jsonify({

        "liked": True,

        "count": count

    })

# =========================

# 搜索

# =========================

@app.route("/search")

def search():

    keyword = request.args.get(

        "keyword",

        ""

    )

    posts = Post.query.filter(

        Post.title.contains(keyword)

    ).all()

    return render_template(

        "search.html",

        posts=posts,

        keyword=keyword

    )

# =========================

# 分类

# =========================

@app.route("/category/<int:id>")

def category(id):

    category = Category.query.get_or_404(id)

    posts = Post.query.filter_by(

        category_id=id

    ).all()

    return render_template(

        "category.html",

        posts=posts,

        category=category

    )

# =========================

# 归档

# =========================

@app.route("/archive")

def archive():

    posts = Post.query.order_by(

        Post.create_time.desc()

    ).all()

    return render_template(

        "archive.html",

        posts=posts

    )

# =========================

# 关于我

# =========================

@app.route("/about")

def about():

    return render_template("about.html")

# =========================

# 启动

# =========================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0"
        
    )