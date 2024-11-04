# İmport necessary libraries and modules
from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

# Create an instance of the Flask class for our web application
app = Flask(__name__)

# Configure the SQLAlchemy database URI to use a SQLite database named 'quiz.db'
# The 'sqlite:///' prefix indicates that we are using SQLite and the database file will be located in the current directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'

# Create an instance of SQLAlchemy, passing in the Flask app instance
# This sets up the database connection and allows us to define models and interact with the database
db = SQLAlchemy(app)

# Define a model for storing user answers in the database
class UserAnswer(db.Model):

    # Create a column named 'id' which will serve as the primary key for this table
    # The 'primary_key=True' argument indicates that this column will uniquely identify each record
    id = db.Column(db.Integer, primary_key=True)

    # Create a column named 'username' to store the name of the user
    # This column can hold strings up to 100 characters and cannot be null
    username = db.Column(db.String(100), nullable=False)

    # Create a column named 'score' to store the user's score from the quiz
    # This column is of type Integer and cannot be null
    score = db.Column(db.Integer, nullable=False)



# Create the database tables defined by the models
with app.app_context():  # Create an application context for the following operations
    db.create_all()  # This command creates all tables defined by the SQLAlchemy models (if they don't already exist)


@app.route('/', methods=['GET', 'POST'])  # Define the route for the root URL with both GET and POST methods
def quiz():
    if request.method == 'POST':  # Check if the request method is POST (indicating a form submission)
        username = request.form['username']  # Retrieve the username from the submitted form data
        score = calculate_score(request.form)  # Check the answers and calculate the score
        
        # Create a new UserAnswer instance to store the username and score
        new_answer = UserAnswer(username=username, score=score)
        
        # Add the new answer record to the database session
        db.session.add(new_answer)
        
        # Commit the changes to the database (save the new answer)
        db.session.commit()
        
        # Render the 'index.html' template with the best score and the current score
        return render_template('index.html', 
                               best_score=UserAnswer.query.order_by(UserAnswer.score.desc()).first(), 
                               score=score)
    
    # If the request method is GET, retrieve the best score from the database
    best_score = UserAnswer.query.order_by(UserAnswer.score.desc()).first()
    
    # Render the 'index.html' template with the best score and no current score
    return render_template('index.html', best_score=best_score, score=None)


def calculate_score(form_data):
    score = 0  # Initialize the score to 0
    # Dictionary containing correct answers for the quiz questions
    correct_answers = {
        'question1': 'Pandas',   # Correct answer for question 1
        'question2': 'OpenCV',    # Correct answer for question 2
        'question3': 'NLTK',      # Correct answer for question 3
        'question4': 'TensorFlow'  # Correct answer for question 4
    }

    # Loop through each question and its corresponding correct answer
    for question, answer in correct_answers.items():
        # Check if the user's answer matches the correct answer
        if form_data.get(question) == answer:
            score += 25  # Add 25 points for each correct answer

    return score  # Return the final calculated score


if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask application in debug mode

