import json
import random
from lib import helper
import settings
import stats
import questions
from datetime import datetime, timedelta
##################################################################
# This file will determine how the quiz object is populated,
# The quiz object consists of question objects
##################################################################


def get_value_of_subject_priority(subject):
    settings_data = helper.get_settings_data()
    # print(subject)
    priority_value_list = []
    for key, value in settings_data.items():
        for item in subject:
            if item in key and "priority" in key:
                priority_value_list.append(value)
    if all(priority_value_list) and len(priority_value_list) > 0:
        priority_value = min(priority_value_list)
        return priority_value
    elif all(priority_value_list) == False:
        priority_value = 0
        return priority_value
    elif any(priority_value_list):
        for i in range(priority_value_list.count(0)):
            priority_value_list.remove(0)
        priority_value = min(priority_value_list)
        return priority_value
    else:
        # If we don't find a matching subject, return 0 so the question is filtered out
        print("something went wrong")
        priority_value = 0
        return priority_value
    
    
    
##################################################################    
def get_value_of_subject_weight(subject):
    settings_data = helper.get_settings_data()
    weight_value_list = []
    for key, value in settings_data.items():
        if subject in key and "weight" in key:
            weight_value = value
    return weight_value



##################################################################    
def get_subject_settings():
    settings_data = helper.get_settings_data()
    priority_settings = {}
    for key, value in settings_data.items():
        if "subject" in key:
            priority_settings.update({key: value})
    return priority_settings
## if question has priority with a setting of 0



##################################################################
def filter_question_list(questions):
    '''filter out ineligble questions from our master list of questions'''
    settings_data = helper.get_settings_data()
    due_date_sensitivity = settings_data["due_date_sensitivity"]
    sorted_questions = []
    for question in questions:
        ## if question is not due within x hours
        # convert to datetime object for comparison
        question["next_revision_due"] = datetime.strptime(question["next_revision_due"], "%Y-%m-%d %H:%M:%S")
        if question["next_revision_due"] < (datetime.now() + timedelta(hours=due_date_sensitivity)):
            sorted_questions.append(question)
            continue
        if get_value_of_subject_priority(question["subject"]) == 0:
            sorted_questions.append(question)
    return sorted_questions

# Check quiz_length setting  against available questions



##################################################################
def ensure_quiz_length(sorted_questions, quiz_length):
    '''
    function provides that the attempted number of questions to be populated into the quiz is <= the number of questions available for selection:
    '''
    if len(sorted_questions) < quiz_length:
        quiz_length = len(sorted_questions)
    if quiz_length <= 0: # If there are no questions up for review, then we need to exit the function:
        print("There are no questions up for review, Good Job!")
        return None
    return quiz_length



##################################################################
def get_number_of_revision_streak_one_questions(sorted_questions):
    num_questions = 0
    for question in sorted_questions:
        if question["revision_streak"] == 1:
            num_questions += 1
    return num_questions
# selection algorithm


##################################################################
def get_number_of_questions_in_subject(subject, sorted_questions):
    available_questions = 0
    for question in sorted_questions:
        if subject in question["subject"]: #subject should be a string, question["subject"] is a list value, so we use subject in list method:
            available_questions += 1
            
    print(f"Number of questions available in the {subject} subject is: {available_questions}")
    return available_questions


##################################################################
def select_questions_to_be_returned(sorted_questions, quiz_length):
## questions filled first, if revision streak is 1, always fill these
    question_list = []
    sorted_questions = sorted(sorted_questions, key=lambda x: x['next_revision_due'])
    if len(sorted_questions) == 0:
        return None
    print(f"Revision Streak One (Unanswered) questions have priority, there are {get_number_of_revision_streak_one_questions(sorted_questions)} unanswered questions.")
