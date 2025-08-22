from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Launch Chrome browser
driver = webdriver.Chrome()   # Make sure chromedriver is installed and in PATH
driver.get("https://www.linkedin.com/login")   # Open LinkedIn login page
time.sleep(3)   # wait for page to load

# step2

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Wait until username box is present
username = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "username"))
)
password = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "password"))
)

# Enter your credentials
username.send_keys("your_email_here")      # 👈 Replace with LinkedIn email
password.send_keys("your_password_here")   # 👈 Replace with LinkedIn password

# Submit form
password.send_keys(Keys.RETURN)

time.sleep(5)  # wait for LinkedIn homepage to load

#step 3


# -------------------
# Example: Python Developer jobs in India
search_url = "https://www.linkedin.com/jobs/search/?keywords=Python%20Developer&location=India"
driver.get(search_url)
time.sleep(5)  # wait for jobs page to load


# step 4



# Scroll multiple times to load more job cards
for i in range(3):   # 👈 increase number if you want more jobs
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)   # wait for new jobs to load


#step 5
from bs4 import BeautifulSoup


# -------------------
soup = BeautifulSoup(driver.page_source, "html.parser")

# Find all job cards
jobs = soup.find_all("div", {"class": "base-card"})

job_data = []
for job in jobs:
    title = job.find("h3", {"class": "base-search-card__title"})
    company = job.find("h4", {"class": "base-search-card__subtitle"})
    date = job.find("time")

    job_data.append({
        "Job Title": title.text.strip() if title else None,
        "Company": company.text.strip() if company else None,
        "Date": date.text.strip() if date else None,
    })

print(f"Scraped {len(job_data)} jobs ✅")


import pandas as pd


# Step 6: Save to CSV
# -------------------

# Convert list of dicts → DataFrame
df = pd.DataFrame(job_data)

# Remove duplicates (same title & company)
df.drop_duplicates(inplace=True)

# Save to CSV
df.to_csv("linkedin_jobs.csv", index=False)

print("Jobs saved to linkedin_jobs.csv ✅")

import matplotlib.pyplot as plt

# -------------------
# Step 7: Visualize Jobs by Company
# -------------------

# Count how many jobs each company posted
company_counts = df["Company"].value_counts().head(10)   # Top 10 companies

# Create bar chart
plt.figure(figsize=(10,6))
company_counts.plot(kind="bar")

plt.title("Top Companies Hiring (LinkedIn Jobs)")
plt.xlabel("Company")
plt.ylabel("Number of Job Listings")
plt.xticks(rotation=45)

plt.show()
