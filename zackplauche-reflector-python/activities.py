from reflector.activities import Activity, IntegrityActivity
from reflector.questions import ListQuestion, InlineQuestion, TextQuestion, YesNoQuestion, OrderedListQuestion, Question

# Questions

daily_intentions = OrderedListQuestion('What are your intentions for the day?', name='Daily Intentions')
daily_lessons = ListQuestion('What lessons did you learn or relearn today?', name='Daily Lessons')
daily_wins = OrderedListQuestion('What are your wins for the day?', name='Daily Wins')
easier_life = OrderedListQuestion('Name an idea to make your life easier', limit=5, loop=True, name='Easy Life')
goals = OrderedListQuestion('What are your goals?', name='Goals')
gratitude = OrderedListQuestion('What are you grateful for?', list_style='. I\'m grateful for ', name='Gratitude List')
improvements = ListQuestion('What can you do to improve?', name='Improvements')
meaningful_experience = TextQuestion('What was one meaningful experience you had today?', name='Meaningful Experience')
perfect_day = OrderedListQuestion('Forget everything you just typed. Now,...\n\n' 'What does your perfect day look like?', name='Perfect Day')
personal_priorities = OrderedListQuestion('What are your top 3 personal priorities (starting with The ONE Thing)?', limit=3, name='Personal Priorities'),
reflect = TextQuestion('Take some time to reflect on your life.', name='Reflection')
self_love = OrderedListQuestion('What are 10 reasons you love yourself?', limit=10, list_style='. I love myself because ', name='10 Reasons I Love Myself')
type_of_person = ListQuestion('What type of person do you choose to be today?', list_style='• I choose to be ', name='Type of Person')
weekly_wins = ListQuestion('What are your wins for the week?', name='Weekly Wins')
wins = ListQuestion('What are your wins?', name='Wins')
work_priorities = OrderedListQuestion('What are your top 3 professional priorities (starting with The ONE Thing)?', limit=3, name='Work Priorities'),
ten_ideas_to_improve_your_life = OrderedListQuestion('What are 10 ideas to improve your life?', limit=10, loop=True, name='10 Ideas to Improve Your Life')


# Activities

physiology = IntegrityActivity('Physiology', [
    YesNoQuestion('Do you feel well rested?', name='Well Rested'),
    YesNoQuestion('Are you hydrated?', name='Hydrated'),
    YesNoQuestion('Are you well fed?', name='Well Fed'),
    YesNoQuestion('Did you (or are you going to) exercise today?', name='Movement'),
    YesNoQuestion('Is the temperature fine for you?', name='Good Temperature'),
    YesNoQuestion('Is your environment clean and organized?', name='Clean Environment'),
    YesNoQuestion('Do you feel complete wellness?', name='Feeling of Wellness'),
], solutions=[
        'Taking a nap up to 30 minutes',
        'Drinking some water',
        'Eating something healthy',
        'Going for a 30 minute walk',
        'Putting on more clothes, taking off some clothes, turning on a fan, Air Conditioner, heater, or drinking something warm, like tea :)',
        'Cleaning  and/or organizing your environment',
        'Drinking an herbal remedy, like ginger, lemon, and honey tea'
])

security = IntegrityActivity('Security', [
    YesNoQuestion('Are you financially well off or have a financial plan?', name='Financially Safe'),
    YesNoQuestion('Are you physically safe?', name='Physically Safe'),
])


love_and_belonging = IntegrityActivity('Love & Belonging', [
    YesNoQuestion('Have you messaged 5 of your friends saying "I appreciate you & you matter to me"?', name='5 Friends Appreciated'),
    YesNoQuestion('Have you talked to your favorite person or Significant Other?', name='SO / Favorite Person Talked To')
])

self_esteem = Activity('Self Esteem', [
    self_love,
    OrderedListQuestion('What 5 things do you feel most competent at today?', limit=10, name='5 Daily Competencies')
])

self_actualization = Activity('Self Actualization', [
    InlineQuestion('What 1 project are you most excited to work on?').endwith('\n'),
    OrderedListQuestion('What skills are you going to use from the self esteem list?', limit=5, name='Project You\'re Most Excited For'),
    OrderedListQuestion('What actions (in order) can be done to secure the success of that project?', name='Actions for Project Success'),
    ListQuestion('What criteria will gauge the success of that project?', name='Criteria for Project Success'),
    YesNoQuestion('Did you express completion of this board to your accountability partners?', name='Shared With Accountability Partners'),
])

acclaim_system = Activity('Acclaim System', [
    physiology.add_intro('PHYSIOLOGY').without_solutions(),
    security.add_intro('SECURITY'),
    love_and_belonging.add_intro('LOVE AND BELONGING'),
    self_esteem.add_intro('SELF ESTEEM'),
    self_actualization.add_intro('SELF ACTUALIZATION'),
])

