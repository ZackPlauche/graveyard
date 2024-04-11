"""
A list of simple godmode commands that you can use in your terminal if you'd like 
your bot to run commands off schedule or reaction from someone or something.
"""
import sys

from config import TOKEN, GROUP_CHAT_IDS
from telegram import Bot

bot = Bot(TOKEN)


def send_message(text, chat_id):
    """Send a message via the bot to a given chat."""

    bot.send_message(text=text, chat_id=chat_id)


def message_blast(text, chat_ids=GROUP_CHAT_IDS):
    """
    Send a message via the bot to every chat in in the
    GROUP_CHAT_IDS settings.
    """

    for chat_id in chat_ids:
        bot.send_message(chat_id=chat_id, text=text)




if __name__ == '__main__':
    import sys

    args = sys.argv[1:]
    if args:
        if args[0] == '-h':
            print( f"""\
Available commands:

- send

  Usage:
  
  Send to entire GROUP_CHAT_IDS list:
  python god.py send "Your text here"

  Send to a specific chat:
  python god.py send_message "Your text here" group_chat_id  
  OR
  python god.py send_message "Your text here" 1  # The 1 represents the index of the group in the GROUP_CHAT_IDS setting.
""")
        elif args[0] == 'send':
            if len(args) == 1:
                print('No text was added. Nothing was sent.')
            if len(args) >= 2:
                text = args[1]
                if len(args) <= 3:
                    try:
                        chat_id = int(args[2])
                        chat_id_is_index = abs(chat_id) <= (len(GROUP_CHAT_IDS) - 1)
                        if chat_id_is_index:
                            chat_id_index = chat_id
                            chat_id = GROUP_CHAT_IDS[chat_id_index]
                        send_message(text, chat_id)
                    except ValueError:
                        feedback = 'The argument you provided for chat_id must be an number.'
                        feedforward = 'Please either provide no chat_id argument or add a chat_id_index or chat_id'
                        print(feedback, feedforward, sep='\n')
                else:
                    message_blast(text)