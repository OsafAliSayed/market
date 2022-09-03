# Handling Routes here
from sqlalchemy.sql.elements import Null
from werkzeug.datastructures import cache_property
from market import app, db
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user, logout_user, login_required, current_user
# Handling Homepage Route


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')

# Handling marketpage Route


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    
    #Creating purchasing and selling forms
    purchase_form = PurchaseItemForm()
    sell_form = SellItemForm()

    if request.method == "POST":
        #Query for purchasing items 
        purchased_item = request.form.get("purchased_item")
        p_item = Item.query.filter_by(name=purchased_item).first()
        if p_item:
            if p_item.price <= current_user.budget:
                p_item.owner = current_user.id
                current_user.budget = current_user.budget - p_item.price
                db.session.commit()
                flash(f"You have purchased {p_item.name}", category = "success")
            else:
                flash(f"Insufficient Funds!", category="danger")
            
        #Query for selling items
        sold_item = request.form.get("sold_item")
        s_item = Item.query.filter_by(name=sold_item).first()
        if s_item:
            s_item.owner = None
            current_user.budget += s_item.price
            db.session.commit()
            flash(f"You have sold {s_item.name} for {s_item.price}$", category="info")
        
        #In any case of post method I wish to return to market page 
        return redirect(url_for("market_page"))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, owned_items=owned_items, purchase_form=purchase_form, sell_form=sell_form)

# Handling registerpage Route


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        # Logging in new user
        login_user(user_to_create)
        flash(f'Your account was created successfully! You are now logged in as {user_to_create.username}', category='success')
        
        return redirect(url_for('market_page'))

    if form.errors.values():
        for error in form.errors.values():
            flash(
                f'There was an error creating a user: {error}', category='danger')

    return render_template('register.html', form=form)


# Handling loginpage Route
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash('You have logged in successfully', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username or password did not match', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have successfully logged out ', category='success')
    return redirect(url_for('home_page'))

