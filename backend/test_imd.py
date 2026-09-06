from app.data.collectors.imd import IMDClient


client = IMDClient()

data = client.get_district_warnings(1)

print(data)