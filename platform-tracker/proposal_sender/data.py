from typing import Any, Iterable

import pandas as pd
from .base_job import Job

from proposal_sender.settings import DATA_DIR, EXPERTISE, EXPERTISE_SECOND_TIER, EXPERTISE_BLACKLIST

DATA_DIR.mkdir(exist_ok=True)


def save_jobs(jobs: Iterable[Job]) -> None:
    # Save jobs to a CSV file. If the file already exists, append to it. Drop duplicates, sort by oldest first. 
    # Also, save the jobs to a general CSV file for jobs from all platforms, which may have different columns,
    # and also save them to a CSV file for their specific platform. Each job has a .platform.name attribute.
    df = pd.DataFrame([job.to_dict() for job in jobs])
    df = df.drop_duplicates(subset=['url'])
    df = df.sort_values(by='publish_date', ascending=True)
    df.to_csv(DATA_DIR / 'jobs.csv', index=False, mode='a', header=not (DATA_DIR / 'jobs.csv').exists())
    for platform in set(df.platform):
        df_platform = df[df.platform == platform]
        df_platform.to_csv(DATA_DIR / f'{platform}.csv', index=False, mode='a', header=not (DATA_DIR / f'{platform}.csv').exists())



def get_unique_tags() -> set[str]:
    # Get all unique tags from the jobs CSV file.
    df = pd.read_csv(DATA_DIR / 'jobs.csv')
    tags = set()
    for tag in df.tags:
        tags.update(tag.split(', '))
    return tags


def get_unused_tags():
    tags = get_unique_tags()
    lowercase_blacklist = [tag.lower() for tag in EXPERTISE_BLACKLIST]
    lowercase_expertise_top_tier = [tag.lower() for tag in EXPERTISE]
    lowercase_expertise_second_tier = [tag.lower() for tag in EXPERTISE_SECOND_TIER]
    unused_tags = [tag for tag in tags if tag.lower() not in lowercase_blacklist and tag.lower() not in lowercase_expertise_top_tier and tag.lower() not in lowercase_expertise_second_tier]
    return unused_tags


def get_most_popular_tags() -> tuple[str,int]:
    # Get the most popular tags from the jobs CSV file.
    df = pd.read_csv(DATA_DIR / 'jobs.csv')
    tags = {}
    for tag in df.tags:
        for tag in tag.split(', '):
            if tag in tags:
                tags[tag] += 1
            else:
                tags[tag] = 1
    return sorted(tags.items(), key=lambda item: item[1], reverse=True)  # type: ignore



