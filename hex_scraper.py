import requests
from bs4 import BeautifulSoup 
import pandas as pd


# load the Hex careers page 
session = requests.Session()
page = session.get('https://hex.tech/careers/')

# save the contents of the page 
soup = BeautifulSoup(page.content, "html.parser")

# create an empty list to store the URLs that I can later filter to get job title postings
href_list = []

# find all the links on the careers page and save them to a list 
for a in soup.find_all('a', href=True):
    href_list.append(a['href'])

# saving the href list to a new dataframe and renaming the column 
url_df = pd.DataFrame({'career_urls':href_list})

# looking for just the links that contain careers but are not equal to the exact /careers path 
career_urls = url_df[
    (url_df["career_urls"].str.contains("careers"))
    & (url_df["career_urls"] != "/careers/")
]

# stripping the careers part of the URL and stripping the trailing slash to get the final job titles
cleaned_postings = (
    career_urls["career_urls"].str.replace("/careers/", "").str.rstrip("/")
)

# back to a dataframe so i can visualize this as a table below 
cleaned_postings = pd.DataFrame(cleaned_postings)

# resetting the index and not inserting the old index as a column
cleaned_postings.reset_index(inplace=True, drop=True)

# get the length of the df to see the number of current role openings 
num_openings = int(len(cleaned_postings))

# finally, build back the URL specific for each job to get the posting 
cleaned_postings["listing_url"] = (
    "https://hex.tech/careers/" + cleaned_postings["career_urls"] + "/"
)
