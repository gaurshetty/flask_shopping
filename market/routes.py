import os
import random
import secrets
from datetime import datetime
from xhtml2pdf import pisa
from io import BytesIO, StringIO
import pdfkit
from flask import render_template, redirect, url_for, flash, request, current_app, make_response
from flask_login import login_user, logout_user, login_required, current_user
from market import app, db, photos
from market.forms import RegistrationForm, LoginForm, PurchaseForm, SellForm, DeleteForm, ItemForm, UserForm
from market.models import Item, User

invoice_num = 'SN'+str(random.randint(0,999999999999))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    purchase_form = PurchaseForm()
    if request.method == "POST":
        # purchase logic
        purchased_item = request.form.get('purchased_item')
        p_item = Item.query.filter_by(id=purchased_item).first()
        if p_item:
            p_item.owner = current_user.id
            db.session.commit()
            flash(f"Congratulation, you have purchased {p_item.name} for ${p_item.price}", "success")
            return redirect(url_for('allproducts'))
        else:
            flash(f"Unfortunately, item is unavailable! We will notify you once available.", "danger")

    searchword = request.args.get('q')
    items = Item.query.msearch(searchword, fields=['name','description']).order_by(Item.name.asc())
    return render_template('result.html', items=items, purchase_form=purchase_form)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(name=form.name.data,
                    barcode=form.barcode.data,
                    price=form.price.data,
                    description=form.description.data,
                    image=photos.save(request.files.get('image'), name=secrets.token_hex(10) + "."))
        db.session.add(item)
        db.session.commit()
        flash(f"Item {item.name} added successfully!", "info")
        return redirect(url_for('admin_item'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category='danger')
    return render_template('add_item.html', form=form)

@app.route('/admin_item', methods=['GET', 'POST'])
@login_required
def admin_item():
    # Logic for item delete
    delete_form = DeleteForm()
    if request.method == "POST":
        deleted_item = request.form.get('deleted_item')
        d_item = Item.query.filter_by(id=deleted_item).first()
        if d_item:
            db.session.delete(d_item)
            db.session.commit()
            flash(f"You have removed {d_item.name} for {d_item.price}$ from your cart", "danger")
            return redirect(url_for('admin_item'))
    # Logic for user delete
    delete_form = DeleteForm()
    if request.method == "POST":
        deleted_user = request.form.get('deleted_user')
        d_user = User.query.filter_by(id=deleted_user).first()
        if d_user:
            db.session.delete(d_user)
            db.session.commit()
            flash(f"You have removed {d_user.username} from website", "danger")
            return redirect(url_for('admin_item'))
    items = Item.query.all()
    users = User.query.all()
    return render_template('admin_item.html', items=items, users=users, delete_form=delete_form)

@app.route('/admin_update_item/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_update_item(id):
    form = ItemForm(request.form)
    item = Item.query.get_or_404(id)
    if request.method == "POST":
        item.name = form.name.data
        item.barcode = form.barcode.data
        item.price = form.price.data
        item.description = form.description.data
        item.image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + ".")
        # if request.files.get('image'):
        #     try:
        #         os.unlink(os.path.join(current_app.root_path, "static/images/" + item.image))
        #         item.image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + ".")
        #     except:
        #         item.image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + ".")
        db.session.commit()
        flash(f"Item {item.name} updated successfully", "info")
        return redirect(url_for('admin_item'))
    form.name.data = item.name
    form.barcode.data = item.barcode
    form.price.data = item.price
    form.description.data = item.description
    items = Item.query.all()
    users = User.query.all()
    return render_template('add_item.html',items=items, users=users, form=form, item=item)

@app.route('/admin_update_user/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_update_user(id):
    form = UserForm(request.form)
    user = User.query.get_or_404(id)
    print(user.__dict__)
    if request.method == "POST":
        user.username = form.username.data
        user.email = form.email.data
        user.budget = form.budget.data
        # user.image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + ".")
        if request.files.get('image'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + user.image))
                user.image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + ".")
            except:
                user.image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + ".")
        db.session.commit()
        flash(f"User {user.username} updated successfully", "info")
        return redirect(url_for('admin_item'))
    form.username.data = user.username
    form.email.data = user.email
    form.budget.data = user.budget
    form.image.data = user.image
    items = Item.query.all()
    users = User.query.all()
    return render_template('update_user.html',items=items, users=users, form=form, user=user)

@app.route('/allproducts', methods=['GET', 'POST'])
@login_required
def allproducts():
    purchase_form = PurchaseForm()
    if request.method == "POST":
        # purchase logic
        purchased_item = request.form.get('purchased_item')
        print(purchased_item)
        p_item = Item.query.filter_by(id=purchased_item).first()
        if p_item:
            p_item.owner = current_user.id
            db.session.commit()
            flash(f"Congratulation, you have purchased {p_item.name} for ${p_item.price}", "success")
            return redirect(url_for('allproducts'))
        else:
            flash(f"Unfortunately, item is unavailable! We will notify you once available.", "danger")
    page = request.args.get('page', 1, type=int)
    items = Item.query.order_by(Item.name.asc()).paginate(page=page, per_page=4)
    return render_template('allproducts.html', items=items, purchase_form=purchase_form)


