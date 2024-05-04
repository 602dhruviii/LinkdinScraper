from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import datetime, timedelta
import time
import schedule

def scrape_linkedin(domain):
    options = Options()
    options.headless = True  # Run Chrome in headless mode (no GUI)
    service = Service("C:/Program Files/Google/Chrome/Application/chromedriver.exe")  # Replace 'path_to_chromedriver' with the actual path to your chromedriver executable
    driver = webdriver.Chrome(service=service, options=options)

    url = f'https://www.linkedin.com/jobs/search/?keywords={domain}&datePosted=1&sortBy=DD'
    driver.get(url)
    time.sleep(5)  # Wait for the page to load (adjust the time as needed)

    job_items = driver.find_elements(By.XPATH, '//div[@class="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card"]')
    print(job_items)
    postings = []
    for job_item in job_items:
        title = job_item.find_element(By.XPATH, './/div[@class="base-search-card__info"]/h3').text
        company = job_item.find_element(By.XPATH, './/div[@class="base-search-card__info"]/h4').text
        location = job_item.find_element(By.XPATH, './/div[@class="base-search-card__info"]/div[@class="base-search-card__metadata"]/span').text
        postings.append({
            'Title': title,
            'Company': company,
            'Location': location,
            'Source':"Linkedin"
        })

    driver.quit()
    return postings

def scrape_glassdoor(domain):
    options = Options()
    options.headless = True  # Run Chrome in headless mode (no GUI)
    service = Service("C:/Program Files/Google/Chrome/Application/chromedriver.exe")  # Replace 'path_to_chromedriver' with the actual path to your chromedriver executable
    driver = webdriver.Chrome(service=service, options=options)

    url = f'https://www.glassdoor.com/Job/jobs.htm?sc.keyword={domain}&locT=C&locId=12345&locKeyword=India'
    driver.get(url)
    time.sleep(5)  # Wait for the page to load (adjust the time as needed)

    job_items = driver.find_elements(By.XPATH, '//div[@class="JobCard_jobCardContainer___hKKI"]/div[1]')
    print(job_items)
    postings = []
    for job_item in job_items:
        title = job_item.find_element(By.XPATH, './/div[1]/a[1]').text
        company = job_item.find_element(By.XPATH, './/div[1]/div[@class="EmployerProfile_profileContainer__VjVBX EmployerProfile_compact__nP9vu"]/div[2]/span').text
        location = job_item.find_element(By.XPATH, './/div/div[@class="JobCard_location__rCz3x"]').text
        postings.append({
            'Title': title,
            'Company': company,
            'Location': location,
            'Source':"GlassDoor"
        })

    driver.quit()
    return postings
def main(domain):
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    data = []
    data.extend(scrape_linkedin(domain))
    data.extend(scrape_glassdoor(domain))
    df = pd.DataFrame(data)
    df.to_excel(f'{domain}_postings_{yesterday.strftime("%Y-%m-%d")}.xlsx', index=False)

def job_scheduler():
    domain = input("Enter the domain keyword: ")
    main(domain)
    schedule.every(24).hours.do(main, domain)

if __name__ == "__main__":
    job_scheduler()
    while True:
        schedule.run_pending()
        time.sleep(1)
