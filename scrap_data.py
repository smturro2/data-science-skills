import numpy as np
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# user define function
# Scrape the data
# and get in string
def getdata(url):
    r = requests.get(url)
    return r.text


# filter job data using
# find_all function
def job_data(soup):
    # find the Html tag
    # with find()
    # and convert into string
    data_str = ""
    soup.find_all("div", id="jobDescriptionText")
    for item in soup.find_all("div", class_="job_seen_beacon"):
        data_str = data_str + item.get_text()
    result_1 = data_str.split("\n")
    return (result_1)


# filter company_data using
# find_all function


def company_data(soup):
    # find the Html tag
    # with find()
    # and convert into string
    data_str = ""
    result = ""
    for item in soup.find_all("div", class_="sjcl"):
        data_str = data_str + item.get_text()
    result_1 = data_str.split("\n")

    res = []
    for i in range(1, len(result_1)):
        if len(result_1[i]) > 1:
            res.append(result_1[i])
    return (res)

def get_jobs(all_these_words,none_these_words,location="Chicago,+IL",explvl="entry_level",limit=50,fromage=15):
    url = "https://www.indeed.com/jobs?"
    url += f"q={'+'.join(all_these_words)}"
    url += f"+-{',+-'.join(none_these_words)}"
    url += f"&l={location}"
    url += f"&explvl={explvl}"
    url += f"&limit={limit}"
    url += f"&fromage={fromage}"

    # specify driver path
    DRIVER_PATH = '\dev\projects\data-science-skills\chromedriver_win32_99\chromedriver'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get(url)
    driver.implicitly_wait(3)

    df_jobs = pd.DataFrame()

    # For each page
    for i in range(0, 1):

        job_card = driver.find_elements(by=By.XPATH, value='//a[contains(@class,"tapItem")]')

        for job in job_card:
            job_dict = {}
            job_dict["title"] = job.find_elements(by=By.XPATH, value='.//h2[contains(@class,"jobTitle")]//span')[-1].get_attribute(name="title")
            job_dict["company"] = job.find_element(by=By.XPATH, value='.//span[@class="companyName"]').text
            job_dict["link"] = job.get_attribute(name="href")

            try:
                job_dict["salary"] = job.find_elements(by=By.XPATH, value='.//div[contains(@class,"salary")]//div')[0]
            except:
                pass

            try:
                job_dict["location"] = job.find_element(by=By.XPATH, value='.//div[contains(@class,"companyLocation")]').text
            except:
                pass

            job_dict = pd.DataFrame([job_dict])
            df_jobs = pd.concat([df_jobs, job_dict], ignore_index=True)

        try:
            next_page = driver.find_element(by=By.XPATH, value='//span[@class="np"]')
            next_page.click()
        except:
            break # We got to last page
        print("Page: {}".format(str(i + 2)))

    # Now go through and get descriptions and reviews

    for i in range(len(df_jobs)):
        link = df_jobs.loc[i,"link"]
        driver.get(link)
        jd = driver.find_element(by=By.XPATH, value='//div[@id="jobDescriptionText"]').text
        df_jobs.loc[i,"desc"] = jd


        try:
            df_jobs.loc[i,"rating_value"] = driver.find_element(by=By.XPATH, value='.//meta[contains(@itemprop,"ratingValue")]').get_attribute("content")
            df_jobs.loc[i,"rating_count"] = driver.find_element(by=By.XPATH, value='.//meta[contains(@itemprop,"ratingCount")]').get_attribute("content")
        except:
            pass

    return df_jobs



if __name__ == "__main__":
    all_these_words = ["python", "data"]
    none_these_words = ["Doctor", "PHD","PH.D", "masters", "Master", "Ph.D.", "Doctorate", "MS", "PhD"]

    df_jobs = get_jobs(all_these_words,none_these_words)
    df_jobs.to_csv("raw.colan",sep="}")
    # pd.read_csv("raw.colan", sep="}")


