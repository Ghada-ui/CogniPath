from librabies_to_import import *

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
    

def Story_with_Drawing_Or_Images(Folder_path, prompt):
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
    image_files = []
    for filename in os.listdir(Folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            print(f"processing : {filename}")
            image_path = os.path.join(Folder_path, filename)
            image_files.append(genai.upload_file(image_path))
    print(f"\n{len(image_files)} image(s) read successfully\n")
    try:
        response = model.generate_content(
            image_files + ["\n\n", messages],
            generation_config=genai.GenerationConfig(temperature=0)
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error generating story: {e}")
        return {"title": "Error", "pages": ["An error occurred."]}
    

def Story_with_Drawings_And_Images(Drawing_Folder, Images_Folder, prompt):
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
    drawing_files = []
    for filename in os.listdir(Drawing_Folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            print(f"processing Drawing : {filename}")
            drawing_path = os.path.join(Drawing_Folder, filename)
            drawing_files.append(genai.upload_file(drawing_path))
    print(f"\n{len(drawing_files)} drawing(s) read successfully\n")
    image_files = []
    for filename in os.listdir(Images_Folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            print(f"processing image : {filename}")
            image_path = os.path.join(Images_Folder, filename)
            image_files.append(genai.upload_file(image_path))
    content = drawing_files + image_files + ["\n\n", messages]
    try:
        response = model.generate_content(
            content, generation_config=genai.GenerationConfig(temperature=0)
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error generating story: {e}")
        return {"title": "Error", "pages": ["An error occurred."]}



def Generate_Story(user_input):
        image_Folder = 'app/Images'
        drawing_Folder = 'app/Drawings'

        # Create the folders if they don't exist
        os.makedirs(image_Folder, exist_ok=True)
        os.makedirs(drawing_Folder, exist_ok=True)

        if bool(os.listdir(image_Folder)) and bool(os.listdir(drawing_Folder)):
            print(f"{'*' * 100} Image and Drawing {'*' * 100}")
            json_response = Story_with_Drawings_And_Images(image_Folder, drawing_Folder, user_input)
        elif bool(os.listdir(image_Folder)):
            print(f"{'*' * 100} Image {'*' * 100}")
            json_response = Story_with_Drawing_Or_Images(image_Folder, user_input)
        elif bool(os.listdir(drawing_Folder)):
            print(f"{'*' * 100} Drawing {'*' * 100}")
            json_response = Story_with_Drawing_Or_Images(drawing_Folder, user_input)
        else:
            print(f"{'*' * 100} Prompt {'*' * 100}")
            json_response = Story_without_Image(user_input)

        if os.listdir(image_Folder):
            for file in os.listdir(image_Folder):
                file_path = os.path.join(image_Folder, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        if bool(os.listdir(drawing_Folder)):
            for file in os.listdir(drawing_Folder):
                file_path = os.path.join(drawing_Folder, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        
        # Parse json_response if it's a string
        if isinstance(json_response, str):
            json_response = json.loads(json_response)

        title = json_response.get("title", "Untitled")
        
        # Check if 'pages' key exists, if not, use 'paragraph1' and 'paragraph2'
        if "pages" in json_response:
            paragraph1 = json_response["pages"][0] if json_response["pages"] else ""
            paragraph2 = json_response["pages"][1] if len(json_response["pages"]) > 1 else ""
        else:
            paragraph1 = json_response.get("paragraph1", "")
            paragraph2 = json_response.get("paragraph2", "")

        current_question_index = 0

        assistant_reply = paragraph1 + (paragraph2 if paragraph2 else "")
        print(f"{'*' * 100} Story : {assistant_reply} {'*' * 100}")            
        
        return json.dumps({
            "title": str(title),
            "paragraph1": str(paragraph1),
            "paragraph2": str(paragraph2),
            "current_question_index": current_question_index
        })
        
        
        
Generate_Story("the yellow duck and the red car")