prismatic_system = Activity('Prismatic System', [
    InlineQuestion('What is your goal?', name='Goal'),
    ListQuestion('P: What People will you utilize to achieve your goal?', name='People'),
    ListQuestion('R: What Resources will you utilzie to achieve your goal?', name='Resources'),
    ListQuestion('I: What Identities will you embody to achieve your goal?', name='Identities'),
    ListQuestion('S: What are the Specifics of your goal?', name='Specifics'),
    ListQuestion('M: What Metrics will you use to track progress towards goal?', name='Metrics'),
    OrderedListQuestion('A: What Actions will you take to achieve your goal?', name='Actions'),
    ListQuestion('T: What are the Timelines for each action?', name='Timeline'),
    ListQuestion('I: What Information will you utilize to achieve your goal?', name='Information'),
    ListQuestion('C: What are your Criteria for Success to achieve this goal?', name='Criteria for Success'),
])

operation_self = Activity('Operation Self', [
    YesNoQuestion("Did you poop today?"),
    YesNoQuestion("Did you tell your significant other that you're experiencing this?").endwith('\n'),
    TextQuestion("Go ahead and reflect for a minute to try to clear your brain."),
    OrderedListQuestion("What can you do to turn this around?")
])

delegation_report = Activity('Delegation Report', [
    ListQuestion('What took your energy?', name='Energy Investments'),
    ListQuestion('What non-ceo activities did you do?', name='Non CEO Activities'),
    ListQuestion('To Do\'s - What Can be delegated?', name='Tasks to Delegate'),
    ListQuestion('What systems do we need?', name='Systems Needed'),
    ListQuestion('What can I stop doing?', name='Stop Doing List'),
])


morning_reflection = Activity('Morning Reflection', [
    reflect.rename('Reflection 1'),
    physiology,
    type_of_person,
    daily_intentions,
    gratitude,
    OrderedListQuestion('What are your top 3 priorities for the day (starting with THE ONE THING)?', limit=3),
    self_love,
    easier_life,
    ten_ideas_to_improve_your_life,
    reflect.rename('Reflection 2')
], intro_text='Good morning handsome ;)')

end_of_day_reflection = Activity('End of Day Reflection', [
    reflect.rename('Reflection 1'),
    daily_wins,
    improvements,
    daily_lessons,
    gratitude,
    meaningful_experience,
    self_love,
    Question('If you were to give this day a name, what would it be?', name='Name This Day'),
    OrderedListQuestion('What are your top 3 personal priorities for tomorrow (starting with THE ONE THING)?', limit=3, name='Tomorrow Personal Priorities'),
    OrderedListQuestion('What are your top 3 professional priorities for tomorrow (starting with THE ONE THING)?', limit=3, name='Tomorrow Professional Priorities'),
    reflect.rename('Reflection 2'),
], intro_text='Good evening sir! :)')

weekly_reflection = Activity('Weekly Reflection', [
    reflect.rename('Reflection 1'),
    weekly_wins,
    improvements,
    OrderedListQuestion('What are your top 3 personal priorities for the week (starting with THE ONE THING)?', limit=3, name='Tomorrow Personal Priorities'),
    OrderedListQuestion('What are your top 3 professional priorities for the week (starting with THE ONE THING)?', limit=3, name='Tomorrow Professional Priorities'),
    OrderedListQuestion('What are 10 ideas to crush it this week?', limit=10, name='10 Ideas to Crush It This Week'),
    ListQuestion('What does your perfect day look like this week?', name='Weekly Perfect Day'),
    reflect.rename('Reflection 2'),
], intro_text='I hope you had a nice week sir! :)')


monthly_reflection = Activity('Monthly Reflection', [
    reflect,
    ListQuestion('What were your wins for the month?', name='Monthly Wins'),
    improvements,
    ListQuestion('What are your top 3 priorities for the month (starting with THE ONE THING)?', name='Monthly Priorities'),
    OrderedListQuestion('What are 10 ideas to crush it this month?'),
    OrderedListQuestion('What does your perfect day look like this month?', name='Perfect Day')
], intro_text='Wow, a whole month. I hope you hada nice month sir! :)\n')


birthday_reflection = Activity('It\'s My Birthday', [
    OrderedListQuestion('What were your biggest wins wins year?', name='Yearly Wins'),
    improvements,
    OrderedListQuestion('What are your priorities for the year (starting with THE ONE THING)?', name='Birthday Priorities'),
    OrderedListQuestion('What are 10 ideas to make this year your most amazing year so far?', name='10 Ideas for the Best Year So Far')
], intro_text='Happy birthday sir! :)')

