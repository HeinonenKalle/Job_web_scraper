#This simple scraper was made by Kalle Heinonen, it was made for a specific topic, so it might need a few tweaks to work
#After making this I realised Duunitori does not allow robots, which could have been checked by using https://duunitori.fi/robots.txt.

import requests
from bs4 import BeautifulSoup
import csv


"""
Potential improvements:
Add the information to a csv file, remember to use "a" option not to overwrite previous data so you can save the data every time
a job posting is found and not only when the program is finished.
Improve efficiency:
Use multithreading:
Writing on csv file and communicating which pages diffrent cores read might be difficult. Come back later once multithreading course has progressed further.
"""

def main():
    #start a session
    s = requests.Session()
    #The cookies needed, since gdpr laws now require you to accept them
    s.cookies.update({'duunitori_gdpr_terms_accepted' : 'true'})
    #page counter
    the_page = 0
    while True:
        #the website design made it so 1 redirects to a completely different search results
        if the_page != 1:
            #Get an url and delete the page number on it 
            URL = "https://duunitori.fi/tyopaikat?alue=Tampere%3BHelsinki&haku=Trainee&order_by=date_posted&sivu=" + str(the_page)
            page = s.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            #Makes a list of all the jobs on the page
            results = soup.find_all("a", class_="job-box__hover gtm-search-result")
            #once all of the pages have been gone thru, scraper stops
            if(len(results) == 0):
                return
            #for loop goes thru every job posting
            for link in results:
                #in the divs they also provided a href to the posting, so we can get that by using:
                temp_link = link.get('href')
                searchpage = "https://duunitori.fi" + temp_link
                new_page = s.get(searchpage)
                #keywords to look for certain talent, would be more efficient if i could easily scrape the specific divs
                #more keywords can be added with an or statement or removed by removing the or statement and the text after that
                if new_page.text.find("C++") != -1 or new_page.text.find("Python") != -1:
                    print(searchpage)
                    temp_soup = BeautifulSoup(new_page.content, "html.parser")
                    #gets information like what company and where the job is
                    job_post_data = temp_soup.find_all('p', class_="header__info")
                    list_of_data = []
                    for k in job_post_data:
                        #The object is NavigableString so lets make it a normal string
                        test = k.get_text()
                        list_of_data.append(test)
                    final_list = []
                    for c in list_of_data:
                        #and now lets remove \n:s from the data to make it readable
                        final_list.append(c.replace("\n", ""))
                    print("Company and location " + final_list[0])
                    print("When was the application released and when is the last time to apply " + final_list[1])
                    with open('jobs.csv', 'a') as open_file:
                        writer_object = csv.writer(open_file)
                        writer_object.writerow([final_list[0], final_list[1], searchpage])
                        open_file.close()
        #goes to the next page
        the_page += 1
        
main()
