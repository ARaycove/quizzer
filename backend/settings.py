# This module holds functions relating to the updating of settings and configurations
# Currently we need to be able to update the quiz length, and subject weighting for quizzes
import json
from lib import helper

def create_first_time_settings_json():
    settings = {}
    settings["quiz_length"] = 35
    settings["time_between_revisions"] = 1.2
    settings["due_date_sensitivity"] = 12
    settings["vault_path"] = ["enter/path/to/obsidian/vault"]
    settings["desired_daily_questions"] = 135
    with open("json_data/settings.json", "w+") as f:
        json.dump(settings, f)

def initialize_settings_json():
    '''creates settings.json if it doesn't exist'''
    try:
        settings = helper.get_settings_data()
        print("settings.json exists")
    except FileNotFoundError:
        print("settings.json not found")
        print("creating settings.json with default values")
        settings = create_first_time_settings_json()

def initialize_desired_daily_questions_settings():
    settings = helper.get_settings_data()
    # if the settings does not exist set it to 120
    # else if the settings does exist we do nothing.
    if settings.get("desired_daily_questions") == None:
        settings["desired_daily_questions"] = 120
        helper.update_settings_json(settings)


            
def update_setting(key, value):
    '''
    takes a key (setting) and a new value to be updated
    checks to see if the value is appropriate, then updates settings.json with the new value if appropriate
    '''
    # First load in settings.json
    settings_data = helper.get_settings_data()
    bad_value = False
    # Check functions for specific settings:
    if key == "quiz_length": # For now only quiz_length needs to be an integer, ie you can't have a fractional number of questions
        print("key is quiz_length")
        try:
            value = float(value)
            value = int(value)
        except ValueError:
            bad_value = True
    elif key == "vault_path":
        print("key is vault_path")
        if ("/" in value) or ("\\" in value):
            print("valid directory")
        else:
            print("invalid directory")
            bad_value = True
            return f"vault_path must be a directory path."
    elif key == "time_between_revisions":
        value = float(value)
    else:
        try:
            value = int(value)
        except ValueError:
            bad_value = True
    # Check if passed key is in the settings, if setting does not exist return an error
    if (key in settings_data) and bad_value == False:
        settings_data[key] = value
        helper.update_settings_json(settings_data)
        return f"Updated setting:{key} to {settings_data[key]}"
    else:
        print("That setting does not exist in settings file")
        return "That setting does not exist in settings file"
    
def get_subjects():
    '''returns a set of subjects based on the subject key in questions.json
    lets you know all the subjects that exist in questions.json'''
    data = helper.get_question_data()
    subject_set = set([])
    for i in data:
        if "subject" in i and i["subject"] is not None:
            temp_list = i["subject"]
            for i in temp_list:
                subject_set.add(i)
    return subject_set

def initialize_settings_json_keys():
    '''Checks settings keys and initializes each key if it doesn't exist'''
    # One long function avoids the need to open the file and write to it multiple times over, more efficient, less readable
    # Load all data into memory first:
    subject_set = get_subjects()
    settings = helper.get_settings_data()
    # Setting check, redundancy
    if settings.get("time_between_revisions") == None:
        settings["time_between_revisions"] = 1.20
        print("Initializing time between revisions setting key")
    else:
        print("time_between_revisions setting already exists")
    # Setting check    
    if settings.get("due_date_sensitivity") == None:
        print("due_date_sensitivity setting does not exist, initializing to 24")
        settings["due_date_sensitivity"] = 12
    else:
        print("due_date_sensitivity settings exists")
    # Setting check
    if settings.get("vault_path") == None:
        settings["vault_path"] = ["/home/karibar/Documents/Education"]   
    for i in subject_set:
        ##################################################
        # initialize subject weighting
        if settings.get(f"subject_{i}_weight") == None:
            print(f"key subject_{i}_weight missing, initializing key value to 1")
            settings[f"subject_{i}_weight"] = 1
        else:
            print(f"subject_{i}_weight exists in settings.json")
        ##################################################
        # initialize subject priority
        if settings.get(f"subject_{i}_priority") == None:
            print(f"key subject_{i}_weight missing, initializing key value to 1")
            settings[f"subject_{i}_priority"] = 9
        else:
            print(f"subject_{i}_priority exists in settings.json")
        
    helper.update_settings_json(settings)
    initialize_desired_daily_questions_settings()