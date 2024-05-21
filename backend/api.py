# Installation of quizzer:
# pip3 install starlette
# pip3 install uvicorn
# pip install "uvicorn[standard]"
# pip install pydantic
# pip install fastapi

#How to run the server component
from typing import Union
from fastapi import FastAPI
import json
import uvicorn
from lib import helper
import initialize
import stats
import settings
import questions
import quiz_functions
# To start API

app = FastAPI()

# def launch_api():
#     subprocess.run([])
#     uvicorn.run("api:app", host="127.0.0.1", port=8000)
#############################################################################
#############################################################################
#############################################################################
# these two functions are just for example/reference
@app.get("/")
def read_root():
	data = {"Hello": "I see you reading me, this is the root directory of the api server!"}
	return data

# example (I'll be reading from this example for the update score call)
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    # Try and get an Ooga booga! from the api server, for practice.
	if q == "test" and item_id == 5:
		response = "Ooga booga!"
	else:
		response = "try again"
	return response
#############################################################################
#############################################################################
#############################################################################
@app.get("/populate_quiz")
def return_question_list():
    '''
    returns a list of questions to be presented to the user
    '''
    question_list, returned_sorted_questions = quiz_functions.populate_question_list()
    return {"question_list": question_list, "sorted_questions": returned_sorted_questions}

#FIXME add in a add_question_function and api_call


@app.get("/add_question")
# function stub


@app.get("/update_score/{status, file_name}")
def question_answer_update_score(status: str, id: str):
    '''
    Use to update the score for the question
    options are "correct" or "incorrect"
    '''
    response = f"updated question with id {id}"
    if status == "correct":
        questions.update_score(status, id)
    elif status == "incorrect":
        questions.update_score(status, id)
    else:
        response = "Please enter a valid status, 'correct' or 'incorrect'"
    return response

@app.get("/update_setting/{key, value}")
def update_a_setting_value(key=str, value=str):
    '''
    Used to update a value located in the settings.json file
    Please note I did not actually use this in the current front-end version
    '''
    print(key)
    print(value)
    response = settings.update_setting(key, value)
    return response

@app.get("/initialize_quizzer")
def initialization(): # This function will contain all the initialization functions from various modules:
    '''
    calls the initialization process
    alternatively you can just call initialization directly from the initialize module
    '''
    initialize.initialize_quizzer()
#############################################################################
#############################################################################
#############################################################################
@app.get("/get_subjects")
def api_get_subjects():
	'''
    Returns a set of all subjects in quizzer
    I forget why this was needed, but here you go
    '''
	subjects = settings.get_subjects()
	return subjects

@app.get("/get_subject_settings") 
#FIXME, this function was my first attempt at creating a menu with an option to display all settings that can be changed
# alternatively you can just use the new get_settings_data call to get a list of all settings.
def get_subject_settings():
    '''
    returns just a list of the subject specific questions for the priority and weight system
    '''
    root = "http://127.0.0.1:8000/"
    settings_menu = True
    subject_settings = {}
    settings_data = helper.get_settings_data()
    query = root + "get_subjects"
    subjects = settings.get_subjects()
    subjects = list(subjects)
    subjects = sorted(subjects)
    for i in range(0, (len(subjects)-1)):
        for key, value in settings_data.items():
            if subjects[i] in key:
                subject_settings[key] = value
    return subject_settings
############################################################
@app.get("/get_stats_data")
def get_stats_data_api():
    stats_data = helper.get_stats_data()
    return stats_data

@app.get("/get_settings_data")
def get_settings_data_api():
    settings_data = helper.get_settings_data()
    return settings_data

@app.get("/get_question_data")
def get_question_data_api():
    question_data = helper.get_question_data()
    return question_data

##########################################################################################
# Quinn
# The following functions are deprecated and aren't intended to be used, I left them in here anyway so you can see the old crap I coded in


@app.get("/get_media_path/{media_file_name}")
#FIXME, every piece of media should now be in the quizzer directory media/
# obsidian integration scans for media and copy pastes them into the media/ directory
#FIXME deprecated, all paths now exist in media_files/, no need to fetch the paths
# all media files related to the questions should exist in the media_files/ directory so that the program works when the entire directory is moved elsewhere
# def return_file_path(media_file_name=str):
#     '''Takes a file name string as input, returns the location of the media'''
#     print(len(media_paths["file_paths"]))
#     for path in media_paths["file_paths"]: # Iterate through the existing media
#         if str(path).endswith(media_file_name):
#             return path		

#FIXME, this call is deprecated, just use the get_stats_data api call instead
@app.get("/get_average_questions_per_day")
def get_average_questions_per_day():
    # Make sure to update stats.json before returning data
    stats.update_stats()
    stats_data = helper.get_stats_data
    average_questions = stats_data["average_questions_per_day"]
    return average_questions