from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from core import views


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(views.bulletin_email, 'interval', minutes=1440)
    scheduler.start()