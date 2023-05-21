"""
In flask_uploads.py
Change
from werkzeug import secure_filename,FileStorage
to
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
"""


"""
(venv) C:\Users\shetty\PycharmProjects\pyproject\flask_shopping>py
Python 3.9.6 (tags/v3.9.6:db3ff76, Jun 28 2021, 15:26:21) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> from market import app, db
>>> app.app_context().push()
>>> db.create_all()

>>> from market import Item
>>> item1 = Item(name='Iphone 13', barcode='123456789101', price=500, description='Iphone 13 is latest one with 4gb, 128hdd, 64 mega pixal camera')
>>> db.session.add(item1)
>>> db.session.commit()
>>> Item.query.all()
[Item Iphone 13]
>>> item2 = Item(name='Laptop', barcode='234567891011', price=600, description='Lenova Laptop with 4gb ram, 1TB sdd, 5 mega pixal camera, windows 11 os')
>>> db.session.add(item2)
>>> db.session.commit()
>>> Item.query.all()
[Item Iphone 13, Item Laptop]
>>> for item in Item.query.all():
...   item.id
...   item.name
...   item.barcode
...   item.price
...   item.description
...
1
'Iphone 13'
'123456789101'
500
'Iphone 13 is latest one with 4gb, 128hdd, 64 mega pixal camera'
2
'Laptop'
'234567891011'
600
'Lenova Laptop with 4gb ram, 1TB sdd, 5 mega pixal camera, windows 11 os'
>>> for item in Item.query.filter_by(price=500):
...   item.name
...
'Iphone 13'
>>>
"""

