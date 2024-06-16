import requests

# Define the endpoint URL and the file ID
base_url = "http://127.0.0.1:8000/files/download/"
file_id = "66566ce0b289a3d6789dafbe"

# Make a GET request to download the file
response = requests.get(f"{base_url}{file_id}", stream=True)

# Check if the request was successful
if response.status_code == 200:
    # Extract the filename from the Content-Disposition header
    content_disposition = response.headers.get('Content-Disposition')
    if content_disposition:
        filename = content_disposition.split("filename=")[-1].strip('"')

        # Save the file locally with the original filename
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File downloaded and saved as: {filename}")
    else:
        print("Filename not found in the response headers.")
else:
    print(f"Failed to download the file. Status code: {response.status_code}")
