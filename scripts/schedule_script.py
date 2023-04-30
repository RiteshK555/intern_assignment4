import schedule
import time
import subprocess

def job():
    subprocess.call(['python3', 'scripts/extract_whois.py'])

schedule.every().day.at("18:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
