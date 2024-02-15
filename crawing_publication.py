import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import threading

def scrape_publications(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    publications = []

    # Iterate over each div with class "result-container"
    for container in soup.find_all('div', class_='result-container'):
        # Extract title
        title = container.find('h3', class_='title').text.strip()

        # Extract authors from 'a' tags
        authors = [author.text.strip() for author in container.find_all('a', class_='link person')]

        # Extract publication date
        publication_date = container.find('span', class_='date').text.strip()

        # Extract publication link
        publication_link = container.find('a', class_='link')['href']

        # Append the extracted information to the publications list
        publications.append({
            'Title': title,
            'Authors': authors,
            'Publication Date': publication_date,
            'Publication Link': publication_link
        })

    # Create a DataFrame from the publications list
    df = pd.DataFrame(publications)

    # Save the DataFrame to a CSV file
    df.to_csv('publications.csv', index=False)

def job():
    base_url = "https://pureportal.coventry.ac.uk/en/organisations/ihw-centre-for-health-and-life-sciences-chls/publications/"
    scrape_publications(base_url)
    # Reschedule the job after one week
    threading.Timer(604800, job).start()  # 604800 seconds = 1 week

# Run the job immediately
job()

# Keep the main thread alive
while True:
    time.sleep(1)
