from fastapi import BackgroundTasks
from typing import Callable
from core.logging import logger


# Example background task for sending emails
async def send_email(email: str, subject: str, body: str):
    logger.info(f"Sending email to {email} with subject '{subject}'")
    # Simulate email sending logic here


# Example background task for generating reports
async def generate_report(report_id: int):
    logger.info(f"Generating report with ID {report_id}")
    # Simulate report generation logic here


# Utility to add tasks to FastAPI's BackgroundTasks
def add_background_task(
    background_tasks: BackgroundTasks, task: Callable, *args, **kwargs
):
    background_tasks.add_task(task, *args, **kwargs)
