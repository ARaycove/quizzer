import json
import math
from lib import helper
import questions
from datetime import date, datetime
#FIXME
# One function per stat should exist
# each function should print the value of that stat to stats.jon
# API Calls should then only need to reference stats.json for statistics information.
#FIXME
def calculate_revision_streak_stats():
    pass

def calculate_average_questions_per_day():
    questions = helper.get_question_data()
    average_questions_per_day = 0
    for question in questions:
        if question["in_circulation"] == True:
            average_questions_per_day += question["average_times_per_day"]
    return average_questions_per_day

def calculate_num_questions_in_circulation():
    length = len(questions.return_in_circulation_questions())
    return length

def initialize_first_time_stats():
    stats = {}
    stats["questions_answered_by_date"] = {f"{datetime.now()}": 0}
    stats["total_questions_answered"] = 0
    stats["average_questions_per_day"] = calculate_average_questions_per_day()
    stats["revision_streak_stats"] = calculate_revision_streak_stats()
    stats["current_questions_in_circulation"] = calculate_num_questions_in_circulation()
    with open("json_data/stats.json", "w+") as f:
        json.dump(stats, f)

def initialize_stats_json():
    '''
    Health check function, if the stats.json file is missing then function will create and initialize stats.json with default data
    '''
    try:
        helper.get_stats_data()
        print("stats.json already exists")
    except FileNotFoundError:
        print("stats.json not found")
        print("creating stats.json with default values")
        initialize_first_time_stats()

def print_and_update_revision_streak_stats():
    # Load in data from json
    questions_data = questions.return_in_circulation_questions()
    stats = helper.get_stats_data()
    
    # Get each level of revision that exists:
    revision_stat_list = []
    revision_stat_set = set(revision_stat_list)
    for i in questions_data:
        revision_stat_list.append(i["revision_streak"])
        revision_stat_set.add(i["revision_streak"])
    # Initialize variables
    average_questions_per_day = 0
    stats["revision_streak_stats"] = {}
    # loop through each unique level of revision and get the total questions with that level of revision
    for i in revision_stat_set:
        count = revision_stat_list.count(i)
        stats["revision_streak_stats"][i] = count
    # Update stats.json with new information
    helper.update_stats_json(stats)
    
def update_stat_total_questions_in_database():
    questions = helper.get_question_data()
    stats = helper.get_stats_data()
    todays_date = helper.stringify_date(date.today())
    total_questions_in_database = len(questions)
    metric = {todays_date: total_questions_in_database}
    if stats.get("total_questions_in_database") == None:
        print("initializing first intance of stat 'total_questions_in_database'")
        stats["total_questions_in_database"] = metric
    else:
        print("updating total_questions_in_database stat")
        stats["total_questions_in_database"][todays_date] = total_questions_in_database
    helper.update_stats_json(stats)

def update_average_questions_per_day():
    questions_data = helper.get_question_data()
    stats = helper.get_stats_data()
    average = 0
    for qa in questions_data:
        if qa["in_circulation"] == True:
            average += qa["average_times_shown_per_day"]
    stats["average_questions_per_day"] = average
    helper.update_stats_json(stats)
    
def update_stat_current_questions_in_circulation():
    stats = helper.get_stats_data()
    questions_data = questions.return_in_circulation_questions()
    length = len(questions_data)
    stats["current_questions_in_circulation"] = length
    helper.update_stats_json(stats)
    
    
def increment_questions_answered():
    '''
    Embeds inside the update score function, increments the questions answered stat. Questions answered is stored by date, so the user can see a record of usage over time.
    '''
    todays_date = helper.stringify_date(date.today())
    stats_data = helper.get_stats_data()
    if stats_data.get("questions_answered_by_date") == None: # First check, if the variable isn't there at all create the questioned answer dict stat
        print("questions_answered object does not exist, creating entry")
        stats_data["questions_answered_by_date"] = {todays_date: 1}
    elif todays_date not in stats_data["questions_answered_by_date"]: # Second check, if the user hasn't answered a questioned today then todays date will not be in the dictionary
        print("first question of the day, initializing new key: value for today's date")
        stats_data["questions_answered_by_date"][todays_date] = 1
    else: # No check needed here, if the variable exists and the todays date exists as key we can safely access the key
        print("incrementing score for today")
        stats_data["questions_answered_by_date"][todays_date] += 1
    stats_data["total_questions_answered"] = sum(stats_data["questions_answered_by_date"].values())
    helper.update_stats_json(stats_data)

def update_stats():
    update_stat_total_questions_in_database()
    print_and_update_revision_streak_stats()
    update_average_questions_per_day()
    update_stat_current_questions_in_circulation()

