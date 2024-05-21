import json
from datetime import datetime, date, timedelta
import mimetypes
import os
# This file contains library functions used across all modules
# also any miscellaneous functions are also stored here if not specific to a particular goal
#   for example, is_media just checks if a filetype is a media file or not

##################################################################################################
##################################################################################################
##################################################################################################
# Read from database functions
def get_question_data():
    with open("json_data/questions.json", "r") as f:
        questions = json.load(f)
    return questions

def get_stats_data():
    with open("json_data/stats.json", "r") as f:
        stats = json.load(f)
    return stats

def get_settings_data():
    with open("json_data/settings.json") as f:
        settings = json.load(f)
    return settings

def get_obsidian_data():
    with open("json_data/obsidian_data.json", "r") as f:
        obsidian_data = json.load(f)
    return obsidian_data

def get_obsidian_media_paths():
    with open("json_data/obsidian_media_paths.json", "r") as f:
        obsidian_media_paths = json.load(f)
    return obsidian_media_paths

##################################################################################################
##################################################################################################
##################################################################################################
# Write to database functions
def update_obsidian_data_json(data):
    with open("json_data/obsidian_data.json", "w+") as f:
        json.dump(data, f)
        
def update_obsidian_media_paths(data):
    with open("json_data/obsidian_media_paths.json", "w+") as f:
        json.dump(data, f)

def update_questions_json(data):
    with open("json_data/questions.json", "w") as f:
        json.dump(data, f)
        
def update_stats_json(data):
    with open("json_data/stats.json", "w") as f:
        json.dump(data, f)
        
def update_settings_json(data):
    with open("json_data/settings.json", "w") as f:
        json.dump(data, f)
##################################################################################################
##################################################################################################
##################################################################################################
# Other functions

def stringify_date(datetime_object):
    '''
    take a datetime object and convert to a string
    '''
    string_object = datetime_object.strftime("%Y-%m-%d %H:%M:%S")
    return string_object
def convert_to_datetime_object(string: str):
    '''
    take a valid string and turn it into a datetime object
    '''
    datetime_object = datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
    return datetime_object

def is_media(file):
    mimestart = mimetypes.guess_type(file)[0]
    if mimestart != None:
        mimestart = mimestart.split('/')[0]
        if mimestart in ['audio', 'video', 'image']:
            return True
    return False



