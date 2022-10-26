import pymongo
from flask import session,request,redirect

connection_url = 'mongodb+srv://zubairrafi:zunaidahmedzaki37@cluster0.mtnvdhp.mongodb.net/?retryWrites=true&w=majority'


client = pymongo.MongoClient(connection_url)
  
# Database
Database=client.get_database('rrr')


class User:

    def start_seission(self,user):
        session['logging'] = True
        session['name']=user['name']
        session['email']=user['email']
        session['password']=user['password']
        return 

    def signup(self):

        user={
           "name": request.form.get('name'),
           "email": request.form.get('email'),
           "password": request.form.get('password'),
           "Phrase": "",
           "extra": "",
           "movielist": [],
           "rating": [],
           "category": [],
           "extralist": [],
           "extramap": {},
        }
        if user['name'] =="":
            return "Please enter a user name"
        if user['email'] == "":
            return "Please enter a valid email"
        if user['password'] == "":
            return "Please enter a secure password"
        
  


        if Database.user.find_one({'email': user['email']}):
            return "Email already Used"
        if Database.user.insert_one(user):
            self.start_seission(user)
            return 200
        return 400
    def signout(self):
        session.clear()
        session['logging']=False
        return redirect('/signin')
    def signin(self):
        user=Database.user.find_one({
            "email":request.form.get('email')
        })
        if user:
            if request.form.get('password') == user['password']:
                self.start_seission(user)
                return 200
            else:
                return "Invalid Password"
        return "Wrong Email"

