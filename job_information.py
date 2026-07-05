import requests
import time
import csv
from bs4 import BeautifulSoup

url = 'https://realpython.github.io/fake-jobs/jobs/senior-python-developer-0.html'

request_delay = 1

def get_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'lxml')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None
    
def extract_job_information(job, url):
    title_tag = job.find('h1',class_='title')
    title = title_tag.get_text(strip=True) if title_tag else 'N/A'

    company_tag = job.find('h2', class_='company')
    company = company_tag.get_text(strip=True) if company_tag else 'N/A'

    location_tag = job.find('p', id='location')
    cleaned_location_tag = location_tag.contents[1].strip()
    location = cleaned_location_tag.get_text(strip=True) if location_tag else 'N/A'

    return {
        'title': title, 
        'company': company,
        'location': location,
        'job_url': url
    }

def save_to_csv(job, filename='job_data.csv'):
    if not job:
        print("No job information to save.")
        return
    
    fieldnames = ['title', 'company', 'location', 'job_url']
    with open(filename, 'w',newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(job)

    print(f"Successfully saved job information to {filename}")

def main():
    print(f"Extracting job information from {url}...")
    soup = get_url(url)

    if not soup:
        print("Failed to retrieve the job page.")
        return
    
    job_info = extract_job_information(soup, url)
    print(f"  Extracted: {job_info['title']} at {job_info['company']}")
    
    time.sleep(request_delay)
    save_to_csv(job_info)


if __name__ == '__main__':
    main()