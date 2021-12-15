from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
# from forms import LoginForm, RegisterForm, AddProduct
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import stripe

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Products(db.Model):
    __tablename__ = 'Products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.Text(900), nullable=False)
    price = db.Column(db.String(10), nullable=False)
# db.create_all()


class Users(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(700), nullable=False)
    cart = db.Column(db.String(10), nullable=False)
# db.create_all()


stripe.api_key = ''


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    price = request.form['price'] + '00'
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Nike shoes',
                },
                'unit_amount': price,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:5000/success',
        cancel_url='http://localhost:5000/cancel',

    )

    return redirect(session.url, code=303)


@app.route('/')
def home():
    products = Products.query.all()
    return render_template('index.html', products=products, current_user=current_user)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        if Users.query.filter_by(email=form.email.data).first():
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        password = form.password.data
        password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        newuser = Users(username=form.name.data, email=form.email.data, password=password, cart=' ')
        db.session.add(newuser)
        db.session.commit()
        login_user(newuser)
        return redirect('/')
    return render_template('register.html', form=form, current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('Password incorrect, please try again.')
        else:
            flash("That email does not exist, please try again.")

    return render_template('login.html', form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    form = AddProduct()
    if form.validate_on_submit():
        new = Products(name=form.name.data, img_url=form.img_url.data, price=form.price.data)
        db.session.add(new)
        db.session.commit()
        return redirect('/')
    return render_template('add.html', form=form)


@app.route('/addtocart/<id>')
def add_to_cart(id):
    prod = id
    user = Users.query.filter_by(email=current_user.email).first()
    user.cart += str(prod) + ' '
    db.session.commit()
    return redirect(url_for('mycart'))


@app.route('/delete/<id>')
def remove_from_cart(id):
    prod = id
    user = Users.query.filter_by(email=current_user.email).first()
    cart = user.cart.split(' ')
    cart = [x for x in cart if x != str(prod)]
    cart = ' '.join(cart)
    user.cart = cart
    db.session.commit()
    return redirect(url_for('mycart'))


@app.route('/mycart')
def mycart():
    cart = Users.query.filter_by(email=current_user.email).first().cart
    cart = cart.split(' ')
    prods = Products.query.all()
    cart = [int(x) for x in cart if x.isnumeric()]
    price = [int(x.price.replace('$', '')) for x in prods if int(x.id) in cart]
    total = sum(price)
    cart = set(cart)
    return render_template('mycart.html', current_user=current_user, items=cart, prods=prods, total=total)


@app.route('/success')
def success():
    user = Users.query.filter_by(email=current_user.email).first()
    user.cart = ' '
    db.session.commit()
    return render_template('success.html')


@app.route('/cancel')
def cancel():
    return render_template('cancel.html')

if __name__ == '__main__':
    app.run(debug=True)