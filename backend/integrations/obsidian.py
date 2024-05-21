from lib import helper
import json
import ruamel.yaml
import os
def get_all_subdirectories():
    settings_data = helper.get_settings_data()
    directory_paths = settings_data["vault_path"]
    all_directories = []
    for start_path in directory_paths:  # Iterate through each path in the list
        for root, dirs, _ in os.walk(start_path):
            # Iterate through subdirectories and add them to the list
            for directory in dirs:
                full_path = os.path.join(root, directory)
                all_directories.append(full_path)
    return all_directories

def get_all_md_files():
    directories = get_all_subdirectories()

def parse_yaml():
    '''
    Does not take an argument, goes through the data.json list of file names and paths, and updates each object with any yaml that might exist
    '''
    start_delimiter, end_delimiter = "---\n", "---\n"
    data = []
    yaml = ruamel.yaml.YAML(typ='safe')
    files = helper.get_obsidian_data()
    for file in files: # attempt to parse out yaml properties
        file_path = file["file_path"]
        if file_path.endswith(".md"):
            # open file contents
            with open(file_path, "r") as f:
                content = f.read() #contents of file now stored in content variable
            start_index = content.find(start_delimiter) + len(start_delimiter)
            end_index = content.find(end_delimiter, start_index)
            if start_index > -1 and end_index > -1:
                #Is yaml, attempt to parse

                yaml_properties = content[start_index:end_index].strip() # Strip out yaml properties
                # print(yaml_properties)
                # print(type(file))
                # print(file)
                # print(f"THE YAML PROPERTIES ARE: \n{yaml_properties}\nITS TYPE IS {type(yaml_properties)}")
                if 'type: question' in yaml_properties:
                    note_dict = yaml.load(yaml_properties) # use yaml library to abstract the processing of properties
                    if type(file) == dict:
                        file.update(note_dict) # file should be a dictionary
                    data.append(file) #append our updated file object to our data list
                
                # We should now have our original file date name and path, plus whatever yaml exists in our file:
                else:
                    # Is not a question:
                    data.append(file) # append the file object to our data list
    print(len(data))
    helper.update_obsidian_data_json(data)

def scan_directory(vault_path): # Returns a list(s) of dictionaries
    '''
    takes a list of file_paths as an argument
    scans the vault_path directory and stores the results in two seperate .json
    data.json contains a raw_list of all .md files
    media_paths.json contains the filepaths for all media in the provided directories
    '''
    media_paths = {"file_paths": []}
    concepts = []
    for path in vault_path:
        total_checks = 0
        print(path)
        for root, dirs, files in os.walk(path):
            # print(f"Scanning root: {root}")
            # print(files)
            total_checks += 1
            for file in files:
                total_checks += 1
                # If a known text file, store in data.json (for now only .md)
                if helper.is_media(file):
                    media_paths["file_paths"].append(os.path.join(root,file))
                else:
                    # Is not media
                    data = {}
                    file_name, extension = os.path.split(os.path.basename(file))
                    data["file_name"] = f"{file_name}.{extension}"
                    data["file_path"] = os.path.join(root,file)
                    concepts.append(data)
                    # print(data)
                # If file is not a known document or script file type, it is treated as media, missed checks do not effect integrity of data. Only contribute to storage size bloat

    helper.update_obsidian_media_paths(media_paths)
    helper.update_obsidian_data_json(concepts)   
    parse_yaml()


def extract_questions_from_raw_data():
    '''
    returns questions_list based on any question objects found in data.json
    checks the questions_list and intializes metrics for question objects
    '''
    existing_database = helper.get_obsidian_data()
    questions_list = []
    for i in existing_database:
        # print(f"question object: {i}")
        if i.get("type") == "question":
            questions_list.append(i)
    
    for question in questions_list:
        del question["type"]
        question["object_type"] = "question"
    print(len(questions_list))
    return questions_list


def update_questions_json():
    '''
    checks new_questions against existing question objects in questions.json, then updates or adds the questions as necessary
    '''
    questions_list = extract_questions_from_raw_data() 
    questions_json = helper.get_question_data()   
    ##################################################
    # If questions.json has data we can initialize keys / scoring metric keys
    for new_question in questions_list:
        found = False
        for existing_question in questions_json:
            # If we find a match, update the existing entry with the new entry, but only certain keys, this retains the scores while keeping updates working
            if new_question["file_name"] == existing_question.get("file_name"):
                found = True
                existing_question.update(new_question)
                break
            # If there is no match, that means the question does not exist in our current questions.json
        if found == True:
            pass
        elif found == False:
            # For new entries, no scoring metrics will exist in that dictionary, we don't need to check if it's a question type since this function handles that already
            questions_json.append(new_question)
        else:
            print("oops something went wrong")
    # Now that we'd updated our questions.json we'll overwrite the old json file with the updated json file:
    
    total_questions_with_valid_keys = 0
    total_questions_with_invalid_keys = 0
    for i in questions_json:
        check = ""
        try:
            check = i["revision_streak"]
            total_questions_with_valid_keys += 1
        except:
            total_questions_with_invalid_keys
    print(f"There are {len(questions_json)} questions loaded into Quizzer.")
    print(f"There are {total_questions_with_valid_keys} questions with valid keys, and {total_questions_with_invalid_keys} with invalid keys.")
    helper.update_questions_json(questions_json) 