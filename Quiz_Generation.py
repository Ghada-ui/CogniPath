from librabies_to_import import *

def generate_quiz_options(story):
    # Update prompt to generate 5 questions
    prompts = f"I want you to generate 5 questions and 5 options for each question about this story. Each set of options should include 1 correct answer and 4 wrong answers, suitable for a 5-year-old. This is the story: {story}"
    
    messages = f"""You are a quiz generator.
                    Use this JSON schema:
                    {{
                    "questions": [
                        {{
                            "question": str,
                            "options": [str, str, str, str],
                            "correct_answer": str
                        }},
                        {{
                            "question": str,
                            "options": [str, str, str, str],
                            "correct_answer": str
                        }},
                        {{
                            "question": str,
                            "options": [str, str, str, str],
                            "correct_answer": str
                        }},
                        {{
                            "question": str,
                            "options": [str, str, str, str],
                            "correct_answer": str
                        }},
                        {{
                            "question": str,
                            "options": [str, str, str, str],
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
                if correct_answer not in question["options"]:
                    question["options"][random.randint(0, 3)] = correct_answer
        
        print(output)
        return output
    
    except Exception as e:
        print(f"Error generating content: {e}")
        return None
    
# def pass_quiz(story):
#     quiz_questions = generate_quiz_options(story)
#     if not quiz_questions:
#         print("Failed to generate quiz questions. Please try again.")
#         return

#     score = 0
#     total_questions = len(quiz_questions)

#     for i, question in enumerate(quiz_questions, 1):
#         print(f"\nQuestion {i}: {question['question']}")
#         for j, option in enumerate(question['options'], 1):
#             print(f"  {j}. {option}")
        
#         while True:
#             try:
#                 answer = int(input("Enter your answer (1-4): "))
#                 if 1 <= answer <= 4:
#                     break
#                 else:
#                     print("Please enter a number between 1 and 4.")
#             except ValueError:
#                 print("Please enter a valid number.")

#         if question['options'][answer - 1] == question['correct_answer']:
#             print("Correct!")
#             score += 1
#         else:
#             print(f"Wrong. The correct answer is: {question['correct_answer']}")

#     print(f"\nQuiz completed! Your score: {score}/{total_questions}")
#     return score, total_questions

story = """Story  : Once upon a time, there was a little yellow duck 🐥 
                    who lived in a pond. He loved to swim and splash in the water. 
                    One day, he saw a shiny red car 🚗 driving by. The car was so fast!
                    The duck wanted to go for a ride, but he didn't know how. 
                    He waddled over to the car and said, "Excuse me, Mr. Car, 
                    can I have a ride?" The car stopped and said, "I'm sorry, 
                    little duck, but I can't take you for a ride. I'm a car, not
                    a boat!" The duck was sad. He wanted to go for a ride so badly.
                    He thought and thought, and then he had an idea! He hopped into
                    the car's trunk and closed the lid. He was so excited! He thought
                    he was going for a ride. The car started driving again. The 
                    duck was bouncing around in the trunk. He was having so much 
                    fun! But then, the car stopped suddenly. The duck was confused.
                    He opened the trunk and looked out. He was in a parking lot! The
                    car was gone! The duck was scared. He didn't know what to do. He 
                    waddled around the parking lot, looking for the car. But the car 
                    was nowhere to be found. The duck was sad and lonely. He missed his
                    pond. He missed his friends. He wanted to go home. Just then, he saw
                    a little girl 👧 walking by. She saw the duck and smiled. "Hello, 
                    little duck!" she said. "Are you lost?" The duck nodded. The girl 
                    picked him up and took him back to the pond. The duck was so happy
                    to be home! He thanked the girl and went for a swim. He learned that
                    it's important to be careful and not to go on adventures without asking 
                    his parents first. 🦆🚗"""

generate_quiz_options(story)







