from flask import Blueprint, render_template, request, redirect, url_for, flash
from baseball_api.forms import UserLoginForm
from baseball_api.models import db, User, check_password_hash
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')


# This route is setting up the route to the Sign Up page
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email, password)
        new_user = User(email, password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Welcome to the Big Leagues: {email}', 'create-success')

        


        return redirect(url_for('auth.signin'))

    return render_template('signup.html', form = form)



# This route is setting up the route to the Sign In Page
@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email, password)
        logged_user = User.query.filter(User.email == email).first()


        # This is checking to see if the password given is the correct password
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            flash(f'Successfully logged in as: {email}', 'auth-success')
            return redirect(url_for('site.home'))
        else:
            flash(f'Incorrect Email/Password. Please try again', 'auth-fail')
            return redirect(url_for('auth.signin'))

    return render_template('signin.html', form = form)





# This route is setting up the logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f'Successfully logged out', 'auth-success')
    return redirect(url_for('site.home'))