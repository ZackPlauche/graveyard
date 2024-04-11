import pandas as pd
from wyzantapi import WyzantAPI


def test_get_job_count(chrome_driver):
    wyzant = WyzantAPI.start(chrome_driver)
    job_count = wyzant.get_job_count()
    print(job_count)
    assert job_count


def test_get_jobs(chrome_driver, data_dir):
    wyzant = WyzantAPI.start(chrome_driver)
    jobs = wyzant.get_jobs()
    df = pd.DataFrame([job.model_dump() for job in jobs])
    df.to_csv(data_dir / 'jobs.csv', index=False)
    assert jobs


def test_apply_to_job(chrome_driver):
    wyzant = WyzantAPI.start(chrome_driver)
    jobs = wyzant.get_jobs()
    job = jobs[0]
    wyzant.apply_to_job(job, f'Hey {job.student.name}! I\'d love to help you with this 🙂. Would you like to have a call?', rate=job.recommended_rate)
    print(job.model_dump())
    assert job.application


def test_apply_to_jobs(chrome_driver):
    wyzant = WyzantAPI.start(chrome_driver)
    jobs = wyzant.get_jobs()
    for job in jobs:
        wyzant.apply_to_job(job, f'Hey {job.student.name}! I\'d love to help you with this 🙂. Would you like to have a call?', rate=job.recommended_rate)
    pd.DataFrame([job.model_dump() for job in jobs]).to_csv('jobs.csv', index=False)