# ----------------------------------------------------------------------------------
"""
from market import app, db
app.app_context().push()
db.create_all()
from market.models import User, Item
u1 = User(username='a1',email='a1@gmail.com',password='root')
db.session.add(u1)
db.session.commit()
t1 = Item(name='Freeze',barcode='123451267890',price=600,description='LG freeze with 20L')
user1 = User.query.filter_by(username='a1').first()
db.session.add(t1)
db.session.commit()
item1 = Item.query.filter_by(name='Iphone').first()
item1
    Item Iphone
item1.owner
item1.owner = user1.id
db.session.add(item1)
db.session.commit()

u2 = User(username='a2',email='a2@gmail.com',password='root2')
db.session.add(u2)
db.session.commit()
user2 = User.query.filter_by(username='a2').first()

from market import app, db
app.app_context().push()
from market.models import User, Item
t1 = Item(name='Table',barcode='123852267890',price=50,description='Wooden table with smooth polish')
db.session.add(t1)
db.session.commit()
t2 = Item(name='Phone_1',barcode='789012123456',price=120,description='Redmi A1 Black, 2GB RAM, 32GB Storage')
db.session.add(t2)
db.session.commit()

t3 = Item(name='Phone_2',barcode='739025160258', price=120, description='Redmi S4 Black, 2GB RAM, 32GB Storage')
db.session.add(t3)
db.session.commit()
t4 = Item(name='Phone_3',barcode='789015946236',price=140,description='Redmi T5 Black, 3GB RAM, 62GB Storage')
db.session.add(t4)
db.session.commit()
t5 = Item(name='Phone_4',barcode='775082648526',price=100,description='Redmi A9 Black, 4GB RAM, 37GB Storage')
db.session.add(t5)
db.session.commit()

"""
"""
=============================================================================
# payment modal 1
-----------------------------------------------------------------------------
# html page

<div class="container bg-light d-md-flex align-items-center">
   <div class="card box1 shadow-sm p-md-5 p-md-5 p-4">
      <div class="fw-bolder mb-4"><span class="fas fa-dollar-sign"></span><span class="ps-1">599,00</span></div>
      <div class="d-flex flex-column">
         <div class="d-flex align-items-center justify-content-between text"> <span class="">Commission</span> <span class="fas fa-dollar-sign"><span class="ps-1">1.99</span></span> </div>
         <div class="d-flex align-items-center justify-content-between text mb-4"> <span>Total</span> <span class="fas fa-dollar-sign"><span class="ps-1">600.99</span></span> </div>
         <div class="border-bottom mb-4"></div>
         <div class="d-flex flex-column mb-4"> <span class="far fa-file-alt text"><span class="ps-2">Invoice ID:</span></span> <span class="ps-3">SN8478042099</span> </div>
         <div class="d-flex flex-column mb-5"> <span class="far fa-calendar-alt text"><span class="ps-2">Next payment:</span></span> <span class="ps-3">22 july,2018</span> </div>
         <div class="d-flex align-items-center justify-content-between text mt-5">
            <div class="d-flex flex-column text"> <span>Customer Support:</span> <span>online chat 24/7</span> </div>
            <div class="btn btn-primary rounded-circle"><span class="fas fa-comment-alt"></span></div>
         </div>
      </div>
   </div>
   <div class="card box2 shadow-sm">
      <div class="d-flex align-items-center justify-content-between p-md-5 p-4">
         <span class="h5 fw-bold m-0">Payment methods</span> 
         <div class="btn btn-primary bar"><span class="fas fa-bars"></span></div>
      </div>
      <ul class="nav nav-tabs mb-3 px-md-4 px-2">
         <li class="nav-item"> <a class="nav-link px-2 active" aria-current="page" href="#">Credit Card</a> </li>
         <li class="nav-item"> <a class="nav-link px-2" href="#">Mobile Payment</a> </li>
         <li class="nav-item ms-auto"> <a class="nav-link px-2" href="#">+ More</a> </li>
      </ul>
      <div class="px-md-5 px-4 mb-4 d-flex align-items-center">
         <div class="btn btn-success me-4"><span class="fas fa-plus"></span></div>
         <div class="btn-group" role="group" aria-label="Basic radio toggle button group"> <input type="radio" class="btn-check" name="btnradio" id="btnradio1" autocomplete="off" checked> <label class="btn btn-outline-primary" for="btnradio1"><span class="pe-1">+</span>5949</label> <input type="radio" class="btn-check" name="btnradio" id="btnradio2" autocomplete="off"> <label class="btn btn-outline-primary" for="btnradio2"><span class="lpe-1">+</span>3894</label> </div>
      </div>
      <form action="">
         <div class="row">
            <div class="col-12">
               <div class="d-flex flex-column px-md-5 px-4 mb-4">
                  <span>Credit Card</span> 
                  <div class="inputWithIcon"> <input class="form-control" type="text" value="5136 1845 5468 3894"> <span class=""> <img src="https://www.freepnglogos.com/uploads/mastercard-png/mastercard-logo-logok-15.png" alt=""></span> </div>
               </div>
            </div>
            <div class="col-md-6">
               <div class="d-flex flex-column ps-md-5 px-md-0 px-4 mb-4">
                  <span>Expiration<span class="ps-1">Date</span></span> 
                  <div class="inputWithIcon"> <input type="text" class="form-control" value="05/20"> <span class="fas fa-calendar-alt"></span> </div>
               </div>
            </div>
            <div class="col-md-6">
               <div class="d-flex flex-column pe-md-5 px-md-0 px-4 mb-4">
                  <span>Code CVV</span> 
                  <div class="inputWithIcon"> <input type="password" class="form-control" value="123"> <span class="fas fa-lock"></span> </div>
               </div>
            </div>
            <div class="col-12">
               <div class="d-flex flex-column px-md-5 px-4 mb-4">
                  <span>Name</span> 
                  <div class="inputWithIcon"> <input class="form-control text-uppercase" type="text" value="valdimir berezovkiy"> <span class="far fa-user"></span> </div>
               </div>
            </div>
            <div class="col-12 px-md-5 px-4 mt-3">
               <div class="btn btn-primary w-100">Pay $599.00</div>
            </div>
         </div>
      </form>
   </div>
</div>

# css page
@import url('https://fonts.googleapis.com/css?family=Montserrat:400,700&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    list-style: none;
    font-family: 'Montserrat', sans-serif
}

body{
    background-color:#3ecc6d;
}

.container {
    margin: 20px auto;
    width: 800px;
    padding: 30px
}

.card.box1 {
    width: 350px;
    height: 500px;
    background-color: #3ecc6d;
    color: #baf0c3;
    border-radius: 0
}

.card.box2 {
    width: 450px;
    height: 580px;
    background-color: #ffffff;
    border-radius: 0
}

.text {
    font-size: 13px
}

.box2 .btn.btn-primary.bar {
    width: 20px;
    background-color: transparent;
    border: none;
    color: #3ecc6d
}

.box2 .btn.btn-primary.bar:hover {
    color: #baf0c3
}

.box1 .btn.btn-primary {
    background-color: #57c97d;
    width: 45px;
    height: 45px;
    display: flex;
    justify-content: center;
    align-items: center;
    border: 1px solid #ddd
}

.box1 .btn.btn-primary:hover {
    background-color: #f6f8f7;
    color: #57c97d
}

.btn.btn-success {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #ddd;
    color: black;
    display: flex;
    justify-content: center;
    align-items: center;
    border: none
}

.nav.nav-tabs {
    border: none;
    border-bottom: 2px solid #ddd
}

.nav.nav-tabs .nav-item .nav-link {
    border: none;
    color: black;
    border-bottom: 2px solid transparent;
    font-size: 14px
}

.nav.nav-tabs .nav-item .nav-link:hover {
    border-bottom: 2px solid #3ecc6d;
    color: #05cf48
}

.nav.nav-tabs .nav-item .nav-link.active {
    border: none;
    border-bottom: 2px solid #3ecc6d
}

.form-control {
    border: none;
    border-bottom: 1px solid #ddd;
    box-shadow: none;
    height: 20px;
    font-weight: 600;
    font-size: 14px;
    padding: 15px 0px;
    letter-spacing: 1.5px;
    border-radius: 0
}

.inputWithIcon {
    position: relative
}

img {
    width: 50px;
    height: 20px;
    object-fit: cover
}

.inputWithIcon span {
    position: absolute;
    right: 0px;
    bottom: 9px;
    color: #57c97d;
    cursor: pointer;
    transition: 0.3s;
    font-size: 14px
}

.form-control:focus {
    box-shadow: none;
    border-bottom: 1px solid #ddd
}

.btn-outline-primary {
    color: black;
    background-color: #ddd;
    border: 1px solid #ddd
}

.btn-outline-primary:hover {
    background-color: #05cf48;
    border: 1px solid #ddd
}

.btn-check:active+.btn-outline-primary,
.btn-check:checked+.btn-outline-primary,
.btn-outline-primary.active,
.btn-outline-primary.dropdown-toggle.show,
.btn-outline-primary:active {
    color: #baf0c3;
    background-color: #3ecc6d;
    box-shadow: none;
    border: 1px solid #ddd
}

.btn-group>.btn-group:not(:last-child)>.btn,
.btn-group>.btn:not(:last-child):not(.dropdown-toggle),
.btn-group>.btn-group:not(:first-child)>.btn,
.btn-group>.btn:nth-child(n+3),
.btn-group>:not(.btn-check)+.btn {
    border-radius: 50px;
    margin-right: 20px
}

form {
    font-size: 14px
}

form .btn.btn-primary {
    width: 100%;
    height: 45px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: #3ecc6d;
    border: 1px solid #ddd
}

form .btn.btn-primary:hover {
    background-color: #05cf48
}

@media (max-width:750px) {
    .container {
        padding: 10px;
        width: 100%
    }

    .text-green {
        font-size: 14px
    }

    .card.box1,
    .card.box2 {
        width: 100%
    }

    .nav.nav-tabs .nav-item .nav-link {
        font-size: 12px
    }
}

# if used as modal
{% include "includes/payment_modal.html" %}
<button class="btn btn-outline btn-success" data-toggle="modal" data-target="#paymentModal">Make Payment</button>

=============================================================================
"""
"""
=============================================================================
# payment method 2
# html page
<div class="text-right">
{% set amount = total.replace('.','') %}
<script
src="https://checkout.stripe.com/checkout.js"
class="stripe-button"
data-key="pk_test_MaILxTYQ15v5Uhd6NKI9wPdD00qdL0QZSl"
data-name="ShopRock"
data-description="Placed order bill payment"
data-amount="{{total}}"
data-currency="usd">
</script>
</div>

=============================================================================

"""

