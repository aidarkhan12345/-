#https://www.youtube.com/watch?v=759C2p3CAA4&t=1867s
from flask import Flask, render_template,redirect 
from flask_sqlalchemy import SQLAlchemy
from flask import request
from cloudipsp import Api, Checkout
import os
import sqlite3
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
################
#current_app.config.get('SQLALCHEMY_DATABASE_URI')

#str(current_app.config.get('SQLALCHEMY_DATABASE_URI'))
###############################
class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    price =db.Column(db.Integer, nullable = False) 
    isActive = db.Column(db.Boolean, default = True)
	#text = db.Column(db.Text, nullable = False)
    def __repr__(self):
        return self.title
		
@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index2.html', data = items) #вместо data любое название
    
@app.route('/about')
def about():
    return render_template('about.html')
###################
   
@app.route('/about2')
def about2():
    return render_template('index.html')

########### обработчик
@app.route('/buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id)
    api = Api(merchant_id=1396424,secret_key='test')
    checkout = Checkout(api = api)
    data = {
        "currency": "KZT",
        "amount": str(item.price)+"00"
}
    url = checkout.url(data).get('checkout_url')

    return redirect(url)

########## 

#########################

@app.route('/create/', methods =['POST', 'GET'])
def create():
    print('1')
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        item = Item(title = title, price = price)
        
       # print('2')
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Получилась ошибка"
    else:
        return render_template('create.html')
	

if __name__ == "__main__":
    app.run(debug=True) #потом поменять на False 
	