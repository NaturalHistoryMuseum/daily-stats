import requests
from datetime import date
import gbif_dbtools as db

today = date.today()

resource_id = "05ff2255-c38a-40c9-b657-4ccb55ab2feb"
action_url = "https://data.nhm.ac.uk/api/3/action/vds_multi_stats"
field = "associatedMediaCount"

r = requests.get(f"{action_url}?resource_ids={resource_id}&field={field}")
result = r.json()["result"]
# the number of images in the specimen collection
image_count = int(result["sum"])
# the number of specimens with images
imaged_count = int(result["count"])

# insert into dashboard.specimen_images
sql = f"""
INSERT INTO specimen_images (date, image_count, imaged_specimens, resource_id)
VALUES ('{today}', {image_count}, {imaged_count}, '{resource_id})')
"""

db.query_db(sql)
