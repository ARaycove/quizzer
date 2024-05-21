# This file is just here to contain old code for reference later
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty

class MainInterface(GridLayout):
    def __init__(self, **kwargs):
        super(MainInterface, self).__init__(**kwargs)
        ############################################
        # Set number of columns
        # self.cols = 1    
        ############################################
        # Add Widgets
        ############################################
        # Contains the Ham_menu, and question metadata and any prominent stats
        # self.top_grid = GridLayout()
        # self.top_grid.cols = 3
        # self.add_widget(self.top_grid)
        # # Top Row
        # self.ham_menu = Button(
        #     text="Menu",
        #     size_hint_x = None)
        # self.top_grid.add_widget(self.ham_menu)
        
        # self.question_data = Label(text="This is some metadata about the question")
        # self.top_grid.add_widget(self.question_data)
        
        # self.question_stats = Label(text="This is more metadata about the question")
        # self.top_grid.add_widget(self.question_stats)
        
        ############################################
        # # Main Body
        # self.question_text = Label(text="This is a question?")
        # self.add_widget(self.question_text)
        
        # self.question_media = Label(text="This is the question's media?")
        # self.add_widget(self.question_media)
        # # self.add_widget(Label(text=""))
        
        # self.answer_text = Label(text="This is the answer to the question")
        # self.add_widget(self.answer_text)
        
        # self.answer_media = Label(text="This is the media that belongs to the answer")
        # self.add_widget(self.answer_media)
        # # self.add_widget(Label(text=""))
        ############################################
        # # User Inputs
        # self.user_input = GridLayout(size_hint_y = None, height="50dp")
        # self.user_input.cols = 2
        # self.add_widget(self.user_input)
        # self.input_field = TextInput(multiline=True)
        # self.user_input.add_widget(self.input_field)
        
        # self.show_answer = Button(text="Next", size_hint_x = None, width="40dp")
        # self.user_input.add_widget(self.show_answer)
        
        # # self.add_widget(Label(text=""))
        # ############################################
        # # Score Buttons
        # # add score buttons row
        # self.score_buttons = GridLayout(size_hint_y = None, height="50dp")
        # self.score_buttons.cols=2
        # self.add_widget(self.score_buttons)
        
        # self.answer_yes = Button(text="YES", width="40dp")
        # self.score_buttons.add_widget(self.answer_yes)
        
        # self.answer_no = Button(text="NO")
        # self.score_buttons.add_widget(self.answer_no)
        # # self.add_widget(Label(text=""))
        ############################################   