from .librabies_to_import import *

import random
import string
from mailjet_rest import Client
import os

import hashlib
from PIL import UnidentifiedImageError





load_dotenv()

MJ_APIKEY_PUBLIC=os.getenv("MJ_APIKEY_PUBLIC")
MJ_APIKEY_PRIVATE=os.getenv("MJ_APIKEY_PRIVATE")

# Azure OpenAI Client Initialization

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
client = AzureOpenAI(
  api_key=AZURE_OPENAI_API_KEY,
  api_version=AZURE_API_VERSION,
  azure_endpoint=AZURE_OPENAI_ENDPOINT
)

IMAGE_API_URL = os.getenv("IMAGE_API_URL")
API_URL_trocr=os.getenv("API_URL_trocr")
API_URL_3D = os.getenv("API_URL_3D")
Image_Bearer = os.getenv("Image_Bearer")
headers = {"Authorization": Image_Bearer}

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# gemini init
GEMINI_API_KEY =os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
model_emotions = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"})
CV_API_KEY = os.getenv("CV_API_KEY")
SP_API_KEY = os.getenv("SP_API_KEY")
ENDPOINT = os.getenv("ENDPOINT")
COGNITIVE_SERVICES_CREDENTIALS = os.getenv("COGNITIVE_SERVICES_CREDENTIALS")
computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(COGNITIVE_SERVICES_CREDENTIALS))



os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev
# Configure session
app.config['SESSION_COOKIE_SECURE'] = True  # For HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes

key_path = "credentials.json"
credentials = Credentials.from_service_account_file(key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"])

if credentials.expired:
    credentials.refresh(Request())
PROJECT_ID = os.getenv("GCP_PROJECT")
LOCATION =  os.getenv('GCP_REGION')   
aiplatform.init(project = PROJECT_ID,location=LOCATION, credentials=credentials)
print("project id : "+PROJECT_ID+" location : "+LOCATION)
vertexai.init(project=PROJECT_ID, location=LOCATION)

def clear_all_session_data():
    """Helper function to clear all session data"""
    # Clear Flask session
    session.clear()
    
    # Clear Flask-Login session
    logout_user()
    
    # Mark session as modified to ensure changes are saved
    session.modified = True
# Helper function to get the current timestamp
def get_current_timestamp():
    return datetime.now().isoformat()

# Create a new user in Firebase
def create_user(id,first_name, last_name, email, phone_number, password):
    user_data = {
        'id':id,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone_number': phone_number,
        'password': password,
        'last_modified': get_current_timestamp()  # Add timestamp
    }
    db.collection('users').document(email).set(user_data)

@app.route('/auth', methods=['GET', 'POST'])
def register():
    msg = None
    success = False
    firebase_config = {
        "apiKey": os.getenv("FIREBASE_WEB_API_KEY"),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
        "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
        "projectId": os.getenv("FIREBASE_PROJECT_ID"),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
        "appId": os.getenv("FIREBASE_APP_ID"),
        "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID")
    }

    if request.method == 'POST':
        if 'signup' in request.form:  # Check if the signup form is submitted
            first_name = request.form['firstName']
            last_name = request.form['lastName']
            email = request.form['email']
            phone_number = request.form['phoneNumber']
            password = request.form['password']
            child_name = request.form['childName']
            birthdate_str = request.form['birthDate']

            # Convert birthdate string to datetime.date object
            try:
                birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
            except ValueError:
                msg = 'Invalid date format. Please use YYYY-MM-DD.'
                return render_template('login.html', msg=msg, success=success,firebase_config=firebase_config)

            # Check if the required fields are not empty
            if first_name and last_name and email and password and child_name:
                # Check if a user with the same email already exists
                user_ref = db.collection('users').document(email)
                if user_ref.get().exists:
                    msg = 'User already exists!'
                else:
                    # Add user to Firebase Authentication and Firestore
                    user_record = auth.create_user(
                        email=email,
                        password=password,
                        display_name=f"{first_name} {last_name}",
                        phone_number=phone_number
                    )

                    # Create user document in Firestore
                    user_data = {
                        'id': user_record.uid,
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'phone_number': phone_number,
                        'last_modified': datetime.now().isoformat()
                    }
                    user_ref.set(user_data)

                    # Generate a unique ID for the child profile (e.g., Firebase auto-generated ID or custom ID)
                    child_profile_ref = db.collection('child_profiles').document()  # Create a new document reference
                    child_id = child_profile_ref.id  # Use the document ID as the child_id

                    # Create child profile in Firestore with custom child_id
                    child_data = {
                        'child_id': child_id,
                        'user_id': user_record.email,
                        'name': child_name,
                        'birthdate': birthdate_str,
                        'last_modified': datetime.now().isoformat()
                    }
                    child_profile_ref.set(child_data)  # Set the child data with child_id as the document ID
                    
                    # Generate a unique ID for the progress id (e.g., Firebase auto-generated ID or custom ID)
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
                        'emotions_understanding': 0,
                        'expressive_proficiency': 0,
                        'last_modified': datetime.now().isoformat()
                    }
                    progress_tracking_ref.set(progress_data)  # Set the progress data with progress_id as the document ID

                    msg = f'Welcome {first_name} {last_name} to the platform!'
                    success = True
            else:
                msg = 'Input error'

        elif 'signin' in request.form:
            email_login = request.form['Email_login']
            password_login = request.form['mdp_login']

            if email_login and password_login:
                try:
                    # Firebase REST API endpoint for sign-in
                    firebase_signin_url = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={os.environ["FIREBASE_WEB_API_KEY"]}'

                    # Verify credentials with Firebase
                    response = requests.post(firebase_signin_url, json={
                        'email': email_login,
                        'password': password_login,
                        'returnSecureToken': True
                    })

                    if response.status_code == 200:
                        # Get user data from Firestore
                        user_ref = db.collection('users').document(email_login).get()
                        
                        if user_ref.exists:
                            # Clear any existing session data before login
                            clear_all_session_data()
                            
                            user_dict = user_ref.to_dict()
                            user_dict['email'] = email_login
                            user = User(user_dict)
                            print("#########################")
                            print(user.id)
                            print("#########################")
                            
                            # Log the user in
                            login_user(user, remember=False)  # Set remember=False to prevent persistent session
                            
                            # Set session variables
                            session['user_email'] = email_login
                            session['logged_in'] = True
                            session.modified = True
                            
                            return redirect(url_for('index'))
                        else:
                            msg = "User not found in database"
                    else:
                        msg = "Password incorrect"
                except Exception as e:
                    msg = f"Authentication error: {str(e)}"
            else:
                msg = 'Please provide both email and password'

    return render_template('login.html', msg=msg, success=success,firebase_config=firebase_config)

