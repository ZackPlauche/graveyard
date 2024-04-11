from dotenv import load_dotenv
from automation import Automation as WyzantAutomation


load_dotenv()

if __name__ == '__main__':
    WyzantAutomation.start()