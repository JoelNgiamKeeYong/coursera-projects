import requests

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/InaFqKi-TlmTZwlzKvlNaQ/DV0101EN-Final-Assign-Part-2-Questions.py"
response = requests.get(url)

with open("DV0101EN-Final-Assign-Part-2-Questions.py", "wb") as file:
    file.write(response.content)

print("Download complete!")