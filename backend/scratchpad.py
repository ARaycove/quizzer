import quiz_functions
import questions
import settings
import stats
import initialize
from lib import helper
import json
import re
import yaml
import requests
import os
from datetime import datetime, date
from datetime import timedelta
import math
import random
import stdio
import sys

    
initialize.initialize_quizzer()
question_list = quiz_functions.populate_question_list()



# Initialize function to set all non-initialized questions to a key: "value" of in_circulation: False,
## Added 2 lines of code to initialize function
# Utility function that returns a list of all questions with key: "value" of in_circulation: True
## Completed
# Set stat function to only include questions with a key: "value" of in_circulation: True,
## The above utility function made this very trivial
# Add in setting value desired_daily_questions
## Ran into an error because of == typo, fixed
# Add in function call to the populate quiz function that changes questions to in_circulation until we are greater than or equal to the desired_daily_questions stat
## This one was a bit more challenging, created an infinite loop because the file wasn't written to on each iteration of the loop
## This one takes a minute to boot up for the first time.
# Change question selection to filter out all questions with key: "value" of in_circulation: False,

# SQL Database
