# -*- encoding: utf-8 -*-
"""
Copyright : COGNIPATH 2023
"""

from app         import db
from flask_login import UserMixin
from enum import Enum
import calendar
import sqlite3
from datetime import datetime
from dateutil.relativedelta import relativedelta
import firebase_admin
from firebase_admin import credentials, firestore, auth
DATABASE = './app/database.sqlite3'
class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data.get('email')
        self.user_id = user_data.get('id')
        self.first_name = user_data.get('first_name')
        self.last_name = user_data.get('last_name')
        self.email = user_data.get('email')
        self.phone_number = user_data.get('phone_number')
        self.last_modified = user_data.get('last_modified')

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.first_name)+ ' - ' +str( self.last_name) + ' - ' + str( self.phone_number)+ ' - ' + str(self.last_modified)
    
    def get_id(self):
        return str(self.id)


def get_current_timestamp():
    return datetime.now().isoformat()
# class ChildProfile(db.Model):
#     __tablename__ = 'child_profile'

#     profile_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     name = db.Column(db.String(64))
#     birthdate = db.Column(db.Date)

#     user = db.relationship('Users', backref=db.backref('child_profiles', lazy=True))

#     def __init__(self, user_id, name, birthdate):
#         self.user_id = user_id
#         self.name = name
#         self.birthdate = birthdate

#     def __repr__(self):
#         return f'<ChildProfile {self.name}>'

#     def save(self):
#         db.session.add(self)
#         db.session.commit()

# class ProgressTracking(db.Model):
#     __tablename__ = 'progress_tracking'

#     progress_id = db.Column(db.Integer, primary_key=True)
#     child_id = db.Column(db.Integer, db.ForeignKey('child_profile.profile_id'), nullable=False)
#     score = db.Column(db.Integer, nullable=False)
#     communication_skills = db.Column(db.Integer, nullable=False)
#     writing_skills = db.Column(db.Integer, nullable=False)
#     consistency = db.Column(db.Integer, nullable=False)
#     emotions_understanding = db.Column(db.Integer, nullable=False)
#     expressive_proficiency = db.Column(db.Integer, nullable=False)

#     child_profile = db.relationship('ChildProfile', backref=db.backref('progress_tracking', lazy=True))

#     def __init__(self, child_id, score=0, communication_skills=0, writing_skills=0, consistency=0, emotions_understanding=0, expressive_proficiency=0):
#         self.child_id = child_id
#         self.score = score
#         self.communication_skills = communication_skills
#         self.writing_skills = writing_skills
#         self.consistency = consistency
#         self.emotions_understanding = emotions_understanding
#         self.expressive_proficiency = expressive_proficiency

#     def save(self):
#         db.session.add(self)
#         db.session.commit()

# class Activities(db.Model):
#     __tablename__ = 'activities'

#     activity_id = db.Column(db.Integer, primary_key=True)
#     activity_name = db.Column(db.String(255), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     profile_id = db.Column(db.Integer, db.ForeignKey('child_profile.profile_id'), nullable=False)

#     child_profile = db.relationship('ChildProfile', backref=db.backref('activities', lazy=True))

#     def __init__(self, activity_name, profile_id):
#         self.activity_name = activity_name
#         self.profile_id = profile_id

#     def __repr__(self):
#         return f'<Activity {self.activity_name}>'

#     def save(self):
#         db.session.add(self)
#         db.session.commit()
# class EmotionRecognition(db.Model):
#     __tablename__ = 'emotion_recognition'

#     record_id = db.Column(db.Integer, primary_key=True)
#     child_id = db.Column(db.Integer, db.ForeignKey('child_profile.profile_id'), nullable=False)
#     image_url = db.Column(db.String, nullable=False)
#     selected_emotion = db.Column(db.String, nullable=False)
#     correct_emotion = db.Column(db.String, nullable=False)
#     attempted_at = db.Column(db.DateTime, default=datetime.utcnow)

