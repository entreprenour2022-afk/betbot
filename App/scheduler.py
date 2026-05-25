from apscheduler.schedulers.blocking import BlockingScheduler
from main import run_bot

scheduler = BlockingScheduler()

scheduler.add_job(run_bot, 'interval', minutes=5)

scheduler.start() 