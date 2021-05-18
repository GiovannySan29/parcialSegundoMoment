from flask import Flask, render_template,request,redirect,url_for,session   
from bson import ObjectId
from flask.helpers import flash 
from passlib.hash import sha256_crypt
from pymongo import MongoClient
from functools import wraps    
import os    
from pymongo.collation import CollationAlternate

    
app = Flask(__name__) 
app.secret_key ="abcd1234"      
    
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.landhoteles    
collectionUser = db.Users
collectionApart = db.Apartments

@app.route('/')    
def home ():    
    return render_template('home.html')  

@app.route('/login')
def login():
    return render_template('login.html') 

@app.route('/register')
def register():
    return render_template('register.html') 

@app.route('/add_apartment')
def add_apartment():
    return render_template('add_apartment.html') 

@app.route('/Apartaments')
def Apartaments():
    return render_template('Apartaments.html') 

@app.route('/administracion')
def administracion():
    username = session["Users"]
    user = collectionUser.find_one({'username': username})
    if 'Users' in session:
        return render_template("administracion.html",  user = user["_id"])  
    else:
        return render_template("index.html")


@app.route("/registerUsers", methods=['POST'])    
def registerUsers():    
    #Adding a Task 
    if request.method == 'POST':
        fullname=request.form.get("fullname")    
        email=request.form.get("email")    
        username=request.form.get("username")    
        country=request.form.get("country")    
        city=request.form.get("city")    
        password=request.form.get("password")    
        typeUsers=request.form.get("typeUsers")    
        collectionUser.insert({"fullname":fullname, "email":email, "username":username, "country":country, "city":city, "password":password,"typeUsers":typeUsers})
        flash("usuario agregado")
        return redirect(url_for('login'))
    return render_template('register.html') 

@app.route("/loginUsers", methods=['POST'])    
def loginUsers():    
    username = request.form.get('username')
    password = request.form.get('password')
    resultRequest = {'password': password,'username':username}
    session['Users'] = username
    result = collectionUser.find_one(resultRequest)
    if result != None:
        if result["typeUsers"] == "invitado":
            return redirect(url_for('home'))
        else:
            return redirect(url_for('administracion'))   

@app.route("/edit_user/<id>")    
def edit_user(id): 
    userEd = collectionUser.find_one({'_id': ObjectId(id)})
    result = []
    result.append({
        '_id':userEd['_id'],
        'fullname':userEd['fullname'],
        'email':userEd['email'],
        'username':userEd['username'],
        'country':userEd['country'],
        'city':userEd['city'],
        'password':userEd['password'],
        'typeUsers':userEd['typeUsers']
    })
    return render_template("edit_user.html", user = result)

@app.route('/editUsers/<id>', methods=['POST'])    
def editUsers(id):
    fullname = request.form.get("fullname")
    email = request.form.get("email")
    username = request.form.get("username")
    country = request.form.get("country")
    city = request.form.get("city")
    password = request.form.get("password")
    typeUsers = request.form.get("typeUsers")
    collectionUser.update_one({'_id':ObjectId(id)},{"$set":{
        'fullname':fullname,
        'email':email,
        'username':username, 
        'country':country,
        'city':city,
        'password':password,
        'typeUsers':typeUsers
    }})
    return redirect(url_for('administracion'))

@app.route('/deletUsers/<id>',methods=['GET'])
def deletUsers(id):
        collectionUser.delete_one({'_id': ObjectId(id)})
        return redirect(url_for('home'))


@app.route("/add_apartments", methods=['POST'])    
def add_apartments():    
    #Adding a Task 
    if request.method == 'POST':
        city=request.form.get("city")    
        country=request.form.get("country")    
        direction=request.form.get("direction")    
        location=request.form.get("location")    
        bedroom=request.form.get("bedroom")    
        picture=request.form.get("picture")    
        photo=request.form.get("photo")    
        value=request.form.get("value")    
        description=request.form.get("description")    
        collectionApart.insert({"city":city, "country":country, "direction":direction, "location":location, "bedroom":bedroom, "picture":picture,"photo":photo, "value":value, "description":description })
        return redirect(url_for('administracion'))
    return render_template('add_apartment.html')


@app.route("/apartments", methods=['POST'])    
def apartments():
    collectionA = collectionApart.find()    
    a1="active"    
    return render_template('Apartaments.html',a1=a1,collectionApart=collectionA)


@app.route("/edit_Apartaments/<id>")    
def edit_Apartaments(id): 
    apartmentsEd = collectionApart.find_one({'_id': ObjectId(id)})
    results = []
    results.append({
        '_id':apartmentsEd['_id'],
        'city':apartmentsEd['city'],
        'country':apartmentsEd['country'],
        'direction':apartmentsEd['direction'],
        'location':apartmentsEd['location'],
        'bedroom':apartmentsEd['username'],
        'picture':apartmentsEd['picture'],
        'photo':apartmentsEd['photo'],
        'value':apartmentsEd['value'],
        'description':apartmentsEd['description']
    })
    return render_template("edit_Apartaments.html", aparts = results)

@app.route('/editApartaments/<id>', methods=['POST'])    
def editApartaments(id):
    city=request.form.get("city")    
    country=request.form.get("country")    
    direction=request.form.get("direction")    
    location=request.form.get("location")    
    bedroom=request.form.get("bedroom")    
    picture=request.form.get("picture")    
    photo=request.form.get("photo")    
    value=request.form.get("value")    
    description=request.form.get("description")  
    collectionApart.update_one({'_id':ObjectId(id)},{"$set":{
        'city':city, 
        'country':country, 
        'direction':direction, 
        'location':location, 
        'bedroom':bedroom, 
        'picture':picture,
        'photo':photo, 
        'value':value, 
        'description':description 
    }})
    return redirect(url_for('administracion'))

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


    
if __name__ == "__main__":    
    app.run(debug=True)   