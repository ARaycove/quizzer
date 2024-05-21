import os
import subprocess
import requests
import time
from urllib.parse import quote
import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from api_calls import (
    populate_quiz, 
    update_score,
    initialize_quizzer, 
    get_absolute_media_path, 
    get_subject_settings,
    get_average_questions_per_day)
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.metrics import dp




class HamMenu(Popup):
    '''
    This class exists to dynamically generate our settings page, since subjects are dynamic.
    '''
    subject_settings = ObjectProperty(None)
    settings_section = ObjectProperty(None)
    def generate_subject_settings(self):
        settings_data = get_subject_settings()
        self.subject_settings.clear_widgets()
        
        for setting, value in settings_data.items():
            label = Label(text=f"{setting}", size_hint_y=None,font_size =16, height=dp(24))
            text_input = TextInput(text=f"{value}", size_hint_y=None, multiline=False, height=dp(24))
            self.subject_settings.add_widget(label)
            self.subject_settings.add_widget(text_input)
    def update_subject_settings(self):
        # for TextInput in subject_settings:
        print("This does nothing yet") #FIXME # Plug in update_setting api call here

class QuestionInterface(Widget):
    #############################
    # Variable Defines
    # ham_menu = ObjectProperty(None)
    # ####################################
    # question_data = ObjectProperty(None)
    # stats_feed = ObjectProperty(None)
    # question_text = ObjectProperty(None)
    # question_media = ObjectProperty(None)
    # answer_text = ObjectProperty(None)
    # answer_media = ObjectProperty(None)
    # user_input = ObjectProperty(None)
    #################################### 
       
            
    def __init__(self, **kwargs):
        super(QuestionInterface, self).__init__(**kwargs)
        # Main Script
        # Populate a quiz upon launch
        self.question_list, self.returned_sorted_questions = populate_quiz()
        # Display the first question
        self.display_question()
        self.has_seen_answer = False
        # Startup complete

    def make_quiz_if_empty(self):
        if self.question_list == None:
            time.sleep(5)
        elif len(self.question_list) <= 0:
            self.question_list, self.returned_sorted_questions = populate_quiz() 

    def display_question(self):
        '''
        Displays a question and returns data about that question
        First Phase of the Loop
        '''
        self.has_seen_answer = False
        self.make_quiz_if_empty()
        try:
            self.current_question = self.question_list[0]
        except:
            self.current_question = {}
        if self.current_question.get("file_name") != None:
            self.file_name = self.current_question.get("file_name")
            
        if self.current_question.get("file_path") != None:
            self.file_path = self.current_question.get("file_path")
            
        if self.current_question.get("type") != None:
            self.type = self.current_question.get("type")
            
        if self.current_question.get("subject") != None:
            self.subject = self.current_question.get("subject")
            data_label_string = f"{'Subject(s)'}: {';'.join(self.subject)}\n"
            
            
        if self.current_question.get("related") != None:
            self.related = self.current_question.get("related")
        
        
        if self.current_question.get("question_text") != None:
            self.question_text = self.current_question.get("question_text")
            self.ids.question_text.text = self.question_text
            
        if self.current_question.get("question_media") != None and self.current_question.get("question_media") != "Error":
            self.question_media = str(self.current_question.get("question_media"))
            print(f"search for me: {self.question_media}")
            self.ids.question_media.source = get_absolute_media_path(self.question_media)
        else:
            self.question_media = ""
            # Load media
        # else:
        #     self.question_media = ""
            
        if self.current_question.get("answer_media") != None and self.current_question.get("answer_media") != "Error":
            self.answer_media = self.current_question.get("answer_media")
            print(self.answer_media)
        if self.current_question.get("answer_text") != None:
            self.answer_text = self.current_question.get("answer_text")
        else:
            self.answer_text = ""
            
        if self.current_question.get("next_revision_due") != None:
            self.next_revision_due = self.current_question.get("next_revision_due")
            
        if self.current_question.get("revision_streak") != None:    
            self.revision_streak = self.current_question.get("revision_streak")
            data_label_string += f"{'Streak'}: {str(self.revision_streak)}\n"
        if self.current_question.get("last_revised") != None:
            self.last_revised = self.current_question.get("last_revised")
            data_label_string += f"{'Last Reviewed'}: {str(self.last_revised)}\n"
            data_label_string += f"{'Due Date'}: {str(self.next_revision_due)}\n"
        
        # Fill in stats_feed section
        try:
            label_string = f"{'For Review'}: {str(len(self.returned_sorted_questions)-(25-len(self.question_list)))}\n"
            label_string += f"{'Avg Q:'}: {get_average_questions_per_day():.2f}"
            self.ids.stats_feed.text = label_string
            self.ids.question_data.text = data_label_string
        except TypeError:
            print("No questions returned")
        return None
    
    def show_answer(self):
        '''
        When button pressed, function shows the answer and enables the use of the scoring buttons
        Second Phase of the Loop
        '''
        if self.answer_text == list:
            self.answer_text = "\n".join(self.answer_text)
        self.has_seen_answer = True
        self.ids.answer_text.text = str(self.answer_text)
        if self.answer_media != None: #meaning we have media for this answer
            self.ids.answer_media.source = str(get_absolute_media_path(str(self.answer_media)))
    def question_correct(self):
        if self.has_seen_answer == True:
            # Update Score, then display the next question
            answer = "correct"
            file_name = self.file_name
            update_score(answer, file_name)
            self.question_list.pop(0)
            self.clear_fields()
            

            
        else:
            print("Button Disabled")
        
    def question_incorrect(self):
        if self.has_seen_answer == True:
            answer = "incorrect"
            file_name = self.file_name
            update_score(answer, file_name)
            self.question_list.pop(0)
            self.clear_fields()

        else:
            print("Button Disabled")
    def question_skip(self):
        '''Skips the question, removing it from the list with no score update'''
        if self.question_list == None:
            self.make_quiz_if_empty()
        else:
            self.question_list.pop(0)
        self.clear_fields()
        
    def clear_fields(self):
        self.ids.answer_text.text = ""
        self.ids.answer_media.source = ""
        self.ids.question_text.text = ""
        self.ids.question_media.source = ""
        self.ids.question_data.text = ""
        self.ids.stats_feed.text = ""
        self.ids.user_input.text = ""
        self.display_question()
    
    
    
class Quizzer(App):
    def build(self):
        return QuestionInterface()

if __name__ == '__main__':
    initialize_quizzer()
    Quizzer().run()


