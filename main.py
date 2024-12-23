import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_jobs(url):
    jobs = []
    
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        job_cards = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
        
        for job_card in job_cards:
            title = job_card.find('h2', class_='heading-trun').get_text(strip=True)
            company = job_card.find('h3', class_='joblist-comp-name').get_text(strip=True)
            description = job_card.find('li', class_='job-description__').get_text(strip=True)
            salary = job_card.find('div', class_='srp-skills').get_text(strip=True)
            
            jobs.append({
                'Title': title,
                'Company': company,
                'Description': description,
                'Salary': salary
            })


    except Exception as e:
        print(f"An error occurred: {e}")
    
    return jobs

def save_to_csv(jobs, filename):
    """Save the job postings to a CSV file."""
    df = pd.DataFrame(jobs)
    df.to_csv(filename, index=False)
    print(f"Saved {len(jobs)} jobs to {filename}")

if __name__ == "__main__":
    url = "https://www.timesjobs.com/candidate/job-search.html?searchType=Home_Search&from=submit&asKey=OFF&txtKeywords=&cboPresFuncArea=35&clusterName=CLUSTER_FA&hc=CLUSTER_FA"
    
    print("Fetching jobs...")
    jobs = fetch_jobs(url)
    
    if jobs:
        print(f"Fetched {len(jobs)} jobs. Saving to CSV...")
        save_to_csv(jobs, "jobs.csv")
    else:
        print("No jobs found.")
