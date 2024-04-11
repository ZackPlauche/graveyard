from models import MessageTemplate

GENERAL_MESSAGE = MessageTemplate(
    name="General Message",
    template="""\
Hey {job.student.name}!

I'd love to help you with this 🙂.

Would you like to have a call?""",
)

