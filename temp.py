
from datetime import datetime

today = datetime.now()

if today.hour < 12:
    h = "00"
else:
    h = "12"

print(f"{'Uername'}-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")