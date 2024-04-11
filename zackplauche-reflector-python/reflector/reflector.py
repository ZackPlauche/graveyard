import time

from reflector.activities import Activity
from reflector.questions import InlineQuestion, YesNoQuestion, YES_ANSWERS
from reflector.utils import create_total_time_string


class Reflector:

    def __init__(self, activities: list):
        if not all(isinstance(activity, Activity) for activity in activities):
            raise TypeError('All objects in "activities" list must be a type of Activity.')
        self.activities = activities

    def run(self):
        print('\nWelcome to Reflector!')
        while True:
            activity = self.select_activity()
            start_time = time.time()
            activity.run()
            end_time = time.time()
            total_time = create_total_time_string(end_time - start_time)
            print('\n', f'Total reflection time: {total_time}', sep='', end="\n\n")
            play_again = YesNoQuestion('Would you like to play again?').endwith('\n').ask()
            if play_again.casefold() not in {*YES_ANSWERS, ''}:
                break
        
    def select_activity(self):
        print('Please select an activity.', end='\n\n')
        print(*(f'{num}) {activity.name}' for num, activity in enumerate(self.activities, 1)), 
              sep='\n', end='\n\n')
        choice_length = len(self.activities)
        activity_number = InlineQuestion(f'Activity number (from 1 to {choice_length})',
                                         valid_answers=range(1, choice_length + 1),
                                         display_answers='',
                                         ).endwith('\n\n').ask()
        activity_number = int(activity_number) - 1
        activity = self.activities[activity_number]
        return activity
        