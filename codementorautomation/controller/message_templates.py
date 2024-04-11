"""Message templates for the bot.

The templates have access to both the job and user objects. You can add them to
your template by adding it in brackets like this: {job} or {user}.

To get their attributes, just call it inside the brackets like this: {job.id}
or {user.first_name}.
"""


MESSAGE_TEMPLATE = '''\
Hey {user.first_name}!

I'd love to help you with this! 🙂

Would you like to schedule a call?'''