#     child_profile = db.relationship('ChildProfile', backref=db.backref('emotion_recognition', lazy=True))

#     def __init__(self, child_id, image_url, selected_emotion, correct_emotion, attempted_at=None):
#         self.child_id = child_id
#         self.image_url = image_url
#         self.selected_emotion = selected_emotion
#         self.correct_emotion = correct_emotion
#         if attempted_at is None:
#             self.attempted_at = datetime.utcnow()
#         else:
#             self.attempted_at = attempted_at

#     def save(self):
#         db.session.add(self)
#         db.session.commit()

# class WritingWizard(db.Model):
#     __tablename__ = 'writing_wizard'

#     record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     child_id = db.Column(db.Integer, db.ForeignKey('child_profile.profile_id'), nullable=False)
#     grade = db.Column(db.Integer, nullable=False)
#     scored_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

#     child_profile = db.relationship('ChildProfile', backref=db.backref('writing_wizard_records', lazy=True))

#     def __init__(self, child_id, grade, scored_at=None):
#         self.child_id = child_id
#         self.grade = grade
#         if scored_at is None:
#             self.scored_at = datetime.utcnow()
#         else:
#             self.scored_at = scored_at

#     def __repr__(self):
#         return f'<WritingWizard {self.record_id}>'

#     def save(self):
#         db.session.add(self)
#         db.session.commit()

# def update_child_progress(child_id):
#     """
#     Update the progress tracking columns for a specific child based on their activities.
#     """
#     # Retrieve all activities for the given child's ID
#     child_activities = Activities.query.filter_by(profile_id=child_id).all()

#     # Initialize scores
#     communication_skills_score = 0
#     writing_skills_score = 0
#     consistency_score = 0
#     emotions_understanding_score = 0
#     expressive_proficiency_score = 0
#     count = 0

#     for activity in child_activities:
#         # Sum up the scores from activities (assuming each activity has these fields)
#         communication_skills_score += activity.communication_skills
#         writing_skills_score += activity.writing_skills
#         consistency_score += activity.consistency
#         emotions_understanding_score += activity.emotions_understanding
#         expressive_proficiency_score += activity.expressive_proficiency
#         count += 1

#     # Calculate average scores if there are activities
#     if count > 0:
#         communication_skills_score /= count
#         writing_skills_score /= count
#         consistency_score /= count
#         emotions_understanding_score /= count
#         expressive_proficiency_score /= count

#     # Update the progress tracking for the given child
#     progress = ProgressTracking.query.filter_by(child_id=child_id).first()

#     if progress:
#         progress.communication_skills = communication_skills_score
#         progress.writing_skills = writing_skills_score
#         progress.consistency = consistency_score
#         progress.emotions_understanding = emotions_understanding_score
#         progress.expressive_proficiency = expressive_proficiency_score

#         # Save the changes to the database
#         db.session.commit()
#     else:
#         # Handle the case where the progress tracking record does not exist
#         pass

#     return count
def update_emotions_understanding(child_id, selected_emotion, correct_emotion):
    """
    Update the emotions understanding score for a specific child based on the EmotionRecognition record.
    """
    try:
        # Create a new EmotionRecognition record in Firestore
        emotion_data = {
            'child_id': child_id,
            'image_url': "image_url",  # Replace with the actual URL if available
            'selected_emotion': selected_emotion,
            'correct_emotion': correct_emotion,
            'attempted_at': datetime.utcnow().isoformat()
        }
        # Add the new record to the 'EmotionRecognition' collection
        db.collection('emotion_recognition').add(emotion_data)

        # Calculate the new percentage (using your defined `get_percentage` function)
        percentage = get_percentage(child_id)
        # Reference to the child's progress tracking record in 'ProgressTracking'
        progress_ref = db.collection('progress_tracking').where('child_id', '==', child_id)
        progress_docs = progress_ref.get()

        # Check if a progress record exists
        if progress_docs:
            # If progress record exists, update emotions_understanding
            for doc in progress_docs:
                doc_ref = db.collection('progress_tracking').document(doc.id)
                doc_ref.update({'emotions_understanding': percentage})
        else:
                progress_tracking_ref = db.collection('progress_tracking').document()  # Create a new document reference
                progress_id = progress_tracking_ref.id  # Use the document ID as the progress_id

                # Initialize progress tracking for the child profile
                progress_data = {
                    'progress_id': progress_id,  # Generate a unique progress_id
                    'child_id': child_id,  # Reference child_id as a foreign key
                    'score': 0,
                    'communication_skills': 0,
                    'writing_skills': 0,
                    'consistency': 0,
                    'emotions_understanding': percentage,
                    'expressive_proficiency': 0,
                    'last_modified': datetime.now().isoformat()
                }
                progress_tracking_ref.set(progress_data)  # Set the progress data with progress_id as the document ID

        print("Emotion understanding updated successfully.")

    except Exception as e:
        print("An error occurred:", str(e))



