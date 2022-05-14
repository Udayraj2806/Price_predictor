
from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
import pickle


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"




app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


db=SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    companies=db.Column(db.String(200),nullable=False)
    car_model=db.Column(db.String(200),nullable=False)
    year=db.Column(db.Integer,nullable=False)
    fuel_type= db.Column(db.String(200),nullable=False)
    kms_driven=db.Column(db.String(200),nullable=False)
    price=db.Column(db.String(200),nullable=False)

    def __repr__(self)-> str:
        return f"{self.sno} - {self.companies}"

model=pickle.load(open("Model.pkl",'rb'))
car=pd.read_csv('Cleaned Car.csv')



@app.route('/predict1',methods=['GET'])
def predict1():
    if request.method == 'GET':
        return render_template('predict.html')


@app.route('/')
def home():


    return render_template('home.html')


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
    car_features=Todo(companies=company,car_model=car_model,year=year,fuel_type=fuel_type,kms_driven=kms_driven,price=predicted_price)
    db.session.add(car_features)
    db.session.commit()

    return str(prediction[0])


@app.route('/buy')
def index1():
    global_cars= Todo.query.all()
    print(global_cars.reverse())
    return render_template('index1.html',global_cars=global_cars)
# @app.route("/index")
# def hello_world():
#     return render_template('index.html')
if __name__== "__main__":
    app.run(debug=True)
