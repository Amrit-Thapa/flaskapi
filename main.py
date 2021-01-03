from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from shortenLink import createid


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datab.sqlite3'

db = SQLAlchemy(app)

'''

'''

# creating database


class LINKS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(1000))
    linkId = db.Column(db.String(6), unique=True)

# storeing links to db


def addnewlink(url):
    id = createid()
    newlink = LINKS(link=url, linkId=id)
    db.session.add(newlink)
    db.session.commit()
    return id


@app.route('/')
def home():
    return render_template('index.html', message="shorten your url here")


@app.route('/shorten', methods=['POST'])
def shorten():
    link = request.form['link']
    linkid = addnewlink(link)
    return render_template('index.html', message=linkid)


@app.route('/<linkid>')
def redir(linkid):
    url = LINKS.query.filter_by(linkId=linkid).first()
    link = url.link
    return redirect(link, code=302)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
