from flask import Blueprint, render_template, url_for, flash

from src.authentication import user_details
from src.database.models.users import User

home_route = Blueprint('home', __name__)


@home_route.get("/")
@user_details
async def get_home(user: User | None):
    social_url = url_for('home.get_home', _external=True)
    context = dict(user=user, social_url=social_url)
    return render_template('index.html', **context)


@home_route.get("/about")
@user_details
async def get_about(user: User | None):
    social_url = url_for('home.get_home', _external=True)
    context = dict(user=user, social_url=social_url)
    return render_template('about.html', **context)


@home_route.get("/contact")
@user_details
async def get_contact(user: User | None):
    social_url = url_for('home.get_home', _external=True)
    context = dict(user=user, social_url=social_url)
    return render_template('contact.html', **context)


@home_route.post("/contact")
@user_details
async def send_contact(user: User | None):
    flash(message="Message successfully sent we will get back to you as soon as possible", category="success")
    social_url = url_for('home.get_home', _external=True)
    context = dict(user=user, social_url=social_url)
    return render_template('contact.html', **context)

