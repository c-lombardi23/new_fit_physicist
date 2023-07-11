from flask import flash, redirect, render_template, request, Blueprint, url_for, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
from models_forms import Comment, CommentForm, Article, User
from werkzeug.utils import secure_filename, send_from_directory
from models_forms import db
from datetime import datetime
import os
from routes.uploads_routes import uploads_bp

article_bp = Blueprint('article', __name__)

article_bp.register_blueprint(uploads_bp)


@article_bp.route('/submit_comment/<int:article_id>', methods=["POST"])
def submit_comment(article_id):
    article = Article.query.get_or_404(article_id)
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        comment = Comment(
            text=comment_form.content.data,
            user_id=current_user.id,
            created_on = datetime.now(),
            article_id=article.id,
        )
        db.session.add(comment)
        db.session.commit()
        flash("Comment submitted successfully!")
        return redirect(url_for('article.single_article', article_id=article_id))

    return render_template('article.html', comment_form=comment_form, article=article)

@article_bp.route('/articles', methods=['GET', 'POST'])
@login_required
def view_article():
    articles = Article.query.all()
    not_authenticated = [article for article in articles if not article.is_authenticated]

    if current_user.username != 'Chrisl2324':
        flash('You are not authorized to view this article.', 'error')
        return redirect(url_for('main.index'))

    return render_template('view_article.html', not_authenticated=not_authenticated)

@article_bp.route('/articles/authenticate', methods=['POST'])
@login_required
def authenticate_article():
    article_id = request.form.get('article_id')
    article = Article.query.get_or_404(article_id)

    if current_user.username == 'Chrisl2324':
        article.is_authenticated = True
        db.session.commit()
        flash('Article authenticated successfully.', 'success')
    else:
        flash('You are not authorized to authenticate this article.', 'error')

    return redirect(url_for('article.view_article'))

@article_bp.route('/view_all')
def view_all():
    articles=Article.query.all()
    articles = [article for article in articles if article.is_authenticated]
    comment_form = CommentForm()
    return render_template('new.html', articles=articles, comment_form=comment_form)


@article_bp.route('/cardio_workouts')
def cardio_article():
    return render_template('cardio_workouts.html', title="Cardio Workouts")

@article_bp.route('/calisthenics_primer')
def calisthentics_primer():
    return render_template('calisthenics_primer.html', title="Calisthenics Primer")

@article_bp.route('/supplements')
def supplements():
    return render_template('supplements.html', title='The Fit Physicist-Supplements')

@article_bp.route('/nutrition_advice')
def nutrition_advice():
    return render_template('nutrition_advice.html', title="Nutrition Advice")

@article_bp.errorhandler(401)
def unauthorized_error(error):
    return render_template('error.html', error_code=401, error_message="Please Log in to View this Page"), 401


@article_bp.route('/single_article/<int:article_id>')
def single_article(article_id):
    article = Article.query.get_or_404(article_id)
    comments = Comment.query.filter_by(article_id=article_id).all()
    return render_template('single_article.html', title="The Fit Physicist", article=article, comments=comments)


@article_bp.route('/delete_comment/<int:comment_id>', methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    # Check if the current user is the owner of the comment
    if comment.user_id == current_user.id or current_user.id == 1:
        db.session.delete(comment)
        db.session.commit()
        flash("Comment deleted successfully!")
    else:
        flash("You are not authorized to delete this comment.")

    # Redirect back to the article page or wherever you want to go after deletion
    return redirect(url_for('article.single_article', title="Delete Comment", article_id=comment.article_id))

@article_bp.route('/delete/<int:id>/', methods=['GET', 'POST'])
@login_required
def delete(id):
    article_to_delete = Article.query.get_or_404(id)

    if current_user.username == article_to_delete.author:
        if request.method == 'GET':
            return render_template('confirm_delete.html', article=article_to_delete)
        
        Comment.query.filter_by(article_id=id).delete()
        db.session.delete(article_to_delete)
        db.session.commit()
        flash("Your article has been deleted")
        return redirect(url_for('main.index'))
    
    flash('You are not authorized to delete this article!')
    return redirect(url_for('main.index'))

@article_bp.route('/edit/<int:id>', methods=["GET", "POST"])
@login_required
def edit(id):
    article_edit = Article.query.get_or_404(id)

    if current_user.username == article_edit.author:
        if request.method == 'POST':
            new_title = request.form.get('title')
            new_content = request.form.get('content')
            new_image = request.files['image']
            new_topic = request.form.get('topic')

            if new_title and new_content and new_topic:  # Ensure the new title is not empty
                article_edit.title = new_title
                article_edit.content = new_content
                article_edit.topic = new_topic

            if new_image:
                if article_edit.image:
                    # Remove the existing image file from the file system
                    old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], article_edit.image)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)

                # Save the new image file to the file system
                filename = secure_filename(new_image.filename)
                new_image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                article_edit.image = filename
                

            db.session.commit()

            flash("Your changes have been saved")
            return redirect(url_for('main.all_articles'))

        return render_template('edit.html', title='Edit Your Article', article=article_edit)
    
    flash("You cannot edit another user's article!")
    return render_template('index.html', title='The Fit Physicist')