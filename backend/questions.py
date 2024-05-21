from lib import helper
import stats
from datetime import datetime, date, timedelta
import json
import math
# This module holds any function that governs or alters a question object
#######################################################################
#######################################################################
#######################################################################
# Toggle whether the question is in circulation or not
def remove_question_from_circulation(question_object):
    question_object["in_circulation"] = False
    return question_object

def add_question_to_circulation(question_object):
    question_object["in_circulation"] = True
    return question_object

# calculate question stats
def calculate_question_id(questions):
    max_id = max(item.get("id", 0) for item in questions)
    new_id = max_id + 1
    print(f"max_id is: {max_id}, new_id is {new_id}")
    return new_id



def calculate_question_average_times_shown_per_day(question):
    '''
    calculates the how many times per day the individual question will be shown per day
    '''
    settings = helper.get_settings_data()
    increment = question["time_between_revisions"]
    revision_streak = question["revision_streak"]
    average = 1 / math.pow(increment, revision_streak)
    question["average_times_shown_per_day"]
    return question



def calculate_average_shown():
    questions = helper.get_question_data()
    for qa in questions:
        qa["average_times_shown_per_day"] = 1 / math.pow(qa["time_between_revisions"], qa["revision_streak"])
    helper.update_questions_json(questions)
    
    
    
def calculate_next_revision_date(status, dictionary):
    settings_data = helper.get_settings_data()
    if status == "correct":
        dictionary["next_revision_due"] = datetime.now() + timedelta(hours=(24 * math.pow(dictionary["time_between_revisions"],dictionary["revision_streak"]))) #principle * (1.nn)^x
    else: # if not correct then incorrect, function should error out if status is not fed into properly:
        # Intent is to make an incorrect question due immediately and of top priority
        dictionary["next_revision_due"] = datetime.now() - timedelta(hours=8760)


    
def create_questions_json_file():
    questions = []
    settings = helper.get_settings_data()
    question = {"time_between_revisions": settings["time_between_revisions"], "revision_streak": 1}
    dummy = {}
    # define initial question metadata
    dummy["id"] = 100
    dummy["file_path"] = "100"
    dummy["file_path"] = None
    dummy["object_type"] = "question"
    dummy["subject"] = ["miscellaneous"]
    dummy["related"] = ["tutorial"]
    # define main details of the question presented
    dummy["question_text"] = "Hello, welcome to quizzer, You can click show to see the answer, If you get the question correct press yes, otherwise press no"
    dummy["question_image"] = None
    dummy["question_audio"] = None
    dummy["question_video"] = None
    # define main details of the answer to the question
    dummy["answer_text"] = "Congratulations, thats it. press the menu and add your own questions"
    dummy["answer_image"] = None
    dummy["answer_audio"] = None
    dummy["answer_video"] = None
    # define question stats
    dummy["revision_streak"] = 100
    dummy["last_revised"] = helper.stringify_date(datetime.now())
    dummy["next_revision_due"] = helper.stringify_date(datetime.now())
    dummy["in_circulation"] = False
    dummy["is_eligible"] = True
    dummy["average_times_shown_per_day"] = calculate_question_average_times_shown_per_day(question)
    dummy["time_between_revisions"] = settings["time_between_revisions"]
    # add dummy question to initialize data structure
    questions.append(dummy)
    with open("json_data/questions.json", "w+") as f:
        json.dump(questions, f)
        
def initialize_questions_json():
    """Checks if question.json exists. If not, create it.
    """
    try:
        questions = helper.get_question_data()
        print("questions.json exists")
    except FileNotFoundError:
        print("questions.json not found")
        print("creating questions.json with default values")
        create_questions_json_file()

def evaluate_subject():
    '''
    Use AI to determine the subject(s) involved in the question object
    currently just a stub #FIXME
    '''
    subject = ["miscellaneous"]
    return subject
def evaluate_related_content():
    '''
    Use AI to determine what concepts/content is related to the question object
    currently just a stub #FIXME
    '''
    related = []
    return related


