from flask import Flask, render_template, redirect, url_for, request, flash
from flask_security import Security, login_required, roles_accepted, roles_required
from flask_migrate import Migrate, upgrade
from models import db, seed_data, Employee, user_seed_data, user_datastore, EmployeePicture
from dotenv import load_dotenv
import os
from sqlalchemy import or_

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('LOCAL_DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT')
app.config["SQLALCHEMY_TRACK_MODIFACTION"] = False

db.init_app(app)

migrate = Migrate(app, db)
security = Security(app, user_datastore)

# ----------------------------------------------------------------------

@app.route("/")
def home_page():
    return render_template("index.html")

# -------------------------------users----------------------------------

@app.route("/users", methods=["GET", "POST"])
@login_required
def users():

    search_query = request.args.get('q', '')
    sort_column = request.args.get('sort_column', 'id')
    sort_order = request.args.get('sort_order', 'asc')
    page = request.args.get('page', 1, type=int)

    users_query = Employee.query
    if search_query:
        users_query = users_query.filter(
            or_(
                Employee.name == search_query,
                Employee.email == search_query,
                Employee.phone == search_query,
                Employee.age == search_query,
                Employee.street_name == search_query,
                Employee.street_number == search_query,
                Employee.postcode == search_query,
                Employee.city == search_query,
                Employee.state == search_query,
                Employee.country == search_query
            )
        )

    if sort_column == 'name':
        sort_by = Employee.name
    elif sort_column == 'email':
        sort_by = Employee.email
    elif sort_column == 'phone':
        sort_by = Employee.phone
    elif sort_column == 'age':
        sort_by = Employee.age
    elif sort_column == 'street_name':
        sort_by = Employee.street_name
    elif sort_column == 'postcode':
        sort_by = Employee.postcode
    elif sort_column == 'city':
        sort_by = Employee.city
    elif sort_column == 'state':
        sort_by = Employee.state
    elif sort_column == 'country':
        sort_by = Employee.country
    else:
        sort_by = Employee.id

    if sort_order == 'asc':
        sort_by = sort_by.asc()
    elif sort_order == 'desc':
        sort_by = sort_by.desc()

    users_query = users_query.order_by(sort_by)

    pagination_obj = users_query.paginate(
        page=page, per_page=10, error_out=True)

    if request.method == "POST":
        user_id = request.form.get('user_id', type=int)
        return redirect(url_for('user_page', user_id=user_id))

    users_list = pagination_obj.items
    for user in users_list:
        last_picture = EmployeePicture.query.filter_by(
            employee_id=user.id).order_by(EmployeePicture.id.desc()).first()
        user.picture = last_picture.picture

    return render_template(
        'users.html',
        users_list=users_list,
        search_query=search_query,
        sort_order=sort_order,
        sort_column=sort_column,
        pagination=pagination_obj,
        current_page=page,
        num_pages=pagination_obj.pages,
        has_next_page=pagination_obj.has_next,
        has_prev_page=pagination_obj.has_prev
    )

# --------------------------create user-------------------------------

@app.route("/create_user", methods=["GET", "POST"])
@login_required
def create_user():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        age = request.form.get('age', type=int)
        street_name = request.form.get('street_name')
        street_number = request.form.get('street_number')
        postcode = request.form.get('postcode')
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')

        email_exist = Employee.query.filter_by(email=email).first()
        username_exist = Employee.query.filter_by(name=name).first()

        if email_exist or username_exist:
            flash('Username or email already exist!')
        else:
            new_user = Employee(name=name, email=email, phone=phone,
                                age=age, street_name=street_name, street_number=street_number, postcode=postcode, city=city, state=state, country=country)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('user_page', user_id=new_user.id))

    return render_template('create_user.html')

# -----------------------------user page--------------------------------

@app.route("/user/<int:user_id>", methods=["GET", "POST"])
@login_required
def user_page(user_id):
    user_info_by_id = Employee.query.get(user_id)
    if request.method == "POST":
        user_info_by_id.name = request.form['name']
        user_info_by_id.email = request.form['email']
        user_info_by_id.phone = request.form['phone']
        user_info_by_id.age = request.form['age']
        user_info_by_id.street_name = request.form['street_name']
        user_info_by_id.street_number = request.form['street_number']
        user_info_by_id.postcode = request.form['postcode']
        user_info_by_id.city = request.form['city']
        user_info_by_id.state = request.form['state']
        user_info_by_id.country = request.form['country']

        try:
            db.session.commit()
        except Exception as e:
            flash(f'Error updating user information: {str(e)}')
            db.session.rollback()
    return render_template('user_page.html', user_info=user_info_by_id)

# -----------------------------logIn/LogOut--------------------------------

@app.route("/logout")
def logout():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("index.html")



if __name__ == "__main__":
    with app.app_context():
        upgrade()
        seed_data(db)
        user_seed_data()
    app.run(port=4500)