@app.route('/product_detail/<int:id>', methods=['GET', 'POST'])
@login_required
def product_detail(id):
    purchase_form = PurchaseForm()
    if request.method == "POST":
        # purchase logic
        purchased_item = request.form.get('purchased_item')
        print(purchased_item)
        p_item = Item.query.filter_by(id=purchased_item).first()
        if p_item:
            p_item.owner = current_user.id
            db.session.commit()
            flash(f"Congratulation, you have purchased {p_item.name} for ${p_item.price}", "success")
            return redirect(url_for('allproducts'))
        else:
            flash(f"Unfortunately, item is unavailable! We will notify you once available.", "danger")
    item = Item.query.filter_by(id=id).first()
    return render_template('product_detail.html', item=item, purchase_form=purchase_form)


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    delete_form = DeleteForm()
    if request.method == "POST":
        deleted_item = request.form.get('deleted_item')
        d_item = Item.query.filter_by(id=deleted_item).first()
        if d_item:
            d_item.owner = None
            db.session.commit()
            flash(f"You have removed {d_item.name} for {d_item.price}$ from your cart", "danger")
            return redirect(url_for('cart'))
    owned_items = Item.query.filter_by(owner=current_user.id)
    subtotal = sum([item.price for item in owned_items])
    tax = ("%.2f" % (0.18 * float(subtotal)))
    total = ("%.2f" % (1.18 * float(subtotal)))
    return render_template('cart.html', owned_items=owned_items, delete_form=delete_form, subtotal=subtotal, tax=tax, total=total)

@app.route('/clear_cart')
@login_required
def clear_cart():
    current_user.items = []
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/invoice/', methods=['GET', 'POST'])
def invoice():
    global invoice_num
    date = datetime.now()
    owned_items = Item.query.filter_by(owner=current_user.id)
    subtotal = sum([item.price for item in owned_items])
    tax = ("%.2f" % (0.18 * float(subtotal)))
    total = ("%.2f" % (1.18 * float(subtotal)))
    return render_template('invoice.html', owned_items=owned_items, date=date, subtotal=subtotal, tax=tax, total=total, invoice_num=invoice_num)

@app.route('/get_pdf', methods=['GET', 'POST'])
def get_pdf():
    # pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    global invoice_num
    date = datetime.now()
    if current_user.is_authenticated:
        owned_items = Item.query.filter_by(owner=current_user.id)
        subtotal = sum([item.price for item in owned_items])
        tax = ("%.2f" % (0.18 * float(subtotal)))
        total = ("%.2f" % (1.18 * float(subtotal)))
        rendered = render_template('pdf.html', owned_items=owned_items, date=date, subtotal=subtotal, tax=tax, total=total, invoice_num=invoice_num)
        pdf = pdfkit.from_string(rendered, False, options={"enable-local-file-access": ""})
        response = make_response(pdf)
        response.headers['content-Type'] = 'application/pdf'
        response.headers['content-Disposition'] = 'inline; filename=invoice.pdf'
        return response
    return redirect(url_for('invoice'))

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == "POST":
        pass
    global invoice_num
    date = datetime.now()
    owned_items = Item.query.filter_by(owner=current_user.id)
    subtotal = sum([item.price for item in owned_items])
    total = ("%.2f" % (1.18 * float(subtotal)))
    commission = ("%.2f" % float(1.99))
    grandtotal = ("%.2f" % (float(commission) + float(total)))
    return render_template('payment.html', date=date, total=total, commission=commission, grandtotal=grandtotal, invoice_num=invoice_num)




@app.route('/market', methods=['GET', 'POST'])
@login_required
def market():
    purchase_form = PurchaseForm()
    sell_form = SellForm()
    if request.method == "POST":
        # purchase logic
        purchased_item = request.form.get('purchased_item')
        p_item = Item.query.filter_by(id=purchased_item).first()
        if p_item:
            if current_user.can_purchase(p_item):
                p_item.buy(current_user)
                flash(f"Congratulation, you have purchased {p_item.name} for {p_item.price}$", "success")
            else:
                flash(f"Unfortunately, you dont have enough money to purchase {p_item.name}", "danger")
        # sell item logic
        sell_item = request.form.get('sell_item')
        s_item = Item.query.filter_by(id=sell_item).first()
        if s_item:
            if current_user.can_sell(s_item):
                s_item.sell(current_user)
                flash(f"Congratulation, you have sold {s_item.name} for {s_item.price}$", "success")
            else:
                flash(f"Something went wrong while selling {s_item.name}", "danger")
        return redirect(url_for('market'))
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items,
                               sell_form=sell_form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    hash_password=form.password1.data,
                    image=photos.save(request.files.get('image'), name=secrets.token_hex(10) + "."))
        db.session.add(user)
        db.session.commit()
        flash(f"Account created successfully, for {user.username}! Login to get access.", "info")
        return redirect(url_for('login'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg[0], category='danger')
    return render_template('registration.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f'{user.username}, You logged in successfully !', category='success')
            return redirect(url_for('allproducts'))
        else:
            flash('Username and Password do not match, Please try again!', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out", category="info")
    return redirect(url_for('home'))