def initialize_question_metric_keys_if_they_dont_exist():
    '''
    takes a dictionary as an argument, then creates the key value pairs if they don't exist:
    "revision_streak" : 1
    "last_revised": datetime.now()
    "next_revision_due": datetime.now()
    returns a dictionary with the updated values, if they don't exist already
    '''
    settings_data = helper.get_settings_data()
    questions = helper.get_question_data()
    for dictionary in questions:
        # Initialize revision streak to 1
        if dictionary.get("revision_streak") == None:
            dictionary["revision_streak"] = 1
        
        # Initialize last revised date to now
        if dictionary.get("last_revised") == None:
            dictionary["last_revised"] = helper.stringify_date(datetime.now())

        # Initialize next_revision to be due immediately (last year)
        if dictionary.get("next_revision_due") == None:
            dictionary["next_revision_due"] = helper.stringify_date(datetime.now() - timedelta(hours=8760)) # This is due immediately and of the highest priority

        # Initialize question_data to None
        if dictionary.get("question_text") == None:
            dictionary["question_text"] = None
        if dictionary.get("question_image") == None:
            dictionary["question_image"] = None
        if dictionary.get("question_audio") == None:
            dictionary["question_audio"] = None
        if dictionary.get("question_video") == None:
            dictionary["question_video"] = None
            
        # Initialize answer_data to None
        if dictionary.get("answer_text") == None:
            dictionary["answer_text"] = None
        if dictionary.get("answer_image") == None:
            dictionary["answer_image"] = None
        if dictionary.get("answer_audio") == None:
            dictionary["answer_audio"] = None
        if dictionary.get("answer_video") == None:
            dictionary["answer_video"] = None
        
        # Initialize subjects
        if dictionary.get("subject") == None:
            dictionary["subject"] = evaluate_subject()
            
        # Initialize related concepts 
        if dictionary.get("related") == None:
            dictionary["related"] = evaluate_related_content()
            
        # Initialize in_circulation to False    
        if dictionary.get("in_circulation") == None:
            dictionary["in_circulation"] = False
        
        # Initialize time_between_revisions to default settings value
        if dictionary.get("time_between_revisions") == None:
            dictionary["time_between_revisions"] = settings_data["time_between_revisions"]
        # Initialize id
        if dictionary.get("id") == None:
            dictionary["id"] = calculate_question_id(questions)
        
    helper.update_questions_json(questions)
    
def return_in_circulation_questions():
    questions = helper.get_question_data()
    questions_in_circulation = []
    for question in questions:
        if question["in_circulation"] == True:
            questions_in_circulation.append(question)
    return questions_in_circulation

def update_score(status, file_name):
    settings_data = helper.get_settings_data()
    check_variable = ""
    bad_matches = 0
    # load config.json into memory, I get the feeling this is poor memory management, but it's only 1000 operations.
    existing_data = helper.get_question_data()
    for dictionary in existing_data:
        if dictionary["file_name"] == file_name:
            # Alternatively this could have been a seperate function for initializing, both work:
            ############# We Have Three Values to Update ########################################
            check_variable = dictionary["revision_streak"]
            print(f"Revision streak was {check_variable}, streak is now {check_variable + 1}")
            if status == "correct":
                dictionary["revision_streak"] = dictionary["revision_streak"] + 1
            elif status == "incorrect":
                dictionary["revision_streak"] = 1
            stats.increment_questions_answered()


            check_variable = dictionary["last_revised"]
            print(f"This question was last revised on {check_variable}")
            # Convert string json value back to a <class 'datetime.datetime'> type variable so it can be worked with:
            dictionary["last_revised"] = datetime.strptime(dictionary["last_revised"], "%Y-%m-%d %H:%M:%S")
            dictionary["last_revised"] = datetime.now()
            # Convert value back to a string so it can be written back to the json file
            dictionary["last_revised"] = dictionary["last_revised"].strftime("%Y-%m-%d %H:%M:%S")

            dictionary["next_revision_due"] = datetime.strptime(dictionary["next_revision_due"], "%Y-%m-%d %H:%M:%S")
            # Next revision due is based on the schedule that was outputted from the generate_revision_schedule() function:
            # If question was correct, update according to schedule, otherwise set next due date according to sensitivity settings so question is immediately available again for review regardless of what the user enters
            dictionary["next_revision_due"] = calculate_next_revision_date(status, dictionary)
            # Convert value back to a string so it can be written back to the json file
            dictionary["next_revision_due"] = dictionary["next_revision_due"].strftime("%Y-%m-%d %H:%M:%S")
            check_variable = dictionary["next_revision_due"]
            print(f"The next revision is due on {check_variable}")
        else:
            bad_matches += 1
    helper.update_questions_json(existing_data)