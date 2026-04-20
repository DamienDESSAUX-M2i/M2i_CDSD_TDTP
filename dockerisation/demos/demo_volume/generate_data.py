import json
from datetime import datetime, timezone

data = {"timestamp": datetime.now(timezone.utc).strftime("%d-%m-%Y %H:%M:%S")}

filename = (
    f"data_output/data_{datetime.now(timezone.utc).strftime('%d%m%Y%H%M%S')}.json"
)

with open(filename, "wt") as f:
    json.dump(data, f)
