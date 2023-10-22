personality_tests = {
    "questions": [
        {
            "question": "When planning a vacation, you prefer to:",
            "options": {
                "a": "Relax on a beach with a good book.",
                "b": "Explore a bustling city with lots of culture.",
                "c": "Go on an adventurous hiking or camping trip.",
                "d": "Visit historical sites and museums."
            }
        },
        {
            "question": "What's your favorite way to spend a Saturday evening?",
            "options": {
                "a": "Hosting a dinner party with friends.",
                "b": "Going to a live concert or theater show.",
                "c": "Trying out a new extreme sport or outdoor activity.",
                "d": "Watching a documentary or reading a non-fiction book."
            }
        },
        {
            "question": "Which of the following words best describes you?",
            "options": {
                "a": "Social",
                "b": "Creative",
                "c": "Adventurous",
                "d": "Intellectual"
            }
        },
        {
            "question": "Your ideal job would involve:",
            "options": {
                "a": "Working with people and helping them.",
                "b": "Expressing your creativity and imagination.",
                "c": "Being physically active and outdoors.",
                "d": "Researching and analyzing data."
            }
        },
        {
            "question": "In your free time, you enjoy:",
            "options": {
                "a": "Cooking and trying new recipes.",
                "b": "Painting, writing, or making music.",
                "c": "Playing sports or engaging in physical activities.",
                "d": "Solving puzzles and playing strategic games."
            }
        }
    ],
    "scoring": {
        "a": 1,
        "b": 2,
        "c": 3,
        "d": 4
    },
    "results": {
        "5-8": "Social",
        "9-12": "Creative",
        "13-16": "Adventurous",
        "17-20": "Intellectual"
    }
}


personality_details = {
    "Social": "You are outgoing and enjoy spending time with friends and meeting new people. You often excel in roles that involve working with others, such as customer service, teaching, or counseling.",
    "Creative": "You are imaginative and enjoy expressing yourself through art, music, writing, or other creative outlets. You often find fulfillment in creative professions like writing, painting, or music.",
    "Adventurous": "You seek excitement and love physical challenges. You are often drawn to activities like sports, hiking, and travel. Careers that involve adventure and physical activity may be appealing to you.",
    "Intellectual": "You have a strong desire to learn and solve complex problems. You are often drawn to fields like science, research, and data analysis. You enjoy reading, puzzles, and strategic games."
}


def user_personality_details(personality):
    return personality_details.get(personality, "Personality details not available.")

# Example usage:
personality_result = "Social Personality"  # Replace with the actual user's personality result
details = user_personality_details(personality_result)
print("You are:", details)



def check_user_choice(choice):
    for key, value in personality_tests["scoring"].items():
        if int(choice) == value:
            return True  
    return False  

def user_personality(score):
    score = int(score)
    results = personality_tests["results"]
    for key, value in results.items():
        min_score, max_score = map(int, key.split('-'))
        if min_score <= (score) <= max_score:
            return value
    return None

def is_user_data_complete(user_data):
    # Check if any value in the user_data dictionary is None
    return all(value is not None for value in user_data.values())

