from datetime import datetime, timezone, timedelta

def execute(argument: dict):
    # Always return India Standard Time (IST) since the user is in India (+5:30)
    tz = timezone(timedelta(hours=5, minutes=30))
    now = datetime.now(tz)
    return now.strftime("%d-%m-%Y %I:%M:%S %p")

