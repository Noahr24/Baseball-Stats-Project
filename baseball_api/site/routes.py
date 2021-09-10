from flask import Blueprint, render_template
from flask_login import login_required

site = Blueprint('site', __name__, template_folder='site_templates')


# Route for Profile
@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


# Route for Home Page
@site.route('/')
def home():
    return render_template('index.html')