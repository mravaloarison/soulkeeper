from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from cs50 import SQL
from flask_session import Session
from helpers import login_required, apology
from flask_cors import CORS
import os, pyrebase, requests
from news import make_news_api_request, categories
from personality import personality_tests, check_user_choice, personality_details, user_personality, is_user_data_complete


app = Flask(__name__)

# Enable CORS for your app with permissive settings
CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}})
CORS(app, resources={r"/*": {"origins": "https://soulkeeper.onrender.com"}})

db = SQL(os.environ.get("SQL_ENVIRONMENT"))

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

config = {
    "apiKey": "AIzaSyBtOIa2Wa9cBTdQ8mgRwt4dFbOV3egAnt8",
    "authDomain": "soulkeeper-a0b72.firebaseapp.com",
    "projectId": "soulkeeper-a0b72",
    "storageBucket": "soulkeeper-a0b72.appspot.com",
    "messagingSenderId": "734672571215",
    "appId": "1:734672571215:web:7d263a080398934b64533a",
    "measurementId": "G-686S3TFQ0S",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

class NewUser():
    def __init__(self, email = None, password = None, avatar = None, personality_type = None, username = None):
        self.username = username
        self.password = password
        self.personality_type = personality_type
        self.avatar = avatar
        self.email = email

    def set_email(self, new_email):
        self.email = new_email

    def set_password(self, new_password):
        self.password = new_password

    def set_avatar(self, new_avatar):
        self.avatar = new_avatar

    def set_personality_type(self, new_personality_type):
        self.personality_type = new_personality_type

    def set_username(self, new_username):
        self.username = new_username

new_user = NewUser()
user_personality_score = 0

@app.route("/")
def main():
    return render_template("index.html")


@app.route("/login_in", methods=["POST", "GET"])
def login_in():
    
    session.clear()

    user_data = request.get_json()

    email = user_data["email"]
    session["uid"] = user_data["uid"]
    session["email"] = email

    user_db = db.execute("SELECT * FROM users WHERE email = ?", email)
    
    if user_db == 0:
        # get email
        new_user.set_email(email)

    return jsonify(user_data)


@app.route("/home")
@login_required
def home():
    user_db = db.execute("SELECT * FROM users WHERE email = ?", session["email"])
    registered = True

    if not user_db:
        registered = False

    return render_template("home.html", registered = registered)


@app.route("/logout")
@login_required
def logout():

    session.clear()

    flash("Logout successfull ✅")
    return redirect(url_for("main"))

# ++++++++++++++++++
# NEW USERS FEATURES
@app.route("/start_personality_test/<int:index>")
@login_required
def start_personality_test(index):
    questions = personality_tests["questions"]
    return render_template("personality_test.html", 
        questions = questions[index], 
        personality_tests = personality_tests, 
        index = index,
    )


@app.route("/submit_personality_test/<int:index>", methods=["POST"])
@login_required
def personality_test(index):
    questions = personality_tests["questions"]
    user_choice = request.form.get("question" + str(index))
    
    if check_user_choice(user_choice):
        global user_personality_score
        user_personality_score += int(user_choice)

        if index + 1 < len(questions):
            return redirect(url_for("start_personality_test", index=index + 1))
        else:
            return redirect(url_for("personality_result", score=user_personality_score))
    else:
        flash("Invalid choice. Please try again.")
        return redirect(url_for("start_personality_test", index = 0))
    

@app.route("/get_avatar_soulname", methods = ["POST"])
@login_required
def get_avatar_soulname():

    user_data = request.get_json()
    
    session["username"] = user_data["username"]

    new_user.set_username(user_data["username"])
    new_user.set_avatar(user_data["avatar"])
    new_user.set_email(session["email"])
    new_user.set_password(session["uid"])

    return jsonify(user_data)


@app.route("/personality_result")
@login_required
def personality_result():

    global user_personality_score
    personality_type = user_personality(user_personality_score)

    if not personality_type == None:
        details = personality_details.get(personality_type, "Personality details not available.")

        # NEED TO STORE THE DATA
        new_user.set_personality_type(personality_type)

        return render_template('personality_details.html', personality_type=personality_type, details=details)

    flash("Something went wrong! please restart your personality test")
    return redirect(url_for("home"))
# END NEW USERS FEATURES
# ++++++++++++++++++++++


@app.route("/search_avatar")
@login_required
def search_avatar():
    global user_avatar_enable 
    user_avatar_enable = True
    api_key = os.environ.get("MULTIAVATAR_API_KEY")
    avatar = request.args.get("q")

    return f'https://api.multiavatar.com/{avatar}.png?apikey={api_key}'


@app.route("/profile")
@login_required
def profile():

    user_db = db.execute("SELECT * FROM users WHERE email = ?", session["email"])

    user_data = {
        "name": new_user.username,
        "password_hash": new_user.password,
        "personality_type": new_user.personality_type,
        "avatar_url": new_user.avatar,
        "email": new_user.email
    }


    if not user_db:
        if is_user_data_complete(user_data):
            db.execute("INSERT INTO users (name, email, password_hash, avatar_url, personality_type) VALUES (?,?,?,?,?)",
                new_user.username,
                new_user.email,
                new_user.password,
                new_user.avatar,
                new_user.personality_type,
            )
        
        else: 
            flash("Profile not available yet, your latest change hasn't been saved!")
            return redirect(url_for("home"))

        user = user_data
    
    else: 
        user = user_db[0]

    stories_db = db.execute("SELECT * FROM stories")
    comments = db.execute("SELECT * FROM commments")


    idea_shared = len(comments) 
    idea_accuracy_avatar = idea_shared / 27

    story_shared = len(stories_db)
    story_accuracy_avatar = story_shared / 20

    progress_data = [
        { "emoji": "🙂", "label": "Personality", "percentage": 12 },
        { "emoji": "🗣️", "label": "Idea expression", "percentage": idea_accuracy_avatar },
        { "emoji": "📝", "label": "Storytelling", "percentage": story_accuracy_avatar },
    ]

    return render_template("profile.html", user=user, progress_data = progress_data)


# /////////
# NEWS_API
@app.route("/search_news/<string:q>")
def search(q):
    params = {'q': q, 'sortBy': 'popularity'}
    return make_news_api_request('everything', params)


@app.route("/news_category/<string:c>")
def category(c):
    params = {'category': c, 'country': 'us'}
    return make_news_api_request('top-headlines', params)
# END NEWS_API
# /////////////



@app.route("/find_soul")
@login_required
def find_soul():
    return render_template("search_user.html")




@app.route("/search_user")
@login_required
def search_user():
    resp_db = db.execute("SELECT name, avatar_url, personality_type FROM users WHERE name LIKE ?", "%" + request.args.get("q") + "%")
    return resp_db



@app.route("/avatar/<string:user_name>")
@login_required
def avatar(user_name):
    user_in_db = db.execute("SELECT * FROM users WHERE name = ?", user_name)
    if user_in_db:
        stories_db = db.execute("SELECT * FROM stories WHERE user_id = ?", user_in_db[0]["user_id"])
        comments = db.execute("SELECT * FROM commments WHERE user_id = ?", user_in_db[0]["user_id"])

        idea_shared = len(comments) 
        idea_accuracy_avatar = idea_shared / 27

        story_shared = len(stories_db)
        story_accuracy_avatar = story_shared / 20

        progress_data = [
            { "emoji": "🙂", "label": "Personality", "percentage": 12 },
            { "emoji": "🗣️", "label": "Idea expression", "percentage": idea_accuracy_avatar },
            { "emoji": "📝", "label": "Storytelling", "percentage": story_accuracy_avatar },
        ]
        return render_template("profile.html", user = user_in_db[0], progress_data = progress_data)
    
    return apology("Something went wrong! Please go back to homepage")


# HOME ROUTES
@app.route("/share_opinion")
@login_required
def share_opinion():
    return render_template("share_opinion.html", categories=categories)


@app.route("/get_idea/<string:type>")
@login_required
def get_idea(type):

    user_id = db.execute("SELECT user_id FROM users WHERE email = ?", session["email"])
    if user_id:
        db.execute("INSERT INTO commments (content, post_title, post_type, user_id) VALUES (?, ?, ?, ?)", 
            request.args.get("user_idea_input"),
            request.args.get("title"),
            type,
            int(user_id[0]['user_id'])
        )

    
    comments = db.execute("SELECT * FROM commments")
    if comments:
        idea_shared = len(comments) 
        idea_accuracy_avatar = idea_shared / 27

    return render_template("successful.html", accuracy=idea_accuracy_avatar)


@app.route("/talk_to_the_avatar/<int:id>")
def talk_to_the_avatar(id):

    avatar = db.execute("SELECT personality_type FROM users WHERE user_id = ?", id)
    avatar_type= avatar[0]["personality_type"]

    ...

if __name__ == "__main__":
    app.run(debug=True)