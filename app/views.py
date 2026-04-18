"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from app.models import User, Profile, Interaction, Match, Message
from flask import render_template, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

###
# Helper Functions
###

def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

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
        user={"id": session.get("user_id"), "email": session.get("email")}
    ), 200

@app.route('/api/profiles', methods=['POST'])
def create_profile():
    user = get_current_user()
    if not user:
        return jsonify(error="unauthorized", message="Please log in"), 401
    if user.profile:
        return jsonify(error="conflict", message="Profile already exists"), 409
    data = request.get_json()
    if not data:
        return jsonify(error="bad_request", message="No data provided"), 400
    required = ["full_name", "age", "bio", "location", "interests"]
    for field in required:
        if not data.get(field):
            return jsonify(error="bad_request", message=f"{field} is required"), 400
    profile = Profile(
        user_id=user.id,
        full_name=data.get("full_name"),
        age=data.get("age"),
        bio=data.get("bio"),
        location=data.get("location"),
        interests=data.get("interests"),
        custom_field_1=data.get("custom_field_1"),
        custom_field_2=data.get("custom_field_2"),
        visibility=data.get("visibility", "public"),
        preferred_age_min=data.get("preferred_age_min"),
        preferred_age_max=data.get("preferred_age_max"),
        preferred_location=data.get("preferred_location"),
        preferred_radius=data.get("preferred_radius")
    )
    db.session.add(profile)
    db.session.commit()
    return jsonify(message="Profile created successfully", profile_id=profile.id), 201


