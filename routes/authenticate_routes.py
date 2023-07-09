from flask import flash, redirect, render_template, request, Blueprint, url_for
from flask_login import LoginManager, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from models_forms import Article, User, Comment

authenticate_bp = Blueprint('authenticate', __name__)

@authenticate_bp.route('/search')
def search():
    query = request.args.get('query')
    articles = Article.query.filter(Article.title.ilike(f'%{query}%')).all()

    workout_articles = [article for article in articles if article.topic == "Workouts"]
    blog_articles = [article for article in articles if article.topic == "Blog"]

    context = {
        "workout_articles": workout_articles,
        "blog_articles": blog_articles
    }

    return render_template('search_results.html', title="Search Results", query=query, **context)

@authenticate_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('main.index'))