## questions by priority
## Stop selecting when quiz length = 0
    jump = True
    revision_one_questions = 0
    while True: #Just making a master loop, the return keyword is what will break us out of the loop (and the function)
    ##################
    # first for loop will fill the question list with streak 1 questions until there are no streak 1 questions left:
        if get_number_of_revision_streak_one_questions(sorted_questions) > 0:
            for question in sorted_questions:
                if question["revision_streak"] == 1:
                    question_list.append(question) # removes the question from our sorted list and adds it to our question list
                    sorted_questions.remove(question)
                    revision_one_questions += 1
                if len(question_list) >= quiz_length:
                    print(f"{revision_one_questions} Streak one questions were selected")
                    return question_list
        else:
            print(f"{revision_one_questions} Streak one questions were selected")
            subject_settings = get_subject_settings()
            priority_settings = []
            for key, value in subject_settings.items():
                if "priority" in key:
                    priority_settings.append((key, value))
                else:
                    continue
            priority_settings = sorted(priority_settings, key=lambda x: x[1])
            for tuple in priority_settings:
                subject = tuple[0]
                subject = subject[len("subject_"):]
                subject = subject[:-len("_priority")]
                print()
                print(f"{'#' * 25}")
                print(f"Now selecting questions from {subject}")
                print(f"{'#' * 25}")
                #Phew, now have a list of sorted subjects:
                # After we select the subject to fill, we need to set the number of questions to choose based on:
                # The weight settings
                # Then check how many questions in the list are available in that subject
                # If the number of questions available to choose is less than the weight settings, set the num_questions to choose to the number available
                num_questions_to_choose = get_value_of_subject_weight(subject)
                available_questions = get_number_of_questions_in_subject(subject, sorted_questions)
                print(f"verifying if enough questions are available in subject: {subject}")
                print(f"There are {available_questions} in subject: {subject}, with {num_questions_to_choose} to be selected")
                if available_questions < num_questions_to_choose:
                    num_questions_to_choose = available_questions
                    print(f"Not enough available questions, now choosing {num_questions_to_choose} out of {available_questions} instead.")
                elif available_questions >= num_questions_to_choose:
                    print(f"There are enough questions available, selecting {num_questions_to_choose} out of {available_questions} available questions.")
                else:
                    print("Something went wrong.")
                print(f"Choosing {num_questions_to_choose} from the subject: {subject}")
                # Select questions based on criteria
                for question in sorted_questions:
                    if subject in question["subject"]:
                        # This line throws an error if no question_text is present
                        print(f"found a match, question-id:{question['id']}")
                        # print(f"found a match: {question['question_text'][:25]}. . .", end="")
                        question_list.append(question)
                        sorted_questions.remove(question)
                        num_questions_to_choose -= 1
                        print(f"current length of question_list is now: {len(question_list)}")
                        print(f"remaining questions to choose from {subject} is now {num_questions_to_choose}")
                    if len(question_list) >= quiz_length:
                        print(f"question list is full, returning now")
                        print(f"verifying. . .:list has {len(question_list)} questions out of {quiz_length} to be selected")
                        return question_list
                    if num_questions_to_choose <= 0:
                        break

def put_questions_in_circulation():
    settings_data = helper.get_settings_data()
    questions_data = helper.get_question_data()
    stats_data = helper.get_stats_data()
    
    average_daily_questions = stats_data["average_questions_per_day"]
    desired_daily_questions = settings_data["desired_daily_questions"]
    
    if average_daily_questions >= desired_daily_questions * 1.10: # 10% threshold, so if desired is 100, if we exceed 110 the script will reduce the amount of questions in circulation
        target = average_daily_questions - (desired_daily_questions * 1.05) # if 100 is desired and 111 exist then 5% above threshold is the target, the count variable would then be 111-105 = 6.
                                                                            # We would then subtract from 6 until target <= 0
        for qa in questions_data:
            if qa["in_circulation"] == True:
                qa["in_circulation"] = False
                target -= qa["average_times_shown_per_day"]
            if target <= 0:
                stats.update_stats()
                helper.update_questions_json(questions_data)
                return None
    elif average_daily_questions < desired_daily_questions: # Indicating we need to add questions
        target = desired_daily_questions - average_daily_questions # so if desired is 100, and average is 90, target is 10. We subtract from the target until we reach 0
        for qa in questions_data:
            if qa["in_circulation"] == False:
                qa["in_circulation"] = True
                target -= qa["average_times_shown_per_day"]
            if target <= 0:
                stats.update_stats()
                helper.update_questions_json(questions_data)
                return None
    else:
        return None
    print("Finished updating list of circulating questions")
    count = 0
    for question in questions_data:
        if question["in_circulation"] == True:
            count += 1
    print(f"Total questions in circulation is: {count}")
    print(f"Total questions in database: {len(questions_data)}")
    stats_data = helper.get_stats_data()
    stats_data["current_questions_in_circulation"] = count
    helper.update_stats_json(stats_data)
    
def update_in_circulation_stat():
    # Update the value
    stats.update_stats()
    #Check settings file and get value
    stats_data = helper.get_stats_data()

    average_daily_questions = stats_data["average_questions_per_day"]
    # return the value to the user
    return average_daily_questions

##################################################################
def populate_question_list():
    put_questions_in_circulation() # Start by ensuring questions are put into circulation if we can fit them in the average
    stats.update_stats() # update stats every time we go to get a new list of questions
    
    stats_data = helper.get_stats_data()
    settings_data = helper.get_settings_data()
    questions_data = helper.get_question_data()
    quiz_length = settings_data["quiz_length"]
    
    ##################################################
    # filter out questions based on criteria
    in_circulation_questions = questions.return_in_circulation_questions()
    sorted_questions = filter_question_list(in_circulation_questions)
    
    #############################################
    # Sort question objects by next_revision_due key value
    quiz_length = ensure_quiz_length(sorted_questions, quiz_length)
    
    question_list = select_questions_to_be_returned(sorted_questions, quiz_length)
    # print(f"number of questions chosen: {len(question_list)}")
    if question_list == None:
        sorted_questions = None
    else:
        print(f"Total questions in database : {len(questions_data)}")
        print(f"Number of eligible questions: {len(sorted_questions)}")
        print(f"Number of questions in this round: {quiz_length}")
        random.shuffle(question_list) # ensures there is some level of randomization, so users don't notice this is just a cycling list
        question_list = question_list[::-1] # Reverse the list
        random.shuffle(question_list) # Shuffle it again
        print(f"List of {len(question_list)} questions has been shuffled for pseudorandomness.")
    print(stats_data)
    return question_list, sorted_questions

