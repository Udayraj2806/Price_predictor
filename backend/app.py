
from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import sqlite3
from werkzeug.utils import secure_filename
# from models import Img
import pandas as pd
import pickle


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"




app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


db=SQLAlchemy(app)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# def save_image(picture_file):
#     picture=picture_file.filename
#     picture_path=os.path.join(app.root_path,'static/profile_pics',picture)
#     picture_file.save(picture_path)
#     return picture_name

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    car_name=db.Column(db.String(200),nullable=False)
    year=db.Column(db.Integer,nullable=False)
    fuel= db.Column(db.String(200),nullable=False)
    km_travelled=db.Column(db.String(200),nullable=False)
    email= db.Column(db.String(200),nullable=False)
    ph_number=db.Column(db.String(200),nullable=False)
    price=db.Column(db.String(200),nullable=False)
    filename=db.Column(db.Text,nullable=False)



    def __repr__(self)-> str:
        return f"{self.sno} - {self.car_name}"

model=pickle.load(open("Model.pkl",'rb'))
car=pd.read_csv('Cleaned Car.csv')



@app.route('/predict1',methods=['GET'])
def predict1():
    if request.method == 'GET':
        return render_template('predict.html')


@app.route('/')
def home():



    return render_template('home.html')

@app.route('/about')
def aboutus():



    return render_template('aboutus.html')


@app.route('/sell2')
def sell2():



    return render_template('sell.html')


app.config['UPLOAD_FOLDER']="static\images"

@app.route('/sell1',methods=['GET','POST'])
def sell1():
    if request.method=='POST':
        car_name = request.form['car_name']
        year =int(request.form['year'])
        fuel = request.form['fuel']
        km_travelled = request.form['km_travelled']
        ph_number = request.form['ph_number']
        email = request.form['email']
        price = request.form['price']
        file=request.files['pic']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print('upload_image filename: ' + filename)



    car_features=Todo(car_name=car_name,year=year,fuel=fuel,km_travelled=km_travelled,ph_number=ph_number,email=email,price=price,filename=filename)
    db.session.add(car_features)
    db.session.commit()
    global_cars = Todo.query.all()
    print(global_cars.reverse())
    print(filename)
    return render_template('sell.html',car_features=car_features,filename=filename)

@app.route('/display/<filename>')
def display_image(filename):
	# print('yes' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/sell')
def index():
    companies =sorted(car['company'].unique())
    car_models=sorted(car['name'].unique())
    year=sorted(car['year'].unique(),reverse=True)
    fuel_type=car['fuel_type'].unique()
    return render_template('index.html',companies=companies,car_models=car_models,years=year,fuel_types=fuel_type)

@app.route('/predict',methods=['POST'])
def predict():
    company =request.form.get('company')
    car_model=request.form.get('car_models')
    year=int(request.form.get('year'))
    fuel_type=request.form.get('fuel_type')
    kms_driven=request.form.get('kilo_driven')
    # print(company, car_model, year, fuel_type, kms_driven)
    prediction=model.predict(pd.DataFrame([[car_model,company,year,kms_driven,fuel_type]],columns=['name','company','year','kms_driven','fuel_type']))
    predicted_price=str(prediction[0])
    # print(type(y))
    # car_features=Todo(companies=company,car_model=car_model,year=year,fuel_type=fuel_type,kms_driven=kms_driven,price=predicted_price)
    # db.session.add(car_features)
    # db.session.commit()

    return str(prediction[0])
conn=sqlite3.connect('todo.db')
cursor=conn.cursor()

@app.route('/buy')
def index1():
    global_cars= Todo.query.all()
    global_cars.reverse()
    # m=cursor.execute("""SELECT img FROM todo""")
    # for x in m:
    #     print(x)
    return render_template('index1.html',global_cars=global_cars)
# @app.route("/index")
# def hello_world():
#     return render_template('index.html')
if __name__== "__main__":
    app.run(debug=True)
