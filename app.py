from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'jhFDXH5ngGGHFGJ88fduilsz257KJgh9f'
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date).all()
    return render_template("posts.html", articles=articles)


@app.route('/create_article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Ошибка при добавлении"
    else:
        return render_template("create_article.html")


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/post/<int:id>/post_update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "Ошибка при редактировании"
    else:
        return render_template("post_update.html", article=article)


@app.route('/post/<int:id>/del')
def post_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Ошибка при удалении"


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, nullable=True)


    def __repr__(self):
        return self.product


@app.route('/shop')
def shop():
    items = Item.query.order_by(Item.price).all()
    return render_template("shop.html", items=items)


@app.route('/create_shop', methods=['POST', 'GET'])
def create_shop():
    if request.method == 'POST':
        product = request.form['product']
        price = request.form['price']

        item = Item(product=product, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/shop')
        except:
            return "Ошибка при добавлении"
    else:
        return render_template("create_shop.html")


@app.route('/shop/<int:id>')
def shop_detail(id):
    item = Item.query.get(id)
    return render_template("shop_detail.html", item=item)

# pip install virtualenv
# pip install virtualenvwrapper-win
# class Com(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.Text, nullable=False)
#     comm = db.Column(db.Text, nullable=False)
#
#
#     def __repr__(self):
#         return self.name
#
#
# @app.route('/comment', methods=['POST', 'GET'])
# def comment():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         comm = request.form['comm']
#
#         if len(request.form['username']) > 2:
#             flash('Сообщение отправлено', category='success')
#         else:
#             flash('Ошибка отправки', category='error')
#
#         com = Com(username=username, email=email, comm=comm)
#
#         try:
#             db.session.add(com)
#             db.session.commit()
#             return redirect('/comment')
#         except:
#             return "Ошибка при добавлении"
#     else:
#         return render_template("comment.html")

# @app.route('/comment', methods=['POST', 'GET'])
# def comment():
#     if request.method == 'POST':
#         if len(request.form['username']) > 2:
#             flash('Сообщение отправлено', category='success')
#         else:
#             flash('Ошибка отправки', category='error')
#
#         return render_template("comment.html")

if __name__ == '__main__':
    app.run(debug=True)
