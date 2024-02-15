import requests
from bs4 import BeautifulSoup
import pandas as pd
import math

#page to extract profile
profile_url = "https://pureportal.coventry.ac.uk/en/organisations/ihw-centre-for-health-and-life-sciences-chls/persons/"

response = requests.get(profile_url)
soup = BeautifulSoup(response.text,'html.parser')

#total no. of pages
def get_total_pages():
    pager_info = soup.find('li', class_='search-pager-information').get_text(strip=True)
    total_results = int(pager_info.split('out of')[-1].strip().split()[0])
    total_pages = math.ceil(total_results/50)
    return(total_pages)


# Define the URL
base_url = "https://pureportal.coventry.ac.uk/en/organisations/ihw-centre-for-health-and-life-sciences-chls/persons/?page={}"

# Initialize empty lists to store data
person_names = []
person_links = []

# Loop over pages
for i in range(0, get_total_pages()):
    p_url = base_url.format(i)
    response = requests.get(p_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    containers = soup.find_all('div', {'class': 'result-container'})

    # Iterate over containers
    for container in containers:
        person_name = container.find('h3', {'class': 'title'}).text.strip()
        a_tag = container.find('a')
        person_link = a_tag['href'] if a_tag else None
        person_names.append(person_name)
        person_links.append(person_link)

# Create a DataFrame after collecting data from all pages
df = pd.DataFrame({'Person Name': person_names, 'Person Link': person_links})

# Splitting the 'Person Name' column into individual names
names = df['Person Name'].str.split()

# Extracting the first name and last name
first_name = names.str[0]
last_name = names.str[-1]

# Constructing the middle name initials if available
middle_name_initials = names.apply(lambda x: x[1][0] if len(x) > 2 else '')

# Creating the new column with the desired format
df['New Column'] = last_name + ', ' + first_name.str[0] + middle_name_initials
df.to_csv('persons.csv',index=False)