@app.route('/api/profiles/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    user = get_current_user()
    if not user:
        return jsonify(error="unauthorized", message="Please log in"), 401
    profile = Profile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify(error="not_found", message="Profile not found"), 404
    if profile.visibility == "private" and profile.user_id != user.id:
        return jsonify(error="forbidden", message="This profile is private"), 403
    return jsonify(
        id=profile.id,
        user_id=profile.user_id,
        full_name=profile.full_name,
        age=profile.age,
        bio=profile.bio,
        location=profile.location,
        interests=profile.interests,
        custom_field_1=profile.custom_field_1,
        custom_field_2=profile.custom_field_2,
        profile_picture=profile.profile_picture,
        visibility=profile.visibility,
        preferred_age_min=profile.preferred_age_min,
        preferred_age_max=profile.preferred_age_max,
        preferred_location=profile.preferred_location,
        preferred_radius=profile.preferred_radius,
        created_at=profile.created_at.isoformat()
    ), 200


@app.route('/api/profiles/<int:user_id>', methods=['PUT'])
def edit_profile(user_id):
    user = get_current_user()
    if not user:
        return jsonify(error="unauthorized", message="Please log in"), 401
    if user.id != user_id:
        return jsonify(error="forbidden", message="You can only edit your own profile"), 403
    profile = Profile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify(error="not_found", message="Profile not found"), 404
    data = request.get_json()
    if not data:
        return jsonify(error="bad_request", message="No data provided"), 400
    if "full_name" in data:
        profile.full_name = data["full_name"]
    if "age" in data:
        profile.age = data["age"]
    if "bio" in data:
        profile.bio = data["bio"]
    if "location" in data:
        profile.location = data["location"]
    if "interests" in data:
        profile.interests = data["interests"]
    if "custom_field_1" in data:
        profile.custom_field_1 = data["custom_field_1"]
    if "custom_field_2" in data:
        profile.custom_field_2 = data["custom_field_2"]
    if "visibility" in data:
        profile.visibility = data["visibility"]
    if "preferred_age_min" in data:
        profile.preferred_age_min = data["preferred_age_min"]
    if "preferred_age_max" in data:
        profile.preferred_age_max = data["preferred_age_max"]
    if "preferred_location" in data:
        profile.preferred_location = data["preferred_location"]
    if "preferred_radius" in data:
        profile.preferred_radius = data["preferred_radius"]
    db.session.commit()
    return jsonify(message="Profile updated successfully"), 200


@app.route('/api/profiles/<int:user_id>/photo', methods=['POST'])
def upload_photo(user_id):
    user = get_current_user()
    if not user:
        return jsonify(error="unauthorized", message="Please log in"), 401
    if user.id != user_id:
        return jsonify(error="forbidden", message="You can only upload your own photo"), 403
    profile = Profile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify(error="not_found", message="Profile not found"), 404
    if 'photo' not in request.files:
        return jsonify(error="bad_request", message="No photo provided"), 400
    file = request.files['photo']
    if file.filename == '':
        return jsonify(error="bad_request", message="No file selected"), 400
    if not allowed_file(file.filename):
        return jsonify(error="bad_request", message="File type not allowed. Use png, jpg, jpeg or gif"), 400
    filename = secure_filename(f"user_{user_id}_{file.filename}")
    upload_folder = os.path.join(app.root_path, '..', 'public', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    file.save(os.path.join(upload_folder, filename))
    profile.profile_picture = filename
    db.session.commit()
    return jsonify(message="Photo uploaded successfully", filename=filename), 200


@app.route('/api/discover', methods=['GET'])
def discover():
    user = get_current_user()
    if not user:
        return jsonify(error="unauthorized", message="Please log in"), 401
    if not user.profile:
        return jsonify(error="bad_request", message="You need a profile first"), 400
    already_seen = db.session.query(Interaction.to_user_id).filter_by(
        from_user_id=user.id
    ).subquery()
    profiles = Profile.query.filter(
        Profile.user_id != user.id,
        Profile.visibility == "public",
        ~Profile.user_id.in_(already_seen)
    ).all()
    result = []
    for profile in profiles:
        score = calculate_match_score(user.profile, profile)
        result.append({
            "user_id": profile.user_id,
            "full_name": profile.full_name,
            "age": profile.age,
            "bio": profile.bio,
            "location": profile.location,
            "interests": profile.interests,
            "profile_picture": profile.profile_picture,
            "match_score": score
        })
    result.sort(key=lambda x: x["match_score"], reverse=True)
    return jsonify(profiles=result), 200


def calculate_match_score(my_profile, other_profile):
    score = 0
    my_interests = set(i.strip().lower() for i in my_profile.interests.split(","))
    other_interests = set(i.strip().lower() for i in other_profile.interests.split(","))
    shared = my_interests & other_interests
    if my_interests:
        score += (len(shared) / len(my_interests)) * 50
    if my_profile.preferred_age_min and my_profile.preferred_age_max:
        if my_profile.preferred_age_min <= other_profile.age <= my_profile.preferred_age_max:
            score += 30
    if my_profile.preferred_location:
        if my_profile.preferred_location.lower() in other_profile.location.lower():
            score += 20
    return round(score, 1)


@app.route('/api/profiles/<int:user_id>/like', methods=['POST'])
def like_user(user_id):
    user = get_current_user()
    if not user:
        return jsonify(error="unauthorized", message="Please log in"), 401
    if user.id == user_id:
        return jsonify(error="bad_request", message="You cannot like yourself"), 400
    target = User.query.get(user_id)
    if not target:
        return jsonify(error="not_found", message="User not found"), 404
    existing = Interaction.query.filter_by(
        from_user_id=user.id,
        to_user_id=user_id
    ).first()
    if existing:
        return jsonify(error="conflict", message="Already interacted with this user"), 409
    interaction = Interaction(
        from_user_id=user.id,
        to_user_id=user_id,
        action="like"
    )
    db.session.add(interaction)
    mutual = Interaction.query.filter_by(
        from_user_id=user_id,
        to_user_id=user.id,
        action="like"
    ).first()
    matched = False
    if mutual:
        match = Match(
            user1_id=min(user.id, user_id),
            user2_id=max(user.id, user_id)
        )
        db.session.add(match)
        matched = True
    db.session.commit()
    if matched:
        return jsonify(message="It's a match!", matched=True), 200
    return jsonify(message="Like recorded", matched=False), 200


@app.route('/api/profiles/<int:user_id>/pass', methods=['POST'])
def pass_user(user_id):
    user = get_current_user()
    if not user:
        return jsonify(error="unauthorized", message="Please log in"), 401
    if user.id == user_id:
        return jsonify(error="bad_request", message="Invalid action"), 400
    existing = Interaction.query.filter_by(
        from_user_id=user.id,
        to_user_id=user_id
    ).first()
    if existing:
        return jsonify(error="conflict", message="Already interacted with this user"), 409
    interaction = Interaction(
        from_user_id=user.id,
        to_user_id=user_id,
        action="pass"
    )
    db.session.add(interaction)
    db.session.commit()
    return jsonify(message="Passed"), 200


@app.route('/api/matches', methods=['GET'])
def get_matches():
    user = get_current_user()
    if not user:
        return jsonify(error="unauthorized", message="Please log in"), 401
    matches = Match.query.filter(
        (Match.user1_id == user.id) | (Match.user2_id == user.id)
    ).all()
    result = []
    for match in matches:
        other_id = match.user2_id if match.user1_id == user.id else match.user1_id
        other_profile = Profile.query.filter_by(user_id=other_id).first()
        if other_profile:
            result.append({
                "match_id": match.id,
                "user_id": other_id,
                "full_name": other_profile.full_name,
                "age": other_profile.age,
                "bio": other_profile.bio,
                "profile_picture": other_profile.profile_picture,
                "matched_at": match.created_at.isoformat()
            })
    return jsonify(matches=result), 200


@app.route('/api/messages', methods=['POST'])
def send_message():
    user = get_current_user()
    if not user:
        return jsonify(error="unauthorized", message="Please log in"), 401
    data = request.get_json()
    if not data:
        return jsonify(error="bad_request", message="No data provided"), 400
    receiver_id = data.get("receiver_id")
    content = data.get("content", "").strip()
    if not receiver_id or not content:
        return jsonify(error="bad_request", message="receiver_id and content are required"), 400
    match = Match.query.filter(
        ((Match.user1_id == user.id) & (Match.user2_id == receiver_id)) |
        ((Match.user1_id == receiver_id) & (Match.user2_id == user.id))
    ).first()
    if not match:
        return jsonify(error="forbidden", message="You can only message users you matched with"), 403
    message = Message(
        match_id=match.id,
        sender_id=user.id,
        receiver_id=receiver_id,
        content=content
    )
    db.session.add(message)
    db.session.commit()
    return jsonify(message="Message sent", message_id=message.id), 201


@app.route('/api/matches/<int:match_id>/messages', methods=['GET'])
def get_messages(match_id):
    user = get_current_user()
    if not user:
        return jsonify(error="unauthorized", message="Please log in"), 401
    match = Match.query.get(match_id)
    if not match:
        return jsonify(error="not_found", message="Match not found"), 404
    if user.id not in [match.user1_id, match.user2_id]:
        return jsonify(error="forbidden", message="You are not part of this match"), 403
    messages = Message.query.filter_by(match_id=match_id).order_by(Message.created_at.asc()).all()
    result = [{
        "id": m.id,
        "sender_id": m.sender_id,
        "receiver_id": m.receiver_id,
        "content": m.content,
        "created_at": m.created_at.isoformat()
    } for m in messages]
    return jsonify(messages=result), 200


@app.route('/api/search', methods=['GET'])
def search_profiles():
    user = get_current_user()
    if not user:
        return jsonify(error="unauthorized", message="Please log in"), 401
    location = request.args.get("location", "").strip()
    age_min = request.args.get("age_min", type=int)
    age_max = request.args.get("age_max", type=int)
    interests = request.args.get("interests", "").strip()
    query = Profile.query.filter(
        Profile.user_id != user.id,
        Profile.visibility == "public"
    )
    if location:
        query = query.filter(Profile.location.ilike(f"%{location}%"))
    if age_min:
        query = query.filter(Profile.age >= age_min)
    if age_max:
        query = query.filter(Profile.age <= age_max)
    if interests:
        query = query.filter(Profile.interests.ilike(f"%{interests}%"))
    profiles = query.all()
    result = [{
        "user_id": p.user_id,
        "full_name": p.full_name,
        "age": p.age,
        "location": p.location,
        "interests": p.interests,
        "profile_picture": p.profile_picture,
        "bio": p.bio
    } for p in profiles]
    return jsonify(profiles=result), 200


###
# The functions below should be applicable to all Flask apps.
###

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