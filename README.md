"""
LinkedIn Job Scraper
- Logs in with Selenium
- Scrapes job title, company, date
- Saves to CSV
- Shows top hiring companies (bar chart)
"""

import time, os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Load credentials
load_dotenv()
EMAIL, PASSWORD = os.getenv("LINKEDIN_EMAIL"), os.getenv("LINKEDIN_PASSWORD")

# Setup browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.linkedin.com/login")

# Login
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(EMAIL)
driver.find_element(By.ID, "password").send_keys(PASSWORD + Keys.RETURN)
time.sleep(5)

# Search Jobs
driver.get("https://www.linkedin.com/jobs/search/?keywords=Python%20Developer&location=India")
time.sleep(5)
for _ in range(3): driver.find_element(By.TAG_NAME,"body").send_keys(Keys.END); time.sleep(2)

# Scrape
soup = BeautifulSoup(driver.page_source, "html.parser")
jobs = [[j.find("h3").text.strip(), j.find("h4").text.strip(), (j.find("time") or "").text.strip()]
        for j in soup.find_all("div", class_="base-card")]

driver.quit()

# Save CSV
df = pd.DataFrame(jobs, columns=["Job Title","Company","Date"]).drop_duplicates()
df.to_csv("linkedin_jobs.csv", index=False)
print("Saved linkedin_jobs.csv")

# Visualize
df["Company"].value_counts().head(10).plot(kind="bar", color="skyblue", title="Top Hiring Companies")
plt.ylabel("Job Count"); plt.show()
