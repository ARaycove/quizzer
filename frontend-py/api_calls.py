import requests
import json
from urllib.parse import quote

def get_subject_settings():
    root = "http://127.0.0.1:8000/"
    query = root + "get_subject_settings"
    data = requests.get(f"{query}")
    subject_settings = data.json()
    return subject_settings

def get_absolute_media_path(media_file_name):
    # strip check, if the path is surrounded by brackets, strip the brackets off before passing
    if media_file_name.startswith("[["):
        media_file_name = media_file_name[2:]
    if media_file_name.endswith("]]"):
        media_file_name = media_file_name[:-2]
    media_file_name = quote(media_file_name) #encode file name for comms to server api
    first_part = "http://127.0.0.1:8000/get_media_path/"
    query = first_part + media_file_name
    data = requests.get(f"{query}")
    data = data.json()
    absolute_file_path = data
    if absolute_file_path == None:
        print("none")
        absolute_file_path = ""
    return absolute_file_path
def populate_quiz():
    root = "http://127.0.0.1:8000/"
    command_pop_quiz = "populate_quiz"
    data = requests.get(f"{root}{command_pop_quiz}")
    print("find data:$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", data)
    if str(data) == "<Response [500]>":
        question_list = [{"file_name": ".ERROR.md", "file_path": "ERROR.md", "type": "question", "subject": ["ERROR_NO_QUESTIONS"], "related": ["ERROR_NO_QUESTIONS", "ERROR"], "question_text": "You have no questions", "revision_streak": 11, "last_revised": "2024-03-23 15:55:47", "next_revision_due": "2024-03-27 21:19:41", "answer_text": "Error", "question_media": "Error", "answer_media": "Error", "in_circulation": True}]
        returned_sorted_questions = 5
        return question_list, returned_sorted_questions
    else:
        data = data.json()
        question_list = data["question_list"]
        returned_sorted_questions = data["sorted_questions"]
        return question_list, returned_sorted_questions

def update_score(answer, file_name):
    encoded_file_name = quote(file_name)
    if answer == "correct":
        first_part = "http://127.0.0.1:8000/update_score/{status, file_name}?status=correct&file_name="
        query = first_part + encoded_file_name
        requests.get(f"{query}")
    elif answer == "incorrect":
        first_part = "http://127.0.0.1:8000/update_score/{status, file_name}?status=incorrect&file_name="
        query = first_part + encoded_file_name
        requests.get(f"{query}")        
    else:
        print("Something went wrong")

def initialize_quizzer():
    root = "http://127.0.0.1:8000/"
    command_initialize_quizzer = "initialize_quizzer"
    requests.get(f"{root}{command_initialize_quizzer}")
    
def get_subjects():
    pass
#########################################
# Stats Calls
def get_average_questions_per_day():
    root = "http://127.0.0.1:8000/"
    command_get_average_quetions_per_day = "get_average_questions_per_day"
    data = requests.get(f"{root}{command_get_average_quetions_per_day}")
    data = data.json()
    return data