from operator import imod
from flask import Blueprint,redirect,request,render_template
from database import User



user_blueprint = Blueprint('user_blueprint', __name__)



import pandas as pd


@user_blueprint.route('/signin',methods=['GET','POST'])
def getin():
    if request.method == 'POST':
        print(request.form.get('email'))
        print(request.form.get('password'))
        reply=User().signin()
        if reply == 200:
            return redirect('/')
        else:
            return render_template('signin.html',reply=reply)
    else :
        return render_template('signin.html')

@user_blueprint.route('/signup',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        reply= User().signup() 
        print(reply)
        if reply== 200:
            return redirect('/')
        else:
            return render_template('signup.html',reply=reply)

    else:
        return render_template('signup.html', reply="")
@user_blueprint.route('/signout',methods=['GET'])
def out():
    return User().signout()