def update_writing_skills(child_id, grade):
    """
    Update the writing skills score for a specific child based on the WritingWizard record.
    """
    try:
        # Create a new WritingWizard record in Firestore
        writing_data = {
            'child_id': child_id,
            'grade': grade,
            'scored_at': datetime.utcnow().isoformat()
        }
        # Add the new record to the 'WritingWizard' collection
        db.collection('writing_wizard').add(writing_data)

        # Calculate the new writing score using the provided function
        writing_score = calculate_writing_skills(child_id)

        # Reference to the child's progress tracking record in 'ProgressTracking'
        progress_ref = db.collection('progress_tracking').where('child_id', '==', child_id)
        progress_docs = progress_ref.get()

        # Check if a progress record exists
        if progress_docs:
            # If progress record exists, update writing_skills
            for doc in progress_docs:
                doc_ref = db.collection('progress_tracking').document(doc.id)
                doc_ref.update({'writing_skills': writing_score})
        else:
                progress_tracking_ref = db.collection('progress_tracking').document()  # Create a new document reference
                progress_id = progress_tracking_ref.id  # Use the document ID as the progress_id

                # Initialize progress tracking for the child profile
                progress_data = {
                    'progress_id': progress_id,  # Generate a unique progress_id
                    'child_id': child_id,  # Reference child_id as a foreign key
                    'score': 0,
                    'communication_skills': 0,
                    'writing_skills': writing_score,
                    'consistency': 0,
                    'emotions_understanding': 0,
                    'expressive_proficiency': 0,
                    'last_modified': datetime.now().isoformat()
                }
                progress_tracking_ref.set(progress_data)  # Set the progress data with progress_id as the document ID

        print("Writing skills updated successfully.")

    except Exception as e:
        print("An error occurred:", str(e))


def get_activities_count_by_day(child_id):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    activity_counts = [0] * 7  # Initialize the list with zeros for each day of the week

    try:
        # Query all activities for the given child_id
        activities_query = db.collection('activities') \
            .where('child_id', '==', child_id) \
            .get()

        # Count activities by the day of the week
        for doc in activities_query:
            created_at_str = doc.to_dict().get('timestamp')
            if created_at_str:
                # Convert created_at string to a datetime object
                created_at = datetime.fromisoformat(created_at_str)
                day_index = created_at.weekday()  # Monday is 0, Sunday is 6
                activity_counts[day_index] += 1

        return activity_counts

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