@app.route('/handle_google_signin', methods=['POST'])
def handle_google_signin():
    try:
        # Get the ID token sent from the client
        data = request.get_json()
        firebase_id_token = data.get('idToken')
        
        # Verify the Firebase ID token
        decoded_token = auth.verify_id_token(firebase_id_token)
        
        # Get user info from the decoded token
        email = decoded_token['email']
        uid = decoded_token['uid']
        
        # Get additional user info
        firebase_user = auth.get_user(uid)
        
        # Check if user exists in Firestore
        user_ref = db.collection('users').document(email)
        user_doc = user_ref.get()

        if not user_doc.exists:
            # Create new user in Firestore
            user_doc = {
                'id': uid,
                'email': email,
                'first_name': firebase_user.display_name.split()[0] if firebase_user.display_name else '',
                'last_name': ' '.join(firebase_user.display_name.split()[1:]) if firebase_user.display_name else '',
                'profile_picture': firebase_user.photo_url,
                'last_modified': datetime.now().isoformat(),
                'auth_provider': 'google',
                'phone_number':''
            }
            user_ref.set(user_doc)
            # Get the complete user data
            user_doc = user_ref.get().to_dict()
            # Generate a unique ID for the child profile (e.g., Firebase auto-generated ID or custom ID)
            child_profile_ref = db.collection('child_profiles').document()  # Create a new document reference
            child_id = child_profile_ref.id  # Use the document ID as the child_id

            # Create child profile in Firestore with custom child_id
            child_data = {
                'child_id': child_id,
                'user_id': email,
                'name': '',
                'birthdate': '2020-01-01',
                'last_modified': datetime.now().isoformat()
            }
            child_profile_ref.set(child_data)  # Set the child data with child_id as the document ID
            
            # Generate a unique ID for the progress id (e.g., Firebase auto-generated ID or custom ID)
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
                'emotions_understanding': 0,
                'expressive_proficiency': 0,
                'last_modified': datetime.now().isoformat()
            }
            progress_tracking_ref.set(progress_data)  # Set the progress data with progress_id as the document ID
        else:
            # Update existing user's data
            user_ref.update({
                'last_login': datetime.now().isoformat(),
                'profile_picture': firebase_user.photo_url
            })

        
        
        # Create User instance and login
        user = User(user_doc)
        login_user(user)
        
        # Set session data
        session['user_email'] = email
        session['logged_in'] = True
        session.modified = True

        return jsonify({
            'success': True,
            'redirect_url': url_for('index')
        })

    except Exception as e:
        print(f"Error in Google authentication: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/logout')
def logout():
    try:
        # Clear all session data
        clear_all_session_data()
        
        # Create response object
        response = make_response(redirect(url_for('index')))
        
        # Remove all cookies
        cookies_to_delete = ['session', 'remember_token', '_user_id', '_fresh']
        for cookie in cookies_to_delete:
            response.delete_cookie(cookie, path='/', domain=None)
        
        # Add cache control headers
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        return response
        
    except Exception as e:
        print(f"Logout error: {e}")
        # Even if there's an error, try to redirect to login
        return redirect(url_for('index'))

@app.before_request
def before_request():
    if current_user.is_authenticated:
        # Check session consistency
        if 'user_email' not in session or session.get('user_email') != current_user.email:
            clear_all_session_data()
            return redirect(url_for('index'))

# Optional: Add after_request handler to ensure no caching
@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response





#######################################################





def get_child_id():
    user = db.collection('users').where('email', '==', current_user.email).limit(1).get()
    if user:
        user_id = user[0].id
        child_profile = db.collection('child_profiles').where('user_id', '==', user_id).limit(1).get()
        
        if child_profile:
            child_id = child_profile[0].id
            return child_id

@app.route('/api/progress', methods=['GET'])
def get_progress():
    # child_id = request.args.get('childId')  # Retrieve childId from query parameters
    child_id = get_child_id()  # Assumes get_child_id() is a defined function
    print(f"child_id: {child_id}")
    if not child_id:
        return jsonify({'error': 'childId parameter is required'}), 400

    try:
        # Fetch the document where child_id matches the requested child_id
        progress_ref = db.collection("progress_tracking").where("child_id", "==", child_id).limit(1)
        progress_data = progress_ref.stream()

        # Retrieve the first matching document
        progress_doc = next(progress_data, None)
        if progress_doc and progress_doc.exists:
            progress_dict = progress_doc.to_dict()
            return jsonify(progress_dict)
        else:
            return jsonify({'error': 'No data found'}), 404

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An internal error occurred'}), 500
    

def get_child_progress(child_id):
    """
    Retrieve the progress tracking details for a specific child by child_id.

    Args:
        child_id (str): The ID of the child whose progress you want to retrieve.

    Returns:
        dict: The progress tracking data for the child, or None if not found.
    """
    # Using where() with keyword arguments instead of positional arguments
    progress_ref = db.collection('progress_tracking').where(field_path='child_id', op_string='==', value=child_id)
    docs = progress_ref.stream()

    for doc in docs:
        progress_data = doc.to_dict()
        # print(progress_data)
        return progress_data
    
    return None
def update_expressive_proficiency(child_id):
    """
    Update the expressive proficiency score for a specific child based on
    the average of communication skills and writing skills.

    Args:
        child_id (str): The ID of the child whose expressive proficiency needs to be updated.
    """
    # Retrieve the child's progress tracking documents
    progress_ref = db.collection('progress_tracking').where('child_id', '==', child_id)
    docs = progress_ref.stream()

    found = False
    for doc in docs:
        found = True
        progress_data = doc.to_dict()
        # print(progress_data)
        # Calculate expressive proficiency based on available data
        expressive_proficiency = (progress_data.get('communication_skills', 0) + progress_data.get('writing_skills', 0)) / 2

        # Update expressive proficiency field in Firestore
        doc.reference.update({'expressive_proficiency': expressive_proficiency})

    if not found:
        print(f"No progress tracking found for child ID {child_id}.")

# def get_percentage(child_id):
#     try:
        

#         # Query to retrieve all answers for the given child_id
#         answers_query = db.collection("emotion_recognition").where("child_id", "==", child_id)
#         for answer in answers_query:
#             data = answer.to_dict()
#             print("yyyyyyyyyyyyyyyyyyyyy")
#             print(data)

#         answers = answers_query.stream()

#         right_answers_count = 0
#         total_answers_count = 0

#         # Calculate counts based on matching selected_emotion and correct_emotion
#         for answer in answers:
#             total_answers_count += 1
#             data = answer.to_dict()
#             if data.get("selected_emotion") == data.get("correct_emotion"):
#                 right_answers_count += 1

#         # Calculate the percentage of correct answers
#         if total_answers_count > 0:
#             percentage = int((right_answers_count / total_answers_count) * 100)
#         else:
#             percentage = 0

#         return percentage

#     except Exception as e:
#         print("An error occurred: ", str(e))
#         return None
        
@app.route('/back_index')
@login_required
def back_index():
    # Get child ID from Firestore
    child_id = get_child_id()
    print(child_id)

    print("zzzz")
    
    # Fetch progress and calculate expressive proficiency
    progress = get_child_progress(child_id)

    update_expressive_proficiency(child_id)
    
    # Extract fields from progress data if available
    # print("$$$$$$$$$$")
    # print(get_percentage(child_id))
    # print("$$$$$$$$$$")
    communication_skills = progress.get('communication_skills')
    print(communication_skills)
    writing_skills = progress.get('writing_skills')
    print(writing_skills)
    consistency = progress.get('consistency')
    print(consistency)
    emotions_understanding = progress.get('emotions_understanding')
    print(emotions_understanding)
    expressive_proficiency = progress.get('expressive_proficiency')
    print(expressive_proficiency)
    # else:
    #     return jsonify({'error': 'Progress data not found'}), 404
    
    # Set session flag
    session['flag'] = 0
    
    # Retrieve other activity-related data from Firestore
    count_activities = activities_per_month(child_id)
    activities_count_per_days = get_activities_count_by_day(child_id)
    activities_count_per_week = get_activities_count_by_week(child_id)
    this_month, months, activities_count_per_month = get_activities_count_last_9_months(child_id)
    
    recent_activities = get_recent_activities(child_id)
    # print("$$$$$$$$$$")
    # print(recent_activities)
    # print("$$$$$$$$$$")
    # Render the dashboard template and pass the user data
    return render_template(
        'dashboard.html',
        user=current_user,
        count_activities=count_activities,
        activities_count_per_days=activities_count_per_days,
        activities_count_per_week=activities_count_per_week,
        activities_count_per_month=activities_count_per_month,
        recent_activities=recent_activities,
        months_labels=months,
        communication_skills=communication_skills,
        writing_skills=writing_skills,
        consistency=consistency,
        emotions_understanding=emotions_understanding,
        expressive_proficiency=expressive_proficiency,
        this_month=this_month
    )



# App main route + generic routing
@app.route('/', defaults={'path': 'index'})
@app.route('/<path>')
def index(path):

    #if not current_user.is_authenticated:
    #    return redirect(url_for('login'))

    try:

        return render_template( 'index.html')
    
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500

# Return sitemap
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml')

@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    json_file = 'app/static/emotions.json'
    random_id, random_sentence = get_random_emotion(json_file)
    filename = f"app/static/gen_images/{random_id}.jfif"
    generate_image(API_URL, headers, filename,random_sentence)
    ##session['output'], session['correct_emotion'] = process_emotion_image(API_URL, headers, filename)
    return render_template('index.html')   


@app.route('/radar')
def radar():
    
    group1 = {
        'p1percent': 0,
        'p2percent': 0,
        'p3percent': 0,
        'p4percent': 0,
        'p5percent': 0,
        'p6percent': 0
    }
    return render_template('radar_chart.html',group1=group1)

 
@app.route("/display_image/<filename>")
def display_image(filename):
    return send_file(filename, mimetype='image/jfif')

@app.route('/Essay_correction')
@login_required
def Essay_correction():
    return render_template('EssayCorrection.html')


@app.route('/Text_simplification')
@login_required
def Text_simplification():
    return render_template('Text_simplification.html')

@app.route('/cognipro')
@login_required
def cognipro():
    return render_template('cognipro.html')
@app.route("/generate_text", methods=["POST"])
@login_required
def generate_text():
    try:
        # Get the uploaded image from the request
        image = request.files["image"]
        if image:
            # Read the uploaded file as bytes
            img_stream = BytesIO(image.read())
            # Encode the image bytes to base64
            img_data = base64.b64encode(img_stream.getvalue()).decode('utf-8')
            
            # Save the uploaded image temporarily
            temp_filename = 'temp_image.jpg'
            with open(temp_filename, 'wb') as temp_file:
                temp_file.write(img_stream.getvalue())

            # Upload the image using the genai service
            myfile = genai.upload_file(temp_filename)
            # Generate content using the model
            extracted_text = model.generate_content(
                [myfile, "\n\n", "extract the text from this image"]
            )
            
            # Remove the temporary file
            os.remove(temp_filename)
            print("\n" + "*"*60 + " generate_text : " + extracted_text.text + "*"*60 + "\n")
            # Return the extracted text and the image data to the template
            return render_template("EssayCorrection.html", generated_text=extracted_text.text, imgg=img_data)

    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route("/correct_text", methods=["POST"])
def correct_text():
    activity = "Writing Wizard"
    user_input = request.form["user_input"]

    messages = """Please read the following essay/paragraph written by a child. Your task is to evaluate the writing on various aspects such as clarity, grammar, creativity, structure, and coherence.

    Here is the paragraph: """ + user_input + """

    When giving feedback, use simple and clear language that a child can easily understand. Make sure to provide at least three points in both the Strengths and Areas_for_Improvement sections. Use this JSON schema for your response:
    {
        "grade": str,
        "Strengths": [str, str, str, ...],
        "Areas_for_Improvement": [str, str, str, ...],
        "Encouragement": str
    }
    Here is an example:
    {
        "grade": "A",
        "Strengths": [
            "You used some really great words and your sentences were clear.",
            "Your ideas were creative and interesting.",
            "Your writing stayed on topic and was easy to follow."
        ],
        "Areas_for_Improvement": [
            "Try to use commas to break up long sentences. It will make your writing easier to read.",
            "Work on spelling some tricky words correctly.",
            "Try to add more details to your story to make it even more exciting."
        ],
        "Encouragement": "You're doing a great job! Keep practicing, and you'll get even better!"
    }
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"})

        response = model.generate_content(
            messages,
            generation_config=genai.GenerationConfig(
                temperature=0.4
            )
        )
        print("\n" + "*" * 60 + " correct_text : " + response.text + "*" * 60 + "\n")
        json_response = json.loads(response.text)
        grade = json_response['grade']
        strengths = json_response['Strengths']
        areas_for_improvement = json_response['Areas_for_Improvement']
        encouragement = json_response['Encouragement']

        strengths_text = '\n'.join(strengths)
        areas_for_improvement_text = '\n'.join(areas_for_improvement)
        strengths_text += '\n' + encouragement

        score_grade = calculate_score_grade(grade)
        
        child_id = get_child_id()
        update_writing_skills(child_id, score_grade)

        # Save activity to Firestore
        activities_ref = db.collection('activities').add({
            'activity_type': activity,
            'child_id': child_id,
            'timestamp': get_current_timestamp()
        })

    except Exception as e:
        return f"Error generating assistant reply: {str(e)}"
    
    # Render the HTML template with the variables
    return render_template("EssayCorrection.html", grade=grade, pros=strengths_text, cons=areas_for_improvement_text, user_input=user_input)

def calculate_score_grade(grade):
    """Convert letter grade to numeric score."""
    score_map = {
        "A": 100,
        "B": 80,
        "C": 60,
        "D": 40,
        "E": 20,
        "F": 10
    }
    return score_map.get(grade, 0)




########################### TODO ##########################################

#        child_id = get_child_id()
#        activities = Activities('Storyfy',child_id)
#        activities.save() 


############################################################################
@app.route("/simplify", methods=["GET", "POST"])
def simplify():
    if request.method == "GET":
        return render_template("simplify.html")

   
    user_input = request.form["user_input"]
    generated_text = user_input  # Use the user-provided text as input

    # messages = """you are a kindergarden teacher Simplify the paragraph given so a 5-year-old can understand it make it like a short story and use alot of emojies :  """ + user_input
    
    # messages = """you are a kindergarden teacher Simplify the paragraph given so a 5-year-old can understand it make it like a short story and use alot of emojies make sure to highlight these caracteristics in the story""" + TODO + """ :  this is the paragraph given """ + user_input
    messages = """""you are a kindergarden teacher Simplify the paragraph given so a 5-year-old can understand it make it like a short story of a maximum of 750 and a min of 700 caracters and use alot of emojies:  """ + user_input + """note that the output should be in JSON format : 
        title : str , 
        pages : [str,str]
        where each str contains a maximum of 335 caracters and a min of 300 caractres  of the story
        """
    model = genai.GenerativeModel('gemini-1.5-flash',                              
                                generation_config={"response_mime_type": "application/json"})

    response = model.generate_content(
                messages,
                generation_config=genai.GenerationConfig(
                    temperature=0
                )
            )
    assistant_reply = response.text

    print("\n" + ""*60 + " simplify : " + assistant_reply + ""*60 + "\n")
    json_response = json.loads(assistant_reply)
    session['title'] = json_response["title"]
    session['paragraph1'] = json_response["pages"][0]
    session['paragraph2'] = json_response["pages"][1]
    
    assistant_reply =json_response["pages"][0]+ json_response["pages"][1]
    
    session['current_question_index'] = 0
    return render_template("simplify.html", generated_text=generated_text, corrected_text=assistant_reply)

@app.route("/play_voice", methods=["GET"])
def play_voice():
    generated_text = request.args.get("generated_text")
    filtered_generated_text = keep_only_letters(generated_text)

    # Initialize the Text-to-Speech client with credentials
    client = texttospeech.TextToSpeechClient(credentials=credentials)

    # Input text to synthesize
    text_input = texttospeech.SynthesisInput(text=filtered_generated_text)

    # Voice selection with higher-pitched female voice for child-like quality
    voice = texttospeech.VoiceSelectionParams(
        name="en-US-Journey-F",  
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    # Audio configuration with adjustments for pitch and speaking rate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        pitch=0,              #  (range -20.0 to 20.0)
        speaking_rate=1.0       # speaking rate (normal is 1.0)
    )

    # Synthesize the speech
    response = client.synthesize_speech(input=text_input, voice=voice, audio_config=audio_config)
    output_path = os.path.join(app.root_path, "output.mp3")

    # Save the synthesized audio to an MP3 file
    with open("app\output.mp3", "wb") as out:
        out.write(response.audio_content)
        print("The audio has been saved as 'output.mp3'")

    return send_file(output_path, as_attachment=True)

def separate_sentences(input_list):
    if len(input_list) == 1:
        # Split the single string in the list into sentences based on the newline character ('\n')
        sentences = input_list[0].split('\n')

        # Remove any leading or trailing whitespace from each sentence
        sentences = [sentence.strip() for sentence in sentences]

        return sentences
    else:
        return []
    
def generate_image(API_URL, headers, filename,correct_emotion):
    payload = {
        "inputs": correct_emotion,
        "resolution":512    
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        image_bytes = response.content

        # Save the image to a file
        with open(filename, "wb") as f:
            f.write(image_bytes)
    except requests.exceptions.RequestException as e:
        print({"error": str(e)})
    
def process_emotion_options(API_URL, headers, filename,correct_emotion):
    prompts = "I want you to generate 4 random simple emotion recognition sentences for example: 'A sad lady in red' or 'A happy young girl holding a toy' make the sentences have the same thematic but with diffrent emotions"
    
    messages = f"""you are an emotion recognition model. Generate 4 random simple emotion recognition sentences for example: 'A sad lady in red' or 'A happy young girl holding a toy' take as refrence this sentences  """+ correct_emotion +""" use the same sex the same thematic easy english level but diffrent emotions  .
                    Use this JSON schema:
                    {{
                    "sentences": [str, str, str, str]
                    }}
                    This is the prompt: {prompts}
                """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash',
                                      generation_config={"response_mime_type": "application/json"})
        
        response = model.generate_content(
            messages,
            generation_config=genai.GenerationConfig(
                temperature=0
            )
        )
        print("\n" + "*"*60 + " correct_text : " + response.text + "*"*60 + "\n")
        json_response = json.loads(response.text)
        
        output = json_response["sentences"]
        if output:
            output[random.randint(0, 3)] = correct_emotion
        print(output)
        return output
    
    except Exception as e:
        print(f"Error generating content: {e}")
        return None
    
def get_random_emotion(json_file):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            random_id = random.choice(list(data.keys()))
            random_sentence = data[random_id]
            return random_id, random_sentence
    except (FileNotFoundError, json.JSONDecodeError):
        return None, None
    
# Load the pre-generated emotions data from a JSON file
with open('app/static/new_emotions.json', 'r') as f:
    emotions_data = json.load(f)["emotions"]

def compute_image_hash(image_bytes):
    return hashlib.md5(image_bytes).hexdigest()

# Store the hash of the last generated image
last_image_hash = None

@app.route('/Emotions', methods=['GET', 'POST'])
def Emotions():
    global last_image_hash

    if request.method == 'POST':
        child_id = get_child_id()
        selected_emotion = request.form['selected-choice']
        correct_emotion = request.form['correct_emotion']

        # Update emotions understanding
        update_emotions_understanding(child_id, selected_emotion, correct_emotion)

        # Create a new activity record in Firestore
        activity_data = {
            'activity_type': 'Emotion Recognition',
            'child_id': child_id,
            'timestamp': get_current_timestamp()
        }
        db.collection('activities').add(activity_data)  # Add activity to Firestore

    prompts = "I want you to generate 4 random simple emotion recognition sentences make it so each time the sentences are different from the ones generated before for example: 'A sad lady in red' or 'A happy young girl holding a toy' make the sentences have the same thematic but with different emotions and describe the sentence in a phrase make the phrase easy to understand."
    messages = f"""You are an emotion recognition model. Generate 4 random simple emotion recognition sentences. Use this JSON schema: {{
        "emotions": [
            {{
                "phrase": str,
                "sentence": str
            }},
            {{
                "phrase": str,
                "sentence": str
            }},
            {{
                "phrase": str,
                "sentence": str
            }},
            {{
                "phrase": str,
                "sentence": str
            }}
        ]
    }}
    This is the prompt: {prompts}
    """

    # Generate the content
    try:
        model = genai.GenerativeModel('gemini-1.5-flash',
                                      generation_config={"response_mime_type": "application/json"})
        
        response = model.generate_content(
            messages,
            generation_config=genai.GenerationConfig(
                temperature=0.3
            )
        )
        
    except Exception as e:
        print(f"Error generating content: {e}")
        return redirect(url_for('/Emotions/Test'))

    print(response.text)

    # Parse the response
    emotions_list = json.loads(response.text)
    print("++++++++++++++++++++++++")
    print(emotions_list)

    # Extract the emotion phrases and prompts
    emotion_data = list(emotions_list['emotions'])

    # Pick a random emotion
    random_emotion = random.choice(emotion_data)
    random_phrase = random_emotion['phrase']
    random_prompt = random_emotion['sentence']

    # Function to query the Hugging Face API
    def query_emotions(payload):
        response = requests.post(API_URL_3D, headers=headers, json=payload)
        return response.content

    while True:
        try:
            # Query the API to generate the image based on the random prompt
            image_bytes = query_emotions({"inputs": random_prompt})

            # Compute the hash of the generated image
            current_image_hash = compute_image_hash(image_bytes)

            # Check if the generated image is the same as the last one
            if current_image_hash == last_image_hash:
                print("Duplicate image generated, regenerating...")
                continue

            # Save the generated image to a file
            image = Image.open(io.BytesIO(image_bytes))
            image.save("app/static/generated_image.png")

            # Update the last image hash
            last_image_hash = current_image_hash

            break
        except UnidentifiedImageError as e:
            print(f"Error identifying image: {e}")
        except Exception as e:
            print(f"Error generating or saving image: {e}")

    return render_template('Emotions_Recognition.html', image_filename="../static/generated_image.png", correct_emotion=random_phrase, emotion_data=emotion_data)

@app.route('/Emotions/Test', methods=['GET'])
def EmotionsTest():
    random_emotion = random.choice(emotions_data)
    random_phrase = random_emotion['phrase']
    image_filename = random_emotion['image']

    # Return the template with the selected emotion and image
    return render_template('Emotions_Recognition.html', image_filename=f"../static/gen_images/{image_filename}", correct_emotion=random_phrase, emotion_data=emotions_data)

# @app.route('/update_emotions', methods=['POST'])
# @login_required
# def update_emotions():  
#     selected_emotion=request.form['selected-choice']
#     correct_emotion=request.form['correct_emotion']
#     update_emotions_understanding(get_child_id(), selected_emotion, correct_emotion)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    msg = None
    success = False
    user_ref = db.collection('users').document(current_user.email)
    user = user_ref.get()
    
    print(current_user)
    # Check if the user document exists in Firestore
    if user.exists:
        user_data = user.to_dict()
        child_profile_ref = db.collection('child_profiles').where('user_id', '==', current_user.email).limit(1)
        child_profile_docs = child_profile_ref.stream()
        child_profile = None
        child_doc_ref = None  # Initialize a variable to store the child document reference
        
        for doc in child_profile_docs:
            child_profile = doc.to_dict()  # Store the document data in the variable
            child_doc_ref = db.collection('child_profiles').document(doc.id)  # Get document reference
            break  # Exit after the first match
        print(child_profile)

    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        phone_number = request.form['phoneNumber']
        password = request.form['password']
        child_name = request.form['childname']
        birthdate_str = request.form['childbirthdate']

        # Convert birthdate string to datetime.date object
        try:
            birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
        except ValueError:
            msg = 'Invalid date format. Please use YYYY-MM-DD.'
            return render_template('profile.html', msg=msg, success=success, child_profile=child_profile)

        # Update user profile in Firestore
        update_data = {
            'first_name': first_name,
            'last_name': last_name,
            'phone_number': phone_number,
            'last_modified': get_current_timestamp(),
            
        }
        user_ref.update(update_data)
        current_user.first_name=first_name
        current_user.phone_number=phone_number
        current_user.last_name=last_name
        

        if password:
            try:
                # Retrieve the user by email to get their uid
                user = auth.get_user_by_email(current_user.email)
                
                # Update the password using uid
                auth.update_user(
                    user.uid,
                    password=password
                )
                
                msg = 'Password updated successfully.'
            except auth.UserNotFoundError:
                msg = 'No user record found for the given email.'
            except Exception as e:
                msg = f'Error updating password: {e}'
            if child_doc_ref:  # Check if we found a child profile document
                child_update_data = {
                    'name': child_name,
                    'birthdate': birthdate_str,
                    'last_modified': get_current_timestamp(),
                    'user_id':current_user.email,
                    'child_id':get_child_id()
                }
                child_doc_ref.update(child_update_data)  # Use set to create or update
            else:
                msg = 'No child profile found to update.'
                return render_template('profile.html', msg=msg, success=False, child_profile=child_profile)

            msg = 'Profile updated successfully.'
            success = True
            if child_doc_ref:  # Get the updated child profile data
                child_profile = child_doc_ref.get().to_dict()
            
            return render_template('profile.html', msg=msg, success=False, child_profile=child_profile)

        # Update child profile in Firestore
        if child_doc_ref:  # Check if we found a child profile document
            child_update_data = {
                'name': child_name,
                'birthdate': birthdate_str,
                'last_modified': get_current_timestamp(),
                'user_id':current_user.email,
                'child_id':get_child_id()
            }
            child_doc_ref.update(child_update_data)  # Use set to create or update
        else:
            msg = 'No child profile found to update.'
            return render_template('profile.html', msg=msg, success=False, child_profile=child_profile)

        msg = 'Profile updated successfully.'
        success = True
        if child_doc_ref:  # Get the updated child profile data
            child_profile = child_doc_ref.get().to_dict()

    return render_template('profile.html', msg=msg, success=success, child_profile=child_profile)


# @app.route('/forgetpassword', methods=['GET', 'POST'])
# def forgetpassword():
#     msg = None
#     success = False
#     if request.method == 'POST':
#         email = request.form['email']
#         user = User.query.filter_by(email=email).first()
#         if user:
#             sql = """
#                     UPDATE users
#                     SET password = ?
#                     WHERE email = ?
#                 """
#             all_characters = string.ascii_letters + string.digits + string.punctuation
#             password = ''.join(random.choices(all_characters, k=8))
#             pw_hash = bc.generate_password_hash(password).decode('utf-8')
#             conn = get_db_connection()
#             cursor = conn.cursor()
#             cursor.execute(sql, (pw_hash ,email))
#             conn.commit()
#             msg = 'Password updated successfully.'
#             success = True

#             from_email = "cognipath.ai@gmail.com"
#             from_name = "CogniPath"
#             to_email = email
#             to_name = email
#             subject = "Your New Password"
#             new_password = password
#             text_part = f"Dear user, your new password is: {new_password}. Please change it after logging in."
#             html_part = f'<h3>Dear user,</h3><p>Your new password is: <strong>{new_password}</strong></p><p>Please change it after logging in.</p>'
#             mailjet = Client(auth=(MJ_APIKEY_PUBLIC, MJ_APIKEY_PRIVATE), version='v3.1')
#             # Define the data dictionary
#             data = {
#             'Messages': [
#                 {
#                 "From": {
#                     "Email": from_email,
#                     "Name": from_name
#                 },
#                 "To": [
#                     {
#                     "Email": to_email,
#                     "Name": to_name
#                     }
#                 ],
#                 "Subject": subject,
#                 "TextPart": text_part,
#                 "HTMLPart": html_part
#                 }
#             ]
#             }

#             result = mailjet.send.create(data=data)
#             print(result.status_code)
#             print(result.json())
#             return render_template('forgetpassword.html',msg=msg,success=success)
#         else:
#             msg = 'Email not found.'
#             return render_template('forgetpassword.html',msg=msg,success=success)
#     return render_template('forgetpassword.html',msg=msg,success=success)
        
def keep_only_letters(text):
    # Define the regex pattern to match only alphabetic characters and spaces
    letters_pattern = re.compile("[^a-zA-Z\s!.,?]")
    return letters_pattern.sub('', text)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

chat_history = {}
MAX_HISTORY_SIZE = 5

def save_message(child_id, message):
    if child_id not in chat_history:
        chat_history[child_id] = []
    # Append the new message and limit the size of the history
    chat_history[child_id].append(message)
    if len(chat_history[child_id]) > MAX_HISTORY_SIZE:
        chat_history[child_id].pop(0)  # Remove the oldest message if the limit is exceeded

def get_chat_history(child_id):
    return chat_history.get(child_id, [])
    
@login_required
@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return 'No video file part', 400
    file = request.files['video']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return jsonify({'filename': file.filename}), 200

@app.route('/analyze', methods=['POST'])
async def analyze():
    data = request.json
    video_file_name = os.path.join(app.config['UPLOAD_FOLDER'], data['filename'])
    print(f"Received video file: {video_file_name}")

    # Get the child ID from your function
    child_id = get_child_id()

    # Save the activity in Firestore
    activities_ref = db.collection('activities')
    activity_data = {
        'activity_type': 'Communication',
        'child_id': child_id,
        'video_file_name': video_file_name,
        'timestamp': get_current_timestamp()  # Automatically set the timestamp
    }
    activities_ref.add(activity_data)

    try:
        # Run file upload in a separate thread
        print("Uploading file...")
        video_file = await asyncio.to_thread(genai.upload_file, path=video_file_name)
        print(f"Completed upload: {video_file.uri}")

        # Await file readiness by checking its state in a non-blocking manner
        while video_file.state.name == "PROCESSING":
            print('.', end='', flush=True)
            await asyncio.sleep(10)
            video_file = await asyncio.to_thread(genai.get_file, video_file.name)

        if video_file.state.name == "FAILED":
            raise ValueError("File processing failed.")

        # Retrieve chat history with fallback for new conversations
        chat_history_list = get_chat_history(child_id)
        if chat_history_list:
            chat_history_str = "\n".join(chat_history_list[-10:])  # Use only the last 10 messages
        else:
            chat_history_str = "This is the first conversation with the child."

        # Create the prompt with dynamic content based on chat history
        prompt = f"""You are a helpful assistant dedicated to enhancing the communication skills of children. Your task is to engage the child in a dialogue, focusing on improving their facial expressions, vocabulary, and overall communication skills.

        Below is the chat history from previous interactions with the child, if available. Use this history to guide the conversation naturally and avoid repeating the same topics or greetings. If this is the first conversation, warmly introduce yourself and encourage the child to talk about their interests and recent experiences.

        Chat History:
        {chat_history_str}

        Current Instructions:

        1. Pay attention to the child’s facial expressions and provide encouragement to smile or use positive expressions when appropriate.
        2. When the child uses good vocabulary, acknowledge it and encourage them to use new and varied words.
        3. Offer suggestions for using new words and provide examples to enrich their vocabulary.
        4. Guide the conversation to help the child express their thoughts clearly, ask questions, and respond thoughtfully.
        5. **Avoid repeating common greetings such as "hi" or "hello" if they have already been used in this conversation.** Focus on moving the dialogue forward.
        6. Avoid repeating the same questions or topics that have already been discussed. Encourage the child to talk about new topics or elaborate on different aspects of their experiences.
        7. Keep track of the topics discussed in this conversation and ensure that the dialogue remains dynamic and engaging.
        8. Encourage the child to practice speaking clearly and engage in a meaningful conversation.
        """

        # Choose a Gemini model.
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        # Run the LLM request in a separate thread
        print("Making LLM inference request...")
        response = await asyncio.to_thread(model.generate_content, [video_file, prompt],
                                           request_options={"timeout": 600})

        # Get and save the result
        analysis_result = response.text
        save_message(child_id, analysis_result)

        # Optionally delete file after processing
        # await asyncio.to_thread(genai.delete_file, video_file.name)
        # print(f'Deleted file {video_file.uri}')

        return jsonify({'result': analysis_result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
@app.route('/save_image', methods=['POST'])
def save_image():
    data = request.get_json()
    image_data = data['image']
    
    # Remove the prefix (data:image/png;base64,) from the image data
    image_data = image_data.replace('data:image/png;base64,', '')
    
    # Decode the base64 string
    image_data = base64.b64decode(image_data)
    
    # Define the path where you want to save the image
    image_path = 'app/drawing.jpg'
    
    # Save the image
    with open(image_path, 'wb') as f:
        f.write(image_data)
    
    return jsonify({'message': 'Image saved successfully'}), 200


@app.route('/save_image_file', methods=['POST'])
def save_image_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    if file:
        # Define the path where you want to save the image
        image_path = 'app/file.jpg'
        
        # Save the image
        file.save(image_path)
        
        return jsonify({'message': 'Image saved successfully'}), 200


def Story_with_one_Image(image_path, prompt):
    messages = """
    You are a kindergarten teacher. Make a short story based on the image provided and make it so a 5-year-old can understand it. Make it like a short story with a maximum of 750 and a minimum of 700 characters. Use a lot of emojis.'""" + prompt+"""'. Note that the output should be in JSON format:
    {{
        "title": "str",
        "pages": ["str", "str"]
    }}
    where each str contains a maximum of 335 characters and a minimum of 300 characters of the story.
    """
    model = genai.GenerativeModel(
        'gemini-1.5-flash', generation_config={"response_mime_type": "application/json"}
    )
    image_file = genai.upload_file(image_path)
    print("\nImage read succecfully\n")
    try:
        response = model.generate_content(
            [image_file ,"\n\n",messages], 
            generation_config=genai.GenerationConfig(temperature=0)
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error generating story: {e}")
        return {"title": "Error", "pages": ["An error occurred."]}

def Story_with_two_Images(image_path1, image_path2, prompt):
    messages = f"""
    You are a kindergarten teacher. Make a short story based on the images provided and make it so a 5-year-old can understand it. Make it like a short story with a maximum of 750 and a minimum of 700 characters. Use a lot of emojis. This is the user input: '{prompt}'. Note that the output should be in JSON format:
    {{
        "title": "str",
        "pages": ["str", "str"]
    }}
    where each str contains a maximum of 335 characters and a minimum of 300 characters of the story.
    """
    model = genai.GenerativeModel(
        'gemini-1.5-flash', generation_config={"response_mime_type": "application/json"}
    )
    image_file1 = genai.upload_file(image_path1)
    image_file2 = genai.upload_file(image_path2)
    content = [image_file1 ,"\n\n",image_file2 ,"\n\n",messages]
    try:
        response = model.generate_content(
            content, generation_config=genai.GenerationConfig(temperature=0)
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error generating story: {e}")
        return {"title": "Error", "pages": ["An error occurred."]}

def Story_without_Image(prompt):
    messages = f"""
    You are a kindergarten teacher. Make a short story based only on the user input and make it so a 5-year-old can understand it. Make it like a short story with a maximum of 750 and a minimum of 700 characters. Use a lot of emojis. This is the user input: '{prompt}'. Note that the output should be in JSON format:
    {{
        "title": "str",
        "pages": ["str", "str"]
    }}
    where each str contains a maximum of 335 characters and a minimum of 300 characters of the story.
    """
    model = genai.GenerativeModel(
        'gemini-1.5-flash', generation_config={"response_mime_type": "application/json"}
    )
    content = [messages]
    try:
        response = model.generate_content(
            content, generation_config=genai.GenerationConfig(temperature=0)
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error generating story: {e}")
        return {"title": "Error", "pages": ["An error occurred."]}

@app.route("/drawing", methods=["GET", "POST"])
def drawing():
    time.sleep(1)
    if request.method == "GET":
        return render_template("simplify.html")

    if request.method == "POST":
        user_input = request.form.get("user_input", "")
        generated_text = user_input

        image_path = 'app/file.jpg'
        drawing_path = 'app/drawing.jpg'

        if os.path.exists(image_path) and os.path.exists(drawing_path):
            print(f"{'*' * 100} Image and Drawing {'*' * 100}")
            json_response = Story_with_two_Images(image_path, drawing_path, user_input)
        elif os.path.exists(image_path):
            print(f"{'*' * 100} Image {'*' * 100}")
            json_response = Story_with_one_Image(image_path, user_input)
        elif os.path.exists(drawing_path):
            print(f"{'*' * 100} Drawing {'*' * 100}")
            json_response = Story_with_one_Image(drawing_path, user_input)
        else:
            print(f"{'*' * 100} Prompt {'*' * 100}")
            json_response = Story_without_Image(user_input)

        if os.path.exists(image_path):
            os.remove(image_path)
        if os.path.exists(drawing_path):
            os.remove(drawing_path)

        session['title'] = json_response["title"]
        session['paragraph1'] = json_response["pages"][0]
        session['paragraph2'] = json_response["pages"][1] if len(json_response["pages"]) > 1 else ""
        session['current_question_index'] = 0

        assistant_reply = json_response["pages"][0] + (json_response["pages"][1] if len(json_response["pages"]) > 1 else "")
        print(f"{'*' * 100} Story : {assistant_reply} {'*' * 100}")
        
        child_id = get_child_id()
        print("child id : ", child_id)
        activities_ref = db.collection('activities')
        activity_data = {
            'activity_type': 'Storyfy',
            'child_id': child_id,
            'timestamp': get_current_timestamp()  # Automatically set the timestamp
        }
        paragraph1 = session['paragraph1']
        paragraph2 = session['paragraph2']
        
        outputfile1 = "app/static/storyImage1.png"
        outputfile2 = "app/static/storyImage2.png"
        print("*"*60 + " generating Image 1 " + "*"*60)
        generate_image_and_save(paragraph1,outputfile1)
        print("*"*60 + " generating Image 2 " + "*"*60)
        generate_image_and_save(paragraph2,outputfile2)
        try:
            activities_ref.add(activity_data)
            print(f"Activity 'Storyfy' for child_id '{child_id}' recorded successfully.")
        except Exception as e:
            print(f"Error recording activity: {str(e)}")
        
        
        return render_template("simplify.html", generated_text=generated_text, corrected_text=assistant_reply)

def generate_quiz_options(story):
    # Update prompt to generate 5 questions
    prompts = f"I want you to generate 5 questions and 5 options for each question about this story. Each set of options should include 1 correct answer and 4 wrong answers, suitable for a 5-year-old. This is the story: {story}"
    
    messages = f"""You are a quiz generator.
                    Use this JSON schema:
                    {{
                    "questions": [
                        {{
                            "question": str,
                            "wrong_answers": [str, str, str, str],
                            "correct_answer": str
                        }},
                        {{
                            "question": str,
                            "wrong_answers": [str, str, str, str],
                            "correct_answer": str
                        }},
                        {{
                            "question": str,
                            "wrong_answers": [str, str, str, str],
                            "correct_answer": str
                        }},
                        {{
                            "question": str,
                            "wrong_answers": [str, str, str, str],
                            "correct_answer": str
                        }},
                        {{
                            "question": str,
                            "wrong_answers": [str, str, str, str],
                            "correct_answer": str
                        }}
                    ]
                    }}
                    This is the prompt: {prompts}
                """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash',
                                      generation_config={"response_mime_type": "application/json"})
        
        response = model.generate_content(
            messages,
            generation_config=genai.GenerationConfig(
                temperature=0
            )
        )
        print("\n" + "*"*60 + " quiz : " + response.text + "*"*60 + "\n")
        json_response = json.loads(response.text)
        
        output = json_response.get("questions", [])
        if len(output) == 5:
            for question in output:
                # Ensure one of the wrong answers is the correct answer
                correct_answer = question["correct_answer"]
                if correct_answer not in question["wrong_answers"]:
                    question["wrong_answers"][random.randint(0, 3)] = correct_answer
        
        print(output)
        return output
    
    except Exception as e:
        print(f"Error generating content: {e}")
        return None
    
    
from flask import session, request, redirect, url_for, render_template
from firebase_admin import firestore
import time

@app.route('/Quiz_page', methods=['GET', 'POST'])
def Quiz_page():
    if request.method == 'POST':
        if 'questions' not in session:
            # On the first request, generate questions
            story = request.form.get('story')
            questions = generate_quiz_options(story=story)
            if questions:
                session['questions'] = questions
                session['current_question_index'] = 0
        else:
            # On subsequent requests, update the question index
            submitted_choice = request.form.get('selected-choice', '')        
            current_question = session['questions'][session['current_question_index']]
            correct_answer = current_question['correct_answer']
            
            # Save the quiz attempt to Firestore
            quiz_attempt_data = {
                'child_id': get_child_id(), 
                'question_id': session['current_question_index'], 
                'selected_answer': submitted_choice, 
                'correct_answer': correct_answer,
                'timestamp': get_current_timestamp() # Automatically set the timestamp
            }
            
            # Save quiz attempt to Firestore
            try:
                db.collection('quiz_attempts').add(quiz_attempt_data)
                print("Quiz attempt recorded successfully.")
            except Exception as e:
                print(f"Error recording quiz attempt: {str(e)}")

            if submitted_choice == correct_answer:
                print("Correct")
            else:
                print("Wrong")
            
            # Increment the question index
            session['current_question_index'] += 1
            time.sleep(1.5)

            # Check if there are more questions
            if session['current_question_index'] >= len(session['questions']):
                session.pop('questions')
                session['current_question_index'] = 0
                
                child_id = get_child_id()
                activities_ref = db.collection('activities')
                activity_data = {
                    'activity_type': 'Quiz',
                    'child_id': child_id,
                    'timestamp': get_current_timestamp()  # Automatically set the timestamp
                }
                
                # Log the activity in Firestore
                try:
                    activities_ref.add(activity_data)
                    print("Activity 'Quiz' recorded successfully.")
                except Exception as e:
                    print(f"Error recording activity: {str(e)}")
                
                return redirect(url_for('quiz_end'))

    elif request.method == 'GET':
        if 'questions' not in session:
            # No questions in session, redirect to start
            return redirect(url_for('start_quiz'))

    # Retrieve the current question based on the index
    current_index = session.get('current_question_index', 0)
    questions = session.get('questions', [])
    if current_index < len(questions):
        current_question = questions[current_index]
        session['wrong_answers'] = current_question["wrong_answers"]
        session['correct_answer'] = current_question["correct_answer"]
        session['question'] = current_question["question"]
    else:
        session.pop('questions')
        session['current_question_index'] = 0
        return redirect(url_for('quiz_end'))

    return render_template('quiz.html')


@app.route('/quiz_end')
def quiz_end():
    # Logic for ending the quiz
    return render_template('simplify.html')


def generate_image_and_save(prompt, output_file):
    try:
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")

        images = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            language="en",
            aspect_ratio="1:1",
            safety_filter_level="block_some"
        )

        # Check if any images were returned
        if images:
            images[0].save(location=output_file, include_generation_parameters=False)
            print(f"Created output image using {len(images[0]._image_bytes)} bytes in {output_file}")
        else:
            print("No images returned from the model.")
            return render_template('simplify.html')  # Render the template if no image is generated

    except Exception as e:
        print(f"An error occurred: {e}")
        # Render the specified template if an error occurs
        return render_template('simplify.html')

