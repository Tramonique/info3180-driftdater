"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from app.models import User
from flask import render_template, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify(message="Backend is working"), 200


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        return jsonify(error="bad_request", message="No data provided"), 400

    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    if not email or not password:
        return jsonify(error="bad_request", message="Email and password are required"), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify(error="conflict", message="Email already exists"), 409

    password_hash = generate_password_hash(password)

    new_user = User(email=email, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(message="User registered successfully"), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify(error="bad_request", message="No data provided"), 400

    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    if not email or not password:
        return jsonify(error="bad_request", message="Email and password are required"), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify(error="unauthorized", message="Invalid email or password"), 401

    session["user_id"] = user.id
    session["email"] = user.email

    return jsonify(message="Login successful", user={"id": user.id, "email": user.email}), 200


@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify(message="Logout successful"), 200


@app.route('/api/check-auth', methods=['GET'])
def check_auth():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify(authenticated=False), 200

    return jsonify(
        authenticated=True,
        user={
            "id": session.get("user_id"),
            "email": session.get("email")
        }
    ), 200

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404