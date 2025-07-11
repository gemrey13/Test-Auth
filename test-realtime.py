from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///realtime.db'
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")

connected_users = {}


# ---------------- Models ---------------- #

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref="posts")


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="likes")
    post = db.relationship("Post", backref="likes")


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    recipient = db.relationship("User", backref="notifications")


# ---------------- Routes ---------------- #

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    user = User(username=data["username"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created", "user_id": user.id})


@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json()
    post = Post(content=data["content"], user_id=data["user_id"])
    db.session.add(post)
    db.session.commit()
    return jsonify({"message": "Post created", "post_id": post.id})


@app.route("/posts", methods=["GET"])
def get_posts():
    posts = Post.query.all()
    results = []
    for post in posts:
        results.append({
            "id": post.id,
            "content": post.content,
            "author": post.user.username,
            "likes": len(post.likes)
        })
    return jsonify(results)


@app.route("/like", methods=["POST"])
def like_post():
    data = request.get_json()
    liker_id = data["liker_id"]
    post_id = data["post_id"]

    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    existing_like = Like.query.filter_by(user_id=liker_id, post_id=post_id).first()
    if existing_like:
        return jsonify({"message": "Already liked"}), 400

    like = Like(user_id=liker_id, post_id=post_id)
    db.session.add(like)

    if liker_id != post.user_id:
        message = f"User {liker_id} liked your post."
        notification = Notification(recipient_id=post.user_id, message=message)
        db.session.add(notification)

        recipient_sid = connected_users.get(str(post.user_id))
        if recipient_sid:
            socketio.emit('notification', {"message": message}, room=recipient_sid)

    db.session.commit()
    return jsonify({"message": "Post liked and notification sent"})


# ---------------- Socket Events ---------------- #

@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("register")
def handle_register(data):
    user_id = str(data["user_id"])
    connected_users[user_id] = request.sid
    print(f"User {user_id} registered with socket ID {request.sid}")


@socketio.on("disconnect")
def handle_disconnect():
    sid = request.sid
    for user_id, socket_id in list(connected_users.items()):
        if socket_id == sid:
            del connected_users[user_id]
            print(f"User {user_id} disconnected")
            break


# ---------------- Start App ---------------- #

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)
