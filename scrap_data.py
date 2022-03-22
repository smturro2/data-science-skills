import numpy as np
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

class IndeedScraper:

    def __init__(self,imported_data=None):
        # specify self.driver path
        DRIVER_PATH = '\dev\projects\data-science-skills\chromedriver_win32_99\chromedriver'
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        if imported_data is None:
            self.df_jobs = pd.DataFrame()
        else:
            self.df_jobs = imported_data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.save_data("raw.txt")
        print("Crashed")

    def get_jobs(self,all_these_words,none_these_words=None,sort="relevance",location="Chicago,+IL",explvl="entry_level",limit=50,
                 fromage=None,educ="bachelor_degree"):
        url = "https://www.indeed.com/jobs?"
        url += f"q={'+'.join(all_these_words)}"
        url += f"&sort={sort}"
        if none_these_words is not None:
            url += f"+-{',+-'.join(none_these_words)}"
        if location is not None:
            url += f"&l={location}"
        if explvl is not None:
            url += f"&explvl={explvl}"
        if limit is not None:
            url += f"&limit={limit}"
        if fromage is not None:
            url += f"&fromage={fromage}"
        if educ is not None:
            url += f"&education={educ}"

        # For each page
        for i in range(20, 100):
            self.driver.get(url + f"&start={i*limit}")
            self.driver.implicitly_wait(1)

            # Ensure we turned the page
            try:
                # Ensure we turned the page
                page_num = self.driver.find_element(by=By.XPATH, value='//b[contains(@aria-current,"true")]').text
                # Close popup
                while page_num == "":
                    self.driver.implicitly_wait(1)
                    self.driver.find_element(by=By.XPATH,
                                             value='//button[contains(@class,"popover-x-button-close")]').click()
                    page_num = self.driver.find_element(by=By.XPATH, value='//b[contains(@aria-current,"true")]').text
                assert page_num == str(i + 1)
            except:
                break
            print("Page: {}".format(str(i + 1)))

            job_card = self.driver.find_elements(by=By.XPATH, value='//a[contains(@class,"tapItem")]')

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

                # Job desc and rating
                job.click()
                job_preview = self.driver.find_element(by=By.XPATH, value='//iframe[contains(@id,"vjs-container-iframe")]')
                self.driver.switch_to.frame(job_preview)
                jd = self.driver.find_element(by=By.XPATH, value='//div[@id="jobDescriptionText"]').text
                job_dict["desc"] = jd.replace("}", "{")
                try:
                    job_dict["rating_value"] = self.driver.find_element(by=By.XPATH,
                                                                                   value='.//meta[contains(@itemprop,"ratingValue")]').get_attribute(
                        "content")
                    job_dict["rating_count"] = self.driver.find_element(by=By.XPATH,
                                                                                   value='.//meta[contains(@itemprop,"ratingCount")]').get_attribute(
                        "content")
                except:
                    pass
                self.driver.switch_to.default_content()

                job_dict = pd.DataFrame([job_dict])
                self.df_jobs = pd.concat([self.df_jobs, job_dict], ignore_index=True)
            self.save_data("raw.txt")

    def get_desc_and_ratings(self):
        if "desc" not in self.df_jobs.columns:
            self.df_jobs["desc"] = np.nan
        jobs_to_get = self.df_jobs.index[self.df_jobs["desc"].isna()]
        max_jobs = 500
        print(f"{len(jobs_to_get)} jobs without descriptions out of {len(self.df_jobs)}")
        for i in jobs_to_get[:max_jobs]:
            link = self.df_jobs.loc[i, "link"]
            self.driver.get(link)
            self.driver.implicitly_wait(1)

            jd = self.driver.find_element(by=By.XPATH, value='//div[@id="jobDescriptionText"]').text
            self.df_jobs.loc[i, "desc"] = jd.replace("}", "{")
    
            try:
                self.df_jobs.loc[i, "rating_value"] = self.driver.find_element(by=By.XPATH,
                                                                     value='.//meta[contains(@itemprop,"ratingValue")]').get_attribute(
                    "content")
                self.df_jobs.loc[i, "rating_count"] = self.driver.find_element(by=By.XPATH,
                                                                     value='.//meta[contains(@itemprop,"ratingCount")]').get_attribute(
                    "content")
            except:
                pass
    
        return self.df_jobs

    def save_data(self,path="raw.txt"):
        self.df_jobs["location"] = self.df_jobs["location"].fillna("none")
        df_new = self.df_jobs.drop_duplicates(subset=["company","title","location"], keep="first")
        df_new.to_csv(path, sep="}",index=False)
        print(f"Data Saved.")
        print(f"Encountered {len(self.df_jobs) - len(df_new)} duplicates.")
        print(f"Now Have {len(df_new)} Total Jobs.")


if __name__ == "__main__":
    all_these_words = ["python", "data"]

    df_jobs = pd.read_csv("raw.txt", sep="}")
    with IndeedScraper(imported_data=df_jobs) as scrapper:
        try:
            scrapper.get_jobs(all_these_words, location=None)
            # scrapper.get_desc_and_ratings()
            scrapper.save_data()
        except:
            pass