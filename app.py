from socketserver import DatagramRequestHandler
from unicodedata import category
from flask import Flask, render_template, request,session

from flask_sqlalchemy import SQLAlchemy
import model
import Poster
from user import user_blueprint 
g={}
from database import Database
from search_web import *


app = Flask(__name__)
app.register_blueprint(user_blueprint)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='b\xd1B\xd1@nS\xd3\xdb\xb9.\x07y!\xd8\xa7'

db=SQLAlchemy(app)

class movielist(db.Model):
    No= db.Column(db.Integer,primary_key=True)
    MovieName= db.Column(db.String(200),nullable=False)
    Category= db.Column(db.String(200),nullable=False)
    rating=db.Column(db.Float,nullable=False)
    def __repr__(self) -> str:
        return f"{self.MovieName} - {self.Category} - {self.rating}"


@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/", methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        moviename=request.form['moviename']
        category=request.form['category']
        rating=request.form['rating']
        data=movielist(MovieName=moviename,Category=category,rating=rating)
        if 'name' in session:
            user=Database.user.find_one({'email': session['email']})
            user['movielist'].append(moviename)
        db.session.add(data)
        db.session.commit()
    allMovie=movielist.query.all()
    return render_template('index.html',allMovie=allMovie,one=Poster.Breaking,two=Poster.Cars,three=Poster.Iron,four=Poster.Inception,cnt=0)

@app.route("/clear", methods=['GET','POST'])
def clear():
    db.session.query(movielist).delete()
    db.session.commit()
    allMovie=movielist.query.all()
    return render_template('index.html',allMovie=allMovie,one=Poster.Breaking,two=Poster.Cars,three=Poster.Iron,four=Poster.Inception,cnt=0)

@app.route("/add", methods=['GET','POST'])
def add():
    if request.method=='POST':
        name=request.form.get('movie')
        genre=request.form.get('genre')
        if( name=="" ):
            return render_template('add.html',reply="Enter a valid movie name")
        if(genre ==""):
            return render_template('add.html',reply="Enter a valid genre ")
        user_movie={
            "movie": name,
            "genre": genre,
            "contributer": session['name']
        }
        Database.movie.insert_one(user_movie)
        return render_template('add.html',reply="Movie Added succesfully")
    return render_template('add.html')

@app.route("/watchlist")
def suggest():
    a={}
    poster={}
    allMovie=movielist.query.all()
    gen=1
    lib=[]
    if(allMovie):
        for i in allMovie:
            if (i.Category=='animation'):
                gen=16
            if (i.Category=='action'):
                gen=28
            if (i.Category=='adventure'):
                gen=12
            if (i.Category=='comedy'):
                gen=35
            if (i.Category=='crime'):
                gen=80
            if (i.Category=='documentary'):
                gen=99
            if (i.Category=='drama'):
                gen=18
            if (i.Category=='family'):
                gen=10751
            if (i.Category=='fantasy'):
                gen=14
            if (i.Category=='history'):
                gen=36
            if (i.Category=='horror'):
                gen=27
            if (i.Category=='music'):
                gen=10402
            if (i.Category=='mystery'):
                gen=9648
            if (i.Category=='romance'):
                gen=10749
            if (i.Category=='science fiction'):
                gen=878
            if (i.Category=='thriller'):
                gen=53
            if (i.Category=='tv movie'):
                gen=10770
            if (i.Category=='war'):
                gen=10752
            if (i.Category=='western'):
                gen=37
            z=model.doit(i.MovieName,gen)
            p=model.getPoster(gen)
            f=model.sim(i.MovieName)
            poster=poster | p
            a=a |z
            do=model.lib_get(i.MovieName)
            lib.append({'name':do.title,
                       'poster': do.poster_path}
            )

        
        a=model.getit(a)
    user=Database.user.find({})
    this_user=Database.user.find_one({'email': session['email']})
    score=0
    mscore=-1
    for i in user:
        if this_user['email']!= i['email']:
            score=model.check_sim(this_user['movielist'],i['movielist'])
            if score>mscore:
                mscore=score
                flist=i['movielist']
    allMovie=movielist.query.all()
    for i in this_user['movielist']:
        for j in flist:
            if i == j:
                flist.remove(j)
    pheu=model.get_poster(flist)
    return render_template('suggestion.html',check=a,poster=poster,lib=lib,pheu=pheu)

@app.route("/mylist")
def movies():
    return render_template('movies.html',search=Poster.s)
@app.route('/error', methods=['GET'])
def error():
    return render_template('index.html'), {"Refresh": "1; url=/watchlist"}

@app.route('/search/<string:name>', methods=['GET'])
def find(name):
    google_search(name)
    allMovie=movielist.query.all()
    return render_template('index.html',allMovie=allMovie,one=Poster.Breaking,two=Poster.Cars,three=Poster.Iron,four=Poster.Inception,cnt=0)

@app.route('/watchlist/<string:name>', methods=['GET'])
def watch(name):
    user=Database.user.find_one({
            "email":session['email']
    })
    lula=user['movielist']
    if (name=="Kwurt"):
        lula=lula
    else:
        lula.append(name)
    final=[]
    for i in lula:
        ok = model.wPoster(i)
        if ok=="":
            final=final
        else:
            final.append(ok)
    Database.user.update_one({'email':session['email']},{"$set":{"movielist":lula}})
    return render_template('watchlist.html',final=final)

@app.route('/remove/<string:name>', methods=['GET'])
def remove(name):
    user=Database.user.find_one({
            "email":session['email']
    })
    lula=user['movielist']
    lula.remove(name)
    final=[]
    for i in lula:
        ok = model.wPoster(i)
        final.append(ok)
    Database.user.update_one({'email':session['email']},{"$set":{"movielist":lula}})
    return render_template('watchlist.html',final=final)


if __name__ == "__main__":
    app.run(debug=True)

