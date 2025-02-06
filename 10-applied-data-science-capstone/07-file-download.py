import urllib.request

# URLs of the files to download
url_1 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
url_2 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/spacex_dash_app.py"

# Output file names
output_file_1 = "spacex_launch_dash.csv"
output_file_2 = "spacex_dash_app.py"

# Download the files
urllib.request.urlretrieve(url_1, output_file_1)
urllib.request.urlretrieve(url_2, output_file_2)

print(f"Files downloaded:\n{output_file_1}\n{output_file_2}")
