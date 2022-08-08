from unicodedata import category
from flask import Flask, render_template, request

from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

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
        db.session.add(data)
        db.session.commit()
    allMovie=movielist.query.all()
    return render_template('index.html',allMovie=allMovie)

@app.route("/mylist")
def movies():
    return "this is second page"

if __name__ == "__main__":
    app.run(debug=True)

