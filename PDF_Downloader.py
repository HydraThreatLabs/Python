from bs4 import BeautifulSoup
import requests
import os
from tqdm import tqdm  # Progress bar for downloads

# URL of the page containing links to PDF files
url = "http://stanford.edu/class/cs114/readings/"

# Path to the folder where PDF files will be saved
folder = os.path.join("files", "pdfs")

# Creating an HTTP session
session = requests.session()

# Downloading the page content
response = requests.get(url)

# Parsing the HTML using BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Creating the folder if it does not exist
os.makedirs(folder, exist_ok=True)

# Iterating through all links on the page
for search in soup.find_all("a"):
    try:
        link = search.get("href")
        # Check if the link ends with ".pdf"
        if link.endswith(".pdf"):
            full_url = url + link  # Creating the full URL to the PDF file

            # Sending a HEAD request to get the file size
            head = session.head(full_url)
            file_size = int(head.headers.get('content-length', 0))  # File size in bytes

            # Downloading the PDF file in streaming mode
            pdf_response = session.get(full_url, stream=True)

            # Path to save the file
            file_path = os.path.join(folder, link)

            # Opening the file for writing and displaying the progress bar
            with open(file_path, "wb") as pdf_file, tqdm(
                desc=f"Downloading {link}",
                total=file_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024
            ) as bar:
                # Writing the file data chunk by chunk
                for chunk in pdf_response.iter_content(chunk_size=1024):
                    pdf_file.write(chunk)
                    bar.update(len(chunk))  # Updating the progress bar

            print(f"Saved file {file_path}")  # Information about completion of saving
    except Exception as e:
        print(e)  # Handling possible errors

