from flask import flash, request, render_template, redirect, Blueprint, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from models_forms import User, Article, Comment, CommentForm
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename, send_from_directory
import app
from flask_login import current_user, login_required, login_user
from models_forms import db
import re
import os

main_bp = Blueprint('main', __name__)


@main_bp.route('/about')
def about():
    return render_template('about.html', title="The Fit Physicist-About")

@main_bp.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        sender = request.form.get('name')
        email = request.form.get('email')
        title = request.form.get('title')
        message = request.form.get('message')
        priority = request.form.get('priority')
            
        msg = Message(title, sender=email, recipients=['clombar1@email.essex.edu'])
        msg.body = f"Name: {sender}\nEmail: {email}\n\n{message}"
        mail.send(msg)

        return 'Email sent!'
    
    return render_template('contact.html')

@main_bp.route('/all_workout_articles')
def all_workout_articles():
    workout_articles = Article.query.filter(Article.topic == "Workouts").all()
    comment_form = CommentForm()
    return render_template('all_workout_articles.html', title="All Workout Articles", workout_articles=workout_articles, comment_form=comment_form)


@main_bp.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.json.get('action')
        if action == 'register':
            # Registration logic
            username = request.json.get('username')
            first_name = request.json.get('first_name')
            last_name = request.json.get('last_name')
            email = request.json.get('email')
            password = request.json.get('password')

            # Validate form values
            if not username or not first_name or not last_name or not email or not password:
                return jsonify(message="Please fill in all fields"), 400

            # Check if username or email already exists
            username_exists = User.query.filter_by(username=username).first()
            if username_exists:
                return jsonify(message="This username already exists"), 400

            email_exists = User.query.filter_by(email=email).first()
            if email_exists:
                return jsonify(message="This email is already registered"), 400
            
            if len(password) < 8:
                return jsonify(message="Password must be at least 8 characters!"), 400
            
            special_characters = ['!', '@', '$', '%', '^', '&', '*', '(', ')', '?', '/', '~', '`']
            if not any(char in special_characters for char in password):
                return jsonify(message="Password must contain special characters!"), 400
            
            if not any(char.isdigit() for char in password):
                return jsonify(message="Password must contain at least one number!"), 400
            
            email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(email_regex, email):
                return jsonify(message="Invalid email address"), 400


            # Create a new user
            password_hash = generate_password_hash(password)
            new_user = User(username=username, first_name=first_name, last_name=last_name, email=email, password_hash=password_hash)
            db.session.add(new_user)
            db.session.commit()

            return jsonify(message="Sign up successful")

        elif action == 'login':
   
            if current_user.is_authenticated:
                return jsonify(message="Another user is already logged in"), 400

   
            username = request.json.get('username')
            password = request.json.get('password')

            print(f"Received username: {username}")
            print(f"Received password: {password}")

            user = User.query.filter_by(username=username).first()

            if not user or not check_password_hash(user.password_hash, password):
                flash("Incorrect login information! Try again")
                return jsonify(message="Login failed")

            login_user(user)
            flash(f"Hello {username}, Welcome to the Fit Physicist!")
            return jsonify(message='Logging you In')
                
    
    articles = Article.query.all()
    context = {
        "articles": articles
    }

    return render_template('index.html', title='The Fit Physicist', **context)

@main_bp.route('/all_articles')
@login_required
def all_articles():
    articles = Article.query.all()
    articles = [article for article in articles if article.topic == "Blog"]
    comment_form = CommentForm()

    return render_template('new.html', title="All Articles", articles=articles, comment_form=comment_form)

@main_bp.route('/article')
def article():
    
    article_previews = [
        { 
            'title': 'Calisthenics Primer',
            'description': "A beginner's intro to calisthenics, with workout plans and other advice",
            'image': 'https://www.dmarge.com/wp-content/uploads/2022/01/most-difficult-handstand-1200x800.jpg',
            'url': url_for('article.calisthentics_primer'),
        },
        {
            'title': 'Basic Nutrition Advice',
            'description': "This is a good starting point for those just starting to track their diets",
            'image': 'http://worldonline.media.clients.ellingtoncms.com/img/croppedphotos/2017/02/27/healthy-diet_t640.jpg?a6ea3ebd4438a44b86d2e9c39ecf7613005fe067',
            'url': url_for('article.nutrition_advice'),
        },
        {
            'title': 'Cardio Workouts',
            'description': 'Various workouts based on circuit-style, designed for maximum calorie burn',
            'image': 'https://www.shape.com/thmb/qr6AnPByfid8VTqqv9nrKgJOUr0=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/best-cardio-exercises-promo-2000-498cbfb8f07541b78572bf810e7fb600.jpg',
            'url': url_for('article.cardio_article')
        },
        {
            'title': 'Deadlift Basics',
            'description': 'This article provides the basic setup and techniques of the deaflift movement',
            'image': 'https://www.americanfootballinternational.com/wp-content/uploads/Barbend-2021-Deadlift-620x400.png',
            'url': url_for('article.single_article', article_id=14)
        },
        {
            'title': 'Supplementation',
            'description': 'My personal experience with supplements and discussion of my favorite brands',
            'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSbwctv2YulNCDZ5JTwRK9ry8yz-D1cY-GU1Q&usqp=CAU',
            'url': url_for('article.supplements'),
        },
        {
            'title': 'Recovery',
            'description': 'Various techniques to enhance and facilitate recovery from strenous exercise',
            'image': 'https://images.pexels.com/photos/3076509/pexels-photo-3076509.jpeg?auto=compress&cs=tinysrgb&w=600',
            'url': url_for('article.cardio_article')
        }
    ]

    return render_template('article.html', title="Articles", articles=article_previews)

@main_bp.route('/contribute', methods=["GET", "POST"])
@login_required
def contribute():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        user_id = current_user.id
        author = current_user.username
        image = request.files['image'] 
        topic = request.form.get('topic')

        title_exists = Article.query.filter_by(title=title).first()
        if title_exists:
            flash("This article already exists. Please choose a new title.")
            return redirect(url_for('main.contribute'))
                
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(request.app.config['UPLOAD_FOLDER'], filename))
            new_article = Article(title=title, content=content, user_id=user_id, author=author, image=filename, topic=topic)
        else:
            new_article = Article(title=title, content=content, user_id=user_id, author=author, image=None, topic=topic)
               
        
        db.session.add(new_article)
        db.session.commit()

        flash("Thanks for sharing with us!\nYour article will be reviewed")
        return redirect(url_for('main.index'))
        
    return render_template('contribute.html', title="The Fit Physicist-Contribute")