# Quizzer
Student Question and Answer program that tests students on a variety of questions in a randomized fashion

This is the inspiration for the entire project. Its components serve as the the base for a portion of the backend and all of the frontend-cli.

## Scientific Basis
Quizzer is not just an application that feeds questions, the premise behind conclusion is that by using established memory science, an algorithm can be built that maximizes the learning process

The selection algorithm for Quizzer is based on Hermann Ebbignhaus's study from 1880 to 1885, this study was repeated in 2015 with similar results. (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4492928/). The order of which questions are presented is also designed to take advantage of our current understanding of the human mind, the engram, the encoding process, and the retrieval process, with added caution involved to prevent the misinformation effect from setting the user back in their studies.

# General Notes
This document contains the structure and descriptions of what's in each json file.
The json data on the backend is organized in these files
- questions.json
- stats.json
- settings.json
# File Structure
- dependencies.txt
    a (not so updated) list of all dependencies required to run quizzer. this is determined by manually going through the imports of each module and compiling the list together. Hoping to deploy this via docker and packaging it that way
- main.py
    - main entry point for the program, all logic to launch both the back and front ends are contained here. Notice the api is a launched in one thread and the front-end launched in a second thread.
    - quizzer/ 
        - contains the backend logic that drives quizzer
        json_data/
            - contains all json files
        backups/
            - contains all backup json files, currently a manual process
        integrations/
            - contains the obsidian module used to integrate quizzer with the users obsidian vault
        lib/
            helper.py
                helper.py contains general library functions used across the program
        media_files/
            contains the actual media files used by the questions
        old_program/
            a relic of the past, just there to glean some old ideas and a momento the very first iteration of quizzer
        api.py
            contains the logic to launch the api server, which effectively is an active backend server
        initialize.py
            compilation of functions written in order, launches the program and performs health check functions.
        questions.py
            contains all logic relating to question objects, if a function alters a question object the function will be located here
        quiz_functions.py
            contains all logic relating to which questions should be presented to the user at any given time
        settings.py
            contains all logic relating to user settings and preferences
        stats.py
            contains all functions and logic relating to statistics

    

# database structure    
## questions.json
the questions.json file contains question objects each with a set of the following properties and descriptions:
- id: the unique reference number to look up the question in the database
- file_name: used in Obsidian integration, refers to the filename that the question object is represented in:
- file_path: used in Obsidian integration, refers to the filepath where the .md document for the question is located.
- object_type: used in Obsidian integration,
- subject: is a list containing every subject the question relates to
- related: is a list containing every concept/idea the question relates to (will be used lated in AI or NLP implementation when graphing a map of concepts)
### question objects must have at least one of the following question fields:
- question_text: optional, contains the text to be displayed when presenting the question to the user
- question_image: optional, contains the image file name to be displayed when presenting the question to the user
- question_audio: optional, contains the audio file name to be played when presenting the question to the user
- question_video: optional, contains the video file name to be played when presenting the question to the user
### question objects must also have at least one of the following answer fields:
- answer_text: optional, contains the text to be displayed when the user answers the question
- answer_image: optional, contains the image file name to be displayed whne the user answers the question
- answer_audio: optional, contains the audio file name to be played when the user answers the question
- answer_video: optional, contains the video file name to be played when the user answers the question
### The next set of variables is used in determining when a question should be shown or some other stat unique to the question_object
- revision_streak: represents the total correct attempts in a row, if a user answered a question x amount of times in a row correctly the streak will be x+1, each streak starts at one.
- last_revised: represents the date and time the user last answered the question
- next_revision_due: represents the date and time the user should answer the question next for optimal retention
- in_circulation: boolean value that determines whether a question is to be shown or kept in "reserve" essential for ensuring the user does not inadvertantly enter so many questions that they can't keep up with the required pace to retain everything entered. Therefore questions are entered into circulation gradually according to the users individual learning pace
- is_eligible: boolean value not in use, will later be used to assess if a question is eligible to be presented to the user when the populate_question_list function is called.
- average_times_shown_per_day: represents the average number of times a question will be shown per day, so a value of 0.1 would mean the question will be shown every 10 days. Used to determine how many questions go into circulation
- time_between_revisions: defaults to the setting value, number represents the "interest rate" of the formula. see the calculate_next_revision_date function for the formula which is called when update_score is called. individual value now adapted to each question, since each question is retained at different rates. So that some things are learned extremely quickly and need less revision to retain while other things are learned slower and need more revision. However the logic is implemented yet to actively adapt this value to the user. So this will be updated with more research later.

## settings.json
- quiz_length: represents the total number of questions that is returned by populate_question_list function. A full list is returned so that we can have a priority and weight system for presentation
- time_between_revisions: see above explanation, determines the default value that each question_object gets
- vault_path: OPTIONAL used to point to the directory of the obsidian vault that the user may or may not have.
- desired_daily_questions: Set by the user currently, set this value to the number of questions the user can reasonably answer on a day to day basis. If you think you can only answer 10 questions a day consistently set this value to 10. If seeking to aggressively learn a large volume of knowledge, set this value to over 200.
- subject_SUBJECT-HERE_priority: determines which questions get priority when the question_list is filled. higher priority number means questions with that subject get filled first.
- subject_SUJBECT-HERE_weight: determines how many questions of said subject get filled on any given iteration of the loop. So a priority of 1 and a weight of 5 would mean that when filling the list that 5 questions of that subject get entered first. when the question list reaches the quiz_length value the question_list is returned. Additionally if the priority is 1 and the weight is 1000, the entire question_list will consist of just that one subject while eligible questions remain.
    this allows the user to set subjects that they are currently studying for class to always come first before showing other miscellaneous knowledge

## stats.json
- questions_answered_by_date: Is a dictionary, each key represents a date, the value represents the number of questions answered on that given day.
- total_questions_answered: is an integer, represents the total amount of questions the user has answered over the entire lifespan
- average_questions_per_day: is a float, represents the current amount of questions that will be shown to the user every day. A function exists that relies on this value to determine when the program should add or remove questions from circulation
- revision_streak_stats: Is a dictionary, each key represents the revision_streak value, each value represents the total amount of questions at that revision_streak. so a key: "value" of "12": 120 means 120 questions have a revision streak of 12
- current_questions_in_circulation: represents the total amount of questions that are actively in rotation. A fun value to show progress to the user, the higher the value gets the more you know. GAMIFICATION!
- total_questions_in_database: is a dictionary, each key represents a given date, each value represents the total number of question objects in questions.json on that given date. This can be used to show progress over time to the user.