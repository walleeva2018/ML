from socketserver import DatagramRequestHandler
from unicodedata import category
from flask import Flask, render_template, request,session,redirect,url_for

from flask_sqlalchemy import SQLAlchemy
import model
import Poster
from user import user_blueprint 
g={}
from database import Database
from search_web import *
from database import User
import pandas as pd
from database import Database
import os
import datetime


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

import random
  
# prints a random value from the list
list1 = [1, 2, 3, 4, 5, 6,8,3,6,1,2,33,4,22,12,13,23,22,15,18,9]

@app.route("/", methods=['GET','POST'])
def hello_world():
    if request.method == 'POST': 
        reply=User().signin()
        if reply == 200:
            if(session['role']=='USER'):
                return redirect('/landingUser')
            if(session['role']=='AGENCY'):
                return redirect('/landingAge')
            return redirect('/landingGov')
        else:
            return render_template('signin.html',reply=reply)
    else :
        return render_template('signin.html')

import plotly.express as px
@app.route("/landingUser", methods=['GET','POST'])
def cello_world():
    lat=[]
    lon=[]
    df=pd.read_csv('projects.csv')
    for i in range(len(df)):
        lat.append(float(df['latitude'][i]))
        lon.append(float(df['longitude'][i]))
    df['lon']=lon
    df['lat']=lat
    fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="name", hover_data=["goal", "exec"],
                        color_discrete_sequence=["fuchsia"], zoom=8, height=300)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    script_dir = os.path.dirname(__file__)
    results_dir = os.path.join(script_dir, 'static/')
    sample_file_name = "map.png"
    #fig.savefig(results_dir+sample_file_name)   # save the figure to file
    #plt.close(fig) 
    if request.method == 'POST': 
        return render_template('signin.html')
    else :
        return render_template('landingUser.html',fig=fig)

import matplotlib.pyplot as plt

@app.route("/landingAge", methods=['GET','POST'])
def bello_world():
    if request.method == 'POST':
        return render_template('signin.html')
    else :
        return render_template('landingAge.html')

@app.route("/landingGov", methods=['GET','POST'])
def gov():
    if request.method == 'POST':
        #reply=User().signin()
        #if reply == 200:
        #return redirect('/landingGov')
        return render_template('signin.html')
    else :
        df=Database.projects.find({})
        x=[]
        y=[]
        cnt=1
        for i in df:
            x.append(cnt+1)
            y.append(float(i['completion']))
            cnt=cnt+1
        plt.xlabel("Project NO.")
        plt.ylabel("Completion in percentage")
        fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
        ax.plot(x, y)
        script_dir = os.path.dirname(__file__)
        results_dir = os.path.join(script_dir, 'static/')
        sample_file_name = "sample.png"
        fig.savefig(results_dir+sample_file_name)   # save the figure to file
        plt.close(fig) 
        proDB=Database.projects.find({})

        consDB=Database.components.find({})
        constDB=Database.constraints.find({})
        const=[]
        floc=[]
        lf=[]
        for i  in constDB:
            dl={
                'code': i['code'], 
                'limit': i['max_limit'],
            }
            const.append(dl)
        task=[]
        for i in proDB:
            x=i['start_date'].split('-')[0]
            a=x[0]
            b=int(a)
            a=x[1]
            b=b*10+int(a)
            a=x[2]
            b=b*10+int(a)
            a=x[3]
            b=b*10+int(a)
            print(b)
            b=b+int(i['timespan'])
            ans=str(b)+"-" +i['start_date'].split('-')[1]+"-" +i['start_date'].split('-')[1]
            g={'name': i['name'],
                'start_date': i['start_date'],
                'end_date': ans,
            }


            #print(ans)

            task.append(g)
        newlist = sorted(task, key=lambda d: d['start_date'])
        return render_template('landingGov.html',task=newlist)



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
        plot=request.form.get('plot')
        language=request.form.get('language')
        if( name=="" ):
            return render_template('add.html',reply="Enter a valid movie name")
        if(genre ==""):
            return render_template('add.html',reply="Enter a valid genre ")
        user_movie={
            "movie": name,
            "genre": genre,
            "contributer": session['name'],
            "plot": plot,
            "language": language,
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
    if(allMovie):
        sfa=model.gsfa(allMovie)
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
    return render_template('suggestion.html',check=a,poster=poster,lib=lib,pheu=pheu,sfa=sfa)

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

@app.route('/contributer', methods=['GET'])
def con():
    movie=Database.movie.find({})
    return render_template("contributer.html",movie=movie)


if __name__ == "__main__":
    app.run(debug=True)