def get_activities_count_by_week(child_id):
    """
    Get the count of activities for each week for a specific child.
    
    Args:
        child_id (str): The ID of the child to get activity counts for
        
    Returns:
        list: List of activity counts by week, ordered chronologically
    """
    activity_counts = []
    week_counts = {}

    try:
        # Query Firestore for activities with the specified child_id
        activities_ref = db.collection('activities')
        query = activities_ref.where('child_id', '==', child_id)
        
        # Fetch all matching activities
        activities = query.stream()

        # Process each activity to count by week
        for activity in activities:
            activity_data = activity.to_dict()
            created_at_str = activity_data.get('timestamp')
            
            # Convert created_at string to a datetime object
            if created_at_str:
                created_at_datetime = datetime.fromisoformat(created_at_str)
                year_week = created_at_datetime.strftime('%Y-%W')  # Format as "YYYY-WW"
                
                # Update the count for the corresponding week
                if year_week in week_counts:
                    week_counts[year_week] += 1
                else:
                    week_counts[year_week] = 1

        # Sort week_counts by week and extract counts in order
        sorted_week_counts = sorted(week_counts.items())
        activity_counts = [count for _, count in sorted_week_counts]

        return activity_counts
        
    except Exception as e:
        print(f"An error occurred while counting activities by week for child {child_id}: {str(e)}")
        return None


# def get_activities_count_by_month(email):
#     activity_counts = [0] * 9  # Initialize the list with zeros for each month
#     month_labels = []

#     try:
#         conn = sqlite3.connect(DATABASE)
#         cursor = conn.cursor()

#         # SQL query to count activities by month for the last 9 months
#         query = """
#         SELECT strftime('%Y-%m', date_time) as month, COUNT(*) as count
#         FROM activities
#         WHERE date_time >= date('now', '-9 months') and user_email = ?
#         GROUP BY month
#         """
#         cursor.execute(query, (email,))

#         for row in cursor.fetchall():
#             month = row[0]
#             activity_count = int(row[1])

#             # Determine the index of the month in the last 9 months
#             # For example, if you're in October, the index would be 0 for October, 1 for September, and so on.
#             current_month = cursor.execute("SELECT strftime('%Y-%m', 'now')").fetchone()[0]
#             month_index = (int(current_month[:4]) - int(month[:4])) * 12 + int(current_month[5:]) - int(month[5:])

#             # Update the count for the respective month
#             activity_counts[month_index] = activity_count

#             # Get the month label (e.g., "Feb") and add it to the labels list
#             month_label = datetime.strptime(month, "%Y-%m").strftime("%b")
#             month_labels.append(month_label)

#         return activity_counts, month_labels

#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         return None

#     finally:
#         conn.close()

def get_activities_count_last_9_months(child_id):
    months = ""  # To store the first letters of each month
    month_counts = []  # To store activity counts for each month
    current_date = datetime.now()
    
    # Create labels for the last 9 months in "YYYY-MM" format
    month_labels = [(current_date - relativedelta(months=i)).strftime('%Y-%m') for i in range(9)]
    month_labels.reverse()  # Start from the oldest to the newest month
    
    try:
        # Query Firestore for activities with the specified profile_id
        activities_query = db.collection('activities').where('child_id', '==', child_id).get()

        # Dictionary to count activities by month
        month_count_dict = {month_label: 0 for month_label in month_labels}

        # Process each activity
        for activity in activities_query:
            created_at_str = activity.to_dict().get('timestamp')
            if created_at_str:
                # Convert the timestamp string to datetime and format it as "YYYY-MM"
                created_at_datetime = datetime.fromisoformat(created_at_str)
                activity_month = created_at_datetime.strftime('%Y-%m')
                
                # Update the count if the activity falls within the last 9 months
                if activity_month in month_count_dict:
                    month_count_dict[activity_month] += 1

        # Prepare the output
        for month_label in month_labels:
            year, month_num = month_label.split('-')
            # Append the first letter of the month to `months`
            month_first_letter = calendar.month_abbr[int(month_num)][0]
            months += month_first_letter
            # Add the count for this month to `month_counts`
            month_counts.append(month_count_dict[month_label])

        # `this_month` is the current month's full name
        this_month = calendar.month_abbr[current_date.month]

        return this_month, months, month_counts

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None, None, None

