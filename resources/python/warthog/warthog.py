import requests

r = requests.get("https://analytics.0xf10.com/api/event")

print(r.content)