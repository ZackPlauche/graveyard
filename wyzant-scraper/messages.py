WYZANT_MIN_CHARS = 150

def pad_message(message: str) -> str:
    """Pad a message with spaces to reach the minimum number of characters"""
    return message + ' ' * (WYZANT_MIN_CHARS + 1 - len(message))


CAN_HELP_MESSAGE = 'Hey {client_name}! I\'d love to help you with this 🙂. Would you like to have a call?'

UNABLE_TO_HELP_MESSAGE = 'Dear {client_name}, While there are probably some things I can help you with, unfortunately I\'m not currently at a level where I can help you with this project 100%. I\'m sending you this because Wyzant doesn\'t have an option to remove a job from my view of jobs available. If you\'ve read my profile and think I could help you, feel free to reach out :) I appreciate your understanding and wish you the best. Respectfully, Zack P.'

OLD_JOB_MESSAGE = 'Hey {client_name}! I\'d love to help you with this 🙂 but it looks like you posted this a while ago. If you happen to still want any {subject} help, I\'d love to assist you 🙂. Please feel free to reach out.'