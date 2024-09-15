import os
import random
import time
from datetime import datetime, timedelta

import yaml
from notifypy import Notify

exercises = [
    "Ten push-ups",
    "Handstand",
    "60 second plank",
    "Stretch hamstrings and hip flexors",
    "Spinal waves",
    "Take a short walk",
    "Five pullups",
    "Five dips",
]


def run_timer(duration=25 * 60):
    end_time = datetime.now() + timedelta(seconds=duration)
    print(f"\nTimer started for {duration // 60} minutes...")

    while True:
        remaining_time = end_time - datetime.now()
        if remaining_time.total_seconds() <= 0:
            break
        mins, secs = divmod(int(remaining_time.total_seconds()), 60)
        time_format = f"{mins:02d}:{secs:02d}"
        print(time_format, end="\r")
        time.sleep(1)


def notify_user(intention, exercise):
    notification = Notify()
    notification.title = "Time for a break"
    notification.message = f"intention: {intention} exercise: {exercise}"
    notification.send()


def log_intention(intention, achieved):
    journal_dir = os.path.expanduser("~/.cache/tomato-journal/")
    os.makedirs(journal_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    journal_file = os.path.join(journal_dir, f"{date_str}.yaml")

    # Create the entry
    entry = {
        "intention": intention,
        "achieved": achieved,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
    }

    # Load existing journal entries if the file exists
    if os.path.exists(journal_file):
        with open(journal_file, "r") as file:
            journal = yaml.safe_load(file) or []
    else:
        journal = []

    # Append the new entry
    journal.append(entry)

    # Save the updated journal back to the file
    with open(journal_file, "w") as file:
        yaml.safe_dump(journal, file)

    print(f"\nIntention logged in {journal_file}\n")


def main():
    while True:
        intention = input("\nWhat is your intention for the next 25 minutes? ")
        run_timer()
        exercise = random.choice(exercises)
        notify_user(intention, exercise)
        achieved = input("\nDid you achieve your intention? (yes/no): ").strip().lower()
        achieved = True if achieved in ["yes", "y"] else False
        print(f"\nSuggested break exercise: {exercise}\n")
        log_intention(intention, achieved)


if __name__ == "__main__":
    main()