def get_percentage(child_id):
    try:
        answers_query = db.collection("emotion_recognition").where("child_id", "==", child_id)
        answers = answers_query.stream()
        right_answers_count = 0
        total_answers_count = 0
        for answer in answers:
            total_answers_count += 1
            data = answer.to_dict()
            if data.get("selected_emotion") == data.get("correct_emotion"):
                right_answers_count += 1
        print("right_answers_count:")
        print(str(right_answers_count))
        print("total_answers_count:")
        print(str(total_answers_count))

        # Calculate the percentage of correct answers
        if total_answers_count > 0:
            percentage = int((right_answers_count / total_answers_count) * 100)
        else:
            percentage = 0

        return percentage

    except Exception as e:
        print("An error occurred: ", str(e))
        return None


def calculate_writing_skills(child_id):
    try:
        # Reference to the writing_wizard collection
        writing_wizard_ref = db.collection('writing_wizard')
        
        # Query to get all records for the specified child_id
        query = writing_wizard_ref.where('child_id', '==', child_id).stream()

        num_paragraphs = 0
        total_grades = 0
        
        # Iterate through the query results
        for doc in query:
            num_paragraphs += 1
            total_grades += doc.to_dict().get('grade', 0)

        # Calculate the average score
        if num_paragraphs > 0:
            score = total_grades // num_paragraphs  # Use integer division
            return score
        else:
            return 0  # Return 0 if no paragraphs found

    except Exception as e:
        print("An error occurred: ", str(e))
        return None

def get_recent_activities(child_id):
    try:
        # Query Firestore for the 6 most recent activities for the given child_id
        activities_query = db.collection('activities') \
            .where('child_id', '==', child_id) \
            .order_by('timestamp', direction=firestore.Query.DESCENDING) \
            .limit(6) \
            .get()

        # Format the fetched activities
        formatted_activities = []
        for activity in activities_query:
            activity_data = activity.to_dict()
            activity_id = activity.id
            activity_name = activity_data.get('activity_type')
            created_at_str = activity_data.get('timestamp')
            profile_id = activity_data.get('child_id')

            # Convert the timestamp string to a readable format
            if created_at_str:
                created_at = datetime.fromisoformat(created_at_str)
                readable_date = created_at.strftime("%B %d, %Y %I:%M %p")
                formatted_activities.append((activity_id, activity_name, readable_date, profile_id))
                # print(formatted_activities)
           
        return formatted_activities

    except Exception as e:
        print("An error occurred:", str(e))
        return None

       


def activities_per_month(child_id):
    try:
        # Get the current year and month as a formatted string
        now = datetime.now()
        current_year_month = f"{now.year}-{now.month:02}"

        # Query to retrieve activities with matching profile_id
        activities_query = db.collection('activities') \
            .where('child_id', '==', child_id) \
            .get()

        # Filter documents to those within the current month
        count = sum(
            1 for doc in activities_query 
            if doc.to_dict().get('timestamp', '').startswith(current_year_month)
        )

        return count

    except Exception as e:
        print("An error occurred:", str(e))
        return None






# #################################################### QUIZ DATA BASE ####################################################

# class QuizAttempt(db.Model):
#     __tablename__ = 'quiz_attempt'

#     record_id = db.Column(db.Integer, primary_key=True)
#     child_id = db.Column(db.Integer, db.ForeignKey('child_profile.profile_id'), nullable=False)
#     question_id = db.Column(db.Integer, nullable=False)
#     selected_answer = db.Column(db.String, nullable=False)
#     correct_answer = db.Column(db.String, nullable=False)
#     attempted_at = db.Column(db.DateTime, default=datetime.utcnow)

#     child_profile = db.relationship('ChildProfile', backref=db.backref('quiz_attempt', lazy=True))

#     def __init__(self, child_id, question_id, selected_answer, correct_answer, attempted_at=None):
#         self.child_id = child_id
#         self.question_id = question_id
#         self.selected_answer = selected_answer
#         self.correct_answer = correct_answer
#         if attempted_at is None:
#             self.attempted_at = datetime.utcnow()
#         else:
#             self.attempted_at = attempted_at

#     def save(self):
#         db.session.add(self)
#         db.session.commit()

########################################################################################################################