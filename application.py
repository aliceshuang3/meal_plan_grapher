# Alice Huang, Aug 2019

import os
import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "ON8ZvUZmSegF1n06YBiw", "isbns": "9781632168146"})
print(res.json())


from flask import Flask, session, render_template, request, jsonify, abort
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    session["user_id"] = [] # clear the stored user when logging out
    return render_template("index.html")

@app.route("/chart")
def chart():
    return render_template("chart.html")
    
@app.route("/hello", methods=["POST"])
def hello():
    username = request.form.get("username") # get form values
    password = request.form.get("password")
    # check if username is already in users table in database
    if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount == 1:
          return render_template("error.html", message="That username already exists.")
    else:
      # if not in database, add username and password
      db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
              {"username": username, "password": password})
      db.commit()
      return render_template("hello.html", username=username)

@app.route("/login", methods=["POST"])
def hello2():
    username = request.form.get("username")
    password = request.form.get("password")
    session["user_id"] = [] # set up session to store user id
    # get the object with matching username and password from users database
    id = db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username": username, "password": password}).fetchone()
    db.commit()
    # check if user entered wrong username/password
    if id is None:
        return render_template("error.html", message="Wrong username or password.")
    else:
        # if correct login info, add user id to session to store
        session["user_id"].append(id.user_id)
        return render_template("hello2.html", username=username, id=id.username)

@app.route("/search")
def search():
    id = session["user_id"][0] # get the integer representing the user id
    # get the username that corresponds to the user id
    id2 = db.execute("SELECT username FROM users WHERE user_id = :user_id", {"user_id": id}).fetchone()
    db.commit()
    return render_template("search.html", id2=id2.username)

@app.route("/match", methods=["POST"])
def matches():
    choice = request.form.get("category") # get form values
    keyword = request.form.get("keyword")
    id = session["user_id"][0] # get current user id logged in
    # get corresponding username
    id2 = db.execute("SELECT username FROM users WHERE user_id = :user_id", {"user_id": id}).fetchone()
    term = "%" + keyword + "%"
    # get all books where the keyword is equal to or part of the corresponding keyword in the database
    if choice == 'isbn':
        matches = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn", {"isbn": term}).fetchall()
    elif choice == 'title':
        matches = db.execute("SELECT * FROM books WHERE title LIKE :title", {"title": term}).fetchall()
    else:
        matches = db.execute("SELECT * FROM books WHERE author LIKE :author", {"author": term}).fetchall()
    db.commit()
    # check if the search returned no matches
    if len(matches) == 0:
        return render_template("error.html", message="No results found. Try another search term.")
    else:
        return render_template("match.html", matches=matches, id2=id2.username)

@app.route("/match/<isbn>")
def match(isbn):
    id = request.args.get('isbn', None)
    id2 = session["user_id"][0] # get current logged in user id
    # get matching username
    id3 = db.execute("SELECT username FROM users WHERE user_id = :user_id", {"user_id": id2}).fetchone()
    # get book that the isbn in the url corresponds to
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    # get all reviews for this book
    reviews = db.execute("SELECT user_id, rating, review FROM reviews WHERE book_id = :book_id", {"book_id": isbn}).fetchall()
    if len(reviews) == 0:
        empty = 1 # if no reviews are found, appropriate message displays
    else:
        empty = 0
    # get the users who wrote all the reviews for this book
    users = db.execute("SELECT username, book_id FROM users JOIN reviews ON reviews.user_id = users.user_id WHERE book_id = :book_id", {"book_id": isbn}).fetchall()
    db.commit()

    # get data from Goodreads site
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "ON8ZvUZmSegF1n06YBiw", "isbns": isbn})
    data = res.json()
    return render_template("details.html", book=book, reviews=reviews, empty=empty, users=users, id=id, data=data, id3=id3.username)

@app.route("/write/<isbn>")
def write(isbn):
    id2 = session["user_id"][0] # get user id for current user logged in
    # get corresponding username
    id3 = db.execute("SELECT username FROM users WHERE user_id = :user_id", {"user_id": id2}).fetchone()
    # get title of book with this isbn #
    title = db.execute("SELECT title FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    db.commit()
    return render_template("review.html", id=isbn, title=title[0], id3=id3.username)

@app.route("/submit/<isbn>", methods=["POST"])
def submit(isbn):
    currUser = session["user_id"][0] # get the current user logged in
    rating = request.form.get("inlineRadioOptions") # get form values
    review = request.form.get("comment")
    # check if this user already submitted a review for this book
    if db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND book_id = :book_id", {"user_id": currUser, "book_id": isbn}).rowcount == 1:
        message = "You cannot submit another review for this book."
    else:
        message = "Thanks for submitting a review!"
        db.execute("INSERT INTO reviews (user_id, book_id, rating, review) VALUES (:user_id,"
        + " :book_id, :rating, :review)", {"user_id": currUser, "book_id": isbn, "rating": rating, "review": review})
    db.commit()
    return render_template("submit.html", message=message, rating=rating, review=review)

@app.errorhandler(404)
def resource_not_found(e):
    # 404 error page if user access api with nonexistent isbn #
    return jsonify(error=str(e)), 404

@app.route("/api/<isbn>", methods=["GET"])
def api(isbn):
    # first check if isbn exists
    if db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).rowcount == 0:
        abort(404, description="Not a valid ISBN number.")

    # then calculate review_count and average_score
    # get number of reviews
    review_count = db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": isbn}).rowcount
    if review_count == 0:
        average_score = "NA"
    else:
        # get all ratings for this book
        ratings = db.execute("SELECT rating FROM reviews WHERE book_id = :book_id", {"book_id": isbn})
        sum = 0
        # add up all ratings and divide by total #
        for rating in ratings:
            sum += rating[0]
        average_score = sum/review_count

    # get corresponding book object
    book = db.execute("SELECT title, author, year FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    title = book.title
    author = book.author
    year = book.year
    db.commit()
    book_json = {"title": title, "author": author, "year": year, "isbn": isbn, "review_count": review_count, "average_score": average_score}
    return jsonify(book_json)
