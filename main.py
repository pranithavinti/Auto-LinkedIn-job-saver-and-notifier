from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import smtplib
import time

CHROME_DRIVER_PATH = YOUR_CHROME_DRIVER_PATH
ACCOUNT_EMAIL = YOUR_LINKEDIN_EMAIL
ACCOUNT_PASSWORD = YPUR_LINKEDIN_PASSWORD
LINKEDIN_JOBS_URL = 'https://www.linkedin.com/jobs/'
JOB_KEYWORDS = ROLE_OR_COMAPANY_KEYWORDS
LOCATION = LOCATION_KEYWORD
MY_EMAIL = YOUR_EMAIL_ID
MY_PASSWORD = YOUR_EMAIL_PASSWORD
details = []

def email_job(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        company_name = soup.find(name="a", class_="topcard__org-name-link topcard__flavor--black-link")
        role = soup.find(name="h1", class_="top-card-layout__title topcard__title")
        location = soup.find(name="span", class_="topcard__flavor topcard__flavor--bullet")
        details.append(company_name.get_text().strip())
        details.append(role.get_text())
        details.append(location.get_text().strip())
        connection = smtplib.SMTP(host="smtp.gmail.com", port=587)
        connection.starttls()
        connection.login(user= MY_EMAIL, password= MY_PASSWORD)
        connection.sendmail(from_addr= MY_EMAIL,
                            to_addrs= MY_EMAIL,
                            msg=f"Subject:New job saved to My Jobs - LINKEDIN \n\nNew job has been saved to My Jobs. The details of the job are listed below.\n\n"
                                f"Company: {details[1]}\nRole: {details[2]}\nLocation: {details[3]}\nLink to apply: {details[0]}\n\nThree more relevant jobs added to My Jobs.")
        connection.close()
        print("successfully sent the mail")

    except Exception as e:
        print(str(e))
        print("failed to send mail")


opt = Options()
opt.headless = True
chrome_driver_path = YOUR_CHROME_DRIVER_PATH
ser = Service(chrome_driver_path)

driver = webdriver.Chrome(service=ser)
driver.get(LINKEDIN_JOBS_URL)
time.sleep(2)
job_keyword_field = driver.find_element(By.NAME, "keywords")
location_field = driver.find_element(By.NAME, "location")
location_field.clear()
job_keyword_field.send_keys(JOB_KEYWORDS)
location_field.send_keys(LOCATION)
location_field.send_keys(Keys.ENTER)

top_job = driver.find_element(By.CLASS_NAME,"base-card__full-link")
top_job.click()
time.sleep(3)

sign_in = driver.find_element(By.CLASS_NAME,"nav__button-secondary")
sign_in.click()
time.sleep(3)

email = driver.find_element(By.NAME, "session_key")
email.send_keys(ACCOUNT_EMAIL)

password = driver.find_element(By.NAME, "session_password")
password.send_keys(ACCOUNT_PASSWORD)
password.send_keys(Keys.ENTER)
time.sleep(2)

save = driver.find_element(By.CSS_SELECTOR,"button.jobs-save-button")
save.click()
time.sleep(3)
job_post_url = driver.current_url
details.append(job_post_url)
email_job(job_post_url)

driver.back()
driver.back()
driver.back()
time.sleep(3)

jobs_list = driver.find_elements(By.CSS_SELECTOR, "div.job-card-container")
top_three_jobs = jobs_list[0:3]
time.sleep(2)
save = driver.find_element(By.CSS_SELECTOR,"button.jobs-save-button")
for item in top_three_jobs:
    item.click()
    time.sleep(2)
    save.click()
print("Done saving top 3 jobs")
driver.quit()
