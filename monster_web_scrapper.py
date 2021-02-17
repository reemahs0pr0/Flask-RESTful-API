from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd

def scrap_jobs():
    ### Code for running the webscrapper to scrape links to individual jobs ###
    df = pd.DataFrame()
    jobTitle = list()
    jobLink = list()
    
    # change urlfront and urlend to scrape different queries
    urlfront = "https://www.monster.com.sg/srp/results?start="
    urlend = "&sort=2&limit=100&query=it&searchId=2b34467f-fc11-4651-98e3-a742474195f5"
    
    
    # leave this at 1
    start = 1
    
    # number of pages to scrape
    num_pages = 11
    
    
    for i in range(num_pages):
        # building the url string to scrape multiple pages
        url = urlfront + str(start) + urlend
        if start == 1:
            start += 99
        else:
            start += 100
        print(url)
    
        # initiating the webdriver. Parameter includes the path of the webdriver.
        driver = webdriver.Chrome('C:/Users/limkh/Downloads/chromedriver_win32/chromedriver.exe')
        driver.get(url)
    
        # this is just to ensure that the page is loaded
        time.sleep(5)
    
        html = driver.page_source
    
        # Now, we could simply apply bs4 to html variable
        soup = BeautifulSoup(html, "html.parser")
        joblinks = soup.find_all(class_="job-tittle")
        driver.close()  # closing the webdriver
    
        for j in joblinks:
            # finds the <a> tags with data-v-5d88d458 as that contains link to html page
    
            ahref = j.find("a", {"data-v-5d88d458": ""})
            jobTitle.append(ahref.string)
            jobLink.append("https:" + ahref['href'])
    
    df['Job Title'] = jobTitle
    df['Job Link'] = jobLink
    
    # save the dataframe into a csv file with job title and job links which will be used in the part below to scrape web pages
    df.to_csv('1000monsters.csv', mode='a', header=True, encoding='utf-8', index=False)
    
    
    ### Getting the individual details from links saved above ###
    
    
    # reading from the saved csv before
    df3 = pd.read_csv('1000monsters.csv', encoding='utf-8')
    
    # getting number of rows to loop through
    index = df3.index
    number_of_rows = len(index)
    
    # scraping loop
    for i in range(number_of_rows):
        try:
    
            # this if is to scrape non sponsored links
            if "https://www.monster.com.sg/seeker/" in df3['Job Link'].iloc[i]:
    
                # Creating dataframe template for writting to csv
                rowdf = pd.DataFrame()
                rowdf['jobTitle'] = ""
                rowdf['companyName'] = ""
                rowdf['jobDescription'] = ""
                rowdf['skills'] = ""
                rowdf['jobAppUrl'] = ""
    
                # checking if seeker is present
                print("row " + str(i) + " seeker present")
    
                # getting link from dataframe from csv
                urlx = df3['Job Link'].iloc[i]
    
                # initiating the webdriver. Parameter includes the path of the webdriver.
                driver = webdriver.Chrome('C:/Users/limkh/Downloads/chromedriver_win32/chromedriver.exe')
                driver.get(urlx)
    
                # this is just to ensure that the page is loaded
                time.sleep(5)
    
                htmlx = driver.page_source
    
                soupx = BeautifulSoup(htmlx, "html.parser")
    
                driver.close()
                jdx = soupx.find('div', {'class': 'job-tittle detail-job-tittle'})
                jdtext = soupx.find('p', {'class': 'jd-text'})
    
        #         rowdf['Job Description'].iloc[0] = jdtext.get_text()
        #         rowdf['Company Name'].iloc[0] = jdx.a.get_text()
    
                jdskillspan = soupx.find_all('span', {'class': 'round-card mb5 grey-link'})
                jdskill = [r.get_text() for r in jdskillspan if r.a.has_attr('class') != True]
    
                string_skill = ""
                for jd in jdskill:
                    string_skill += jd
        #         rowdf['Skills'].iloc[0] = string_skill
        #         rowdf['Job Title'] = df3['Job Title'].iloc[i]
        #         rowdf['Job Link'] = df3['Job Link'].iloc[i]
    
                # placing the data into 1 row to append to the csv
                # data order as follows: 'Job title', 'Company Name', 'Job Description', 'Skills', 'Job Link'
                rowdf.loc[0] = [df3['Job Title'].iloc[i], jdx.a.get_text(), jdtext.get_text(), string_skill, df3['Job Link'].iloc[i]]
                rowdf.to_csv('fullmonsters.csv', mode='a', header=False, encoding='utf-8', index=False)
            print("row " + str(i) + " is done")
        except:
            print("error in row: " + str(i) + " occured")
            continue
    
    print("task fully completed")

if __name__ == '__main__':    
    scrap_jobs()