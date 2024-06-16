import requests

# Assuming your endpoint is hosted at http://example.com
url = "http://127.0.0.1:8000/files/upload"
# filepath = "./download_file.py"
filepath = "IMG_0423.JPG"

# Assuming you have a file named "example.txt" in the same directory as your script
files = {'file': open(filepath, 'rb')}

response = requests.post(url, files=files)

# Print the response from the server
print(response.json())
