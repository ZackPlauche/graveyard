import logging
import codecs
import sys
import os
from pathlib import Path

import click
import matplotlib.pyplot as plt
import pandas as pd
from inquirer import prompt, Checkbox
from selenium.webdriver.remote.remote_connection import LOGGER as seleniumLogger
from selenium.webdriver.common.service import logger as seleniumServiceLogger
from selenium.webdriver.common.selenium_manager import logger as seleniumManagerLogger
from urllib3.connectionpool import log as urllibLogger

from controller import CodementorController
from database import Session, db_url
from database.models import Job, Expertise, BaseModel


try:
    logging_level = getattr(logging, os.getenv('LOGGING_LEVEL'))
except (TypeError, AttributeError) as e:
    logging_level = logging.INFO


logging.basicConfig(
    level=logging_level,
    format='%(asctime)s - %(levelname)-5s - %(message)s',
    handlers=[
        logging.FileHandler("codementor.log", 'a', encoding='utf-8'),
        logging.StreamHandler(codecs.getwriter('utf-8')(sys.stdout.buffer))
    ]
)

# Suppress all 3rd party package logs
seleniumLogger.setLevel(logging.WARNING)
seleniumServiceLogger.setLevel(logging.WARNING)
urllibLogger.setLevel(logging.WARNING)
seleniumManagerLogger.setLevel(logging.WARNING)


@click.group()
def cli():
    pass

@cli.command()
def update_reqs():
    os.system('pipenv run pip-chill --no-version --no-chill > requirements.txt')


@click.group()
def database():
    pass

@database.command()
@click.argument('model_name', type=str)
def count(model_name: str):
    models: BaseModel = BaseModel.__subclasses__()
    try:
        selected_model = [model for model in models if model.__tablename__ == model_name][0]
    except:
        print(f'No model found with name {model_name}.')
        return
    with Session() as session:
        count = selected_model.count(session)
        print(count)



@database.command()
def updatealembicurl():
    alembic_ini = Path('alembic.ini')
    alembic_ini_lines = alembic_ini.read_text().splitlines()
    alembic_ini_lines[62] = f'sqlalchemy.url = {db_url}'.replace('\\', '/')
    alembic_ini.write_text('\n'.join(alembic_ini_lines))


@database.command()
@click.option('--name', prompt='Name of migration', type=str)
def makemigrations(name: str):
    if not name:
        name = click.prompt('Migration name', type=str)
    os.system(f'alembic revision --autogenerate -m "{name}"')


@database.command()
def migrate():
    os.system('alembic upgrade head')


@database.command()
@click.option('--name', prompt='Name of migration', type=str)
def easymigrate(name: str):
    if not name:
        name = 'easymigrate'
    os.system(f'alembic revision --autogenerate -m "{name}" && alembic upgrade head')


@click.group()
def jobs():
    pass


@jobs.command()
@click.option('--path', prompt='Path to csv', type=str)
def exporttocsv(path: str):
    session = Session()
    jobs = [dict(job) for job in Job.all(session)]
    df = pd.DataFrame(jobs)
    df.to_csv(path, index=False)
    session.close()


@jobs.command()
def watch():
    controller = CodementorController.start()
    controller.watch_jobs()

@jobs.command()
def apply():
    controller = CodementorController.start()
    controller.apply_to_applicable_jobs()

@jobs.command()
def update_and_apply():
    controller = CodementorController.start()
    with Session() as session:
        not_updated_jobs = Job.filter_by(session, is_fully_updated=False).all()
        controller.update_and_apply_to_jobs(not_updated_jobs)

@jobs.command()
def update_without_users():
    with Session() as session:
        jobs_without_users = Job.filter_by(session, user_id=None).all()
    if jobs_without_users:
        logging.info('👀 Updating jobs without users...')
        controller = CodementorController.start()
        controller.update_and_apply_to_jobs(jobs_without_users)
    else:
        logging.info('👍 No jobs without users found.')  


@jobs.command()
def update_incomplete():
    controller = CodementorController.start()
    controller.update_incomplete_jobs()

@jobs.command()
def update_all():
    controller = CodementorController.start()
    controller.update_all_jobs()


@jobs.command()
def count_applicable():
    print(f'Applicable jobs: {Job.get_applicable(Session()).count()}')

@jobs.command()
def evaluate():
    Job.evaluate_all(Session())


@click.group()
def expertise():
    pass


@expertise.command()
def load_from_job_tags():
    logging.info('🔍 Updating expertise from tags...')
    Expertise.load_from_job_tags(Session())


@expertise.command()
def blacklist():
    with Session() as session:
        expertise = Expertise.get_unlisted(session)
        expertise_to_blacklist: list[Expertise] = prompt([
            Checkbox(
                name='expertise',
                message='Select expertise to blacklist',
                choices=expertise,
            )
        ])['expertise']
        for expertise in expertise_to_blacklist:
            expertise.is_blacklisted = True
        session.commit()
        print(f'✅ {len(expertise_to_blacklist)} expertise blacklisted.')


@expertise.command()
def unblacklist():
    with Session() as session:
        blacklist = Expertise.get_blacklisted(session)
        expertise_to_unblacklist: list[Expertise] = prompt([
            Checkbox(
                name='expertise',
                message='Select blacklist expertise to remove.',
                choices=blacklist,
            )
        ])['expertise']
        for expertise in expertise_to_unblacklist:
            expertise.is_blacklisted = False
        session.commit()
    print(f'✅ {len(expertise_to_unblacklist)} expertise unblacklisted.')



@expertise.command()
def whitelist():
    with Session() as session:
        unlisted_expertise = Expertise.get_unlisted(session)
        expertise_to_whitelist: list[Expertise] = prompt([
            Checkbox(
                name='expertise',
                message='Select blacklist expertise to remove.',
                choices=unlisted_expertise,
            )
        ])['expertise']
        for expertise in expertise_to_whitelist:
            expertise.is_whitelisted = True
        session.commit()
    print(f'✅ {len(expertise_to_whitelist)} expertise whitelisted.')

@expertise.command()
def unwhitelist():
    with Session() as session:
        whitelisted_expertise = Expertise.get_whitelisted(session)
        expertise_to_unwhitelist: list[Expertise] = prompt([
            Checkbox(
                name='expertise',
                message='Select whitelist expertise to remove.',
                choices=whitelisted_expertise,
            )
        ])['expertise']
        for expertise in expertise_to_unwhitelist:
            expertise.is_whitelisted = False
        session.commit()
    print(f'✅ {len(expertise_to_unwhitelist)} expertise unwhitelisted.')



@click.group()
def data():
    pass


@data.command()
def most_popular_tags():
    with Session() as session:
        most_popular_tags = Job.get_most_popular_tags(session)
    # plot tags
    plt.bar(*zip(*most_popular_tags[:20]))
    plt.xticks(rotation=90)
    plt.show()



cli.add_command(database)
cli.add_command(jobs)
cli.add_command(expertise)
cli.add_command(data)

if __name__ == '__main__':
    try:
        cli()
    except Exception as e:
        logging.exception(e)
        raise e

