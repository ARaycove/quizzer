import os
import json
from datetime import datetime, timedelta
from lib import helper
import settings
import questions
import stats
from integrations import obsidian
import shutil
def count_files_in_directory(directory_path):
    try:
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"The provided path '{directory_path}' is not a directory.")
        items = os.listdir(directory_path)
        files = [item for item in items if os.path.isfile(os.path.join(directory_path, item))]
        return len(files)
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0
def return_file_path(media_file_name=str):
    '''Takes a file name string as input, returns the location of the media'''
    with open("json_data/obsidian_media_paths.json", "r") as f:
        media_paths = json.load(f)
    for path in media_paths["file_paths"]: # Iterate through the existing media
        if str(path).endswith(media_file_name):
            return path		
def move_file_to_media(file_name):
    file_path = return_file_path(file_name)
    src = file_path
    dst = "media_files/"
    shutil.copy2(src, dst)
    
def copy_media_into_local_dir():
    question_data = helper.get_question_data()
    for qa in question_data:
        try:
            if qa["question_image"] != None:
                move_file_to_media(qa["question_image"])
        except (TypeError, shutil.SameFileError):
            pass
        try:
            if qa["question_audio"] != None:
                move_file_to_media(qa["question_audio"])
        except (TypeError, shutil.SameFileError):
            pass
        try:

            if qa["question_video"] != None:
                move_file_to_media(qa["question_video"])
        except (TypeError, shutil.SameFileError):
            pass
        try:        
            if qa["answer_image"] != None:
                move_file_to_media(qa["answer_image"])
        except (TypeError, shutil.SameFileError):
            pass
        try:        
            if qa["answer_audio"] != None:
                move_file_to_media(qa["answer_video"])
        except (TypeError, shutil.SameFileError):
            pass
        

def initialize_quizzer():
    '''
    Main Entry Point for program,
    calls health check functions
    initializes json data if necessary
    launches backend-server
    launches front-end interface
    '''
    # To initialize the program:
    timer_start = datetime.now()
    print("Checking if json files exist")
    settings.initialize_settings_json()
    questions.initialize_questions_json()
    stats.initialize_stats_json()
    settings_data = helper.get_settings_data()
    vault_path = settings_data["vault_path"]
    print("#" * 25)
    print("Now checking integrations:")
    print("Scanning for Obsidian data")
    # Obsidian integration
    if vault_path != ["enter/path/to/obsidian/vault"]: #this is the default value of vault path in the settings, requires the user to initiate the integration
        #FIXME needs proper logic to check if Obsidian is installed on the current device and auto-detect these directories instead of having the user manually find and enter them.
        try:
            obsidian_directories = obsidian.get_all_subdirectories()
            print(len(obsidian_directories), "obsidian sub_directories")
            obsidian.scan_directory(vault_path)
            obsidian.update_questions_json()
            copy_media_into_local_dir()
        except:
            pass
    else:
        print("Enter a filepath for your obsidian vault")
    # Health check question objects
    questions.initialize_question_metric_keys_if_they_dont_exist()
    questions.calculate_average_shown()
    stats.update_stats()
    stats_data = helper.get_stats_data()
    print(stats_data)
    print(count_files_in_directory("media_files/"), "media files loaded")
    print("#" * 25)
    # Initialize settings keys (subject keys)
    settings.initialize_settings_json_keys()
    
    # End Initialization
    timer_end = datetime.now()
    elapsed_time = timer_end - timer_start
    total_seconds = elapsed_time.total_seconds()
    minutes, seconds = divmod(total_seconds, 60)
    print(f"Success: initialization takes {int(minutes)} minutes and {int(seconds)} seconds.")
