from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
from tqdm import tqdm
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

browser = webdriver.Chrome(executable_path='/Users/Ethan/Library/Python/3.7/lib/python/site-packages/selenium/chromedriver')
'''
browser.get('https://www.erowid.org/experiences/exp_list.shtml')

# use .// to start at parent element so that we don't go all the way back to browser
substance_parents = browser.find_elements_by_tag_name('b')[3:]

substance_dict = {'substance_name':[], 'substance_link':[]}

for parent in tqdm(list(substance_parents)):
    try:
        substance_tags = parent.find_elements_by_tag_name('a')
        if len(substance_tags) > 1:
            substance_tag = substance_tags[1]
            substance_link = substance_tag.get_attribute('href')
            substance_name = substance_name_tag.text
            substance_dict['substance_name'].append(substance_name)
            substance_dict['substance_link'].append(substance_link)
    except NoSuchElementException as e:
        pass

substance_df = pd.DataFrame(substance_dict)
browser.quit()
'''
my_url = 'https://www.erowid.org/experiences/exp.php?ID=25991'
browser.get(my_url)

report_parent1 = browser.find_elements_by_tag_name('div')
for parent in tqdm(list(report_parent1)):
    try:
        # browser works before try for loop
        report_title = browser.find_element_by_class_name("title")
        report_substance = browser.find_element_by_class_name("substance")
        author = browser.find_element_by_class_name("author")
        citation = browser.find_element_by_class_name("ts-citation")
    except NoSuchElementException as e:
        pass

report_parent2 = browser.find_elements_by_class_name("report-text-surround")
for parent in tqdm(list(report_parent2)):
    quotes = parent.find_elements_by_class_name("pullquote-right1")
    try:
        dose_chart = parent.find_element_by_class_name("dosechart").text
        ### print(dose_chart)
        body_weight = parent.find_element_by_class_name("bodyweight").text
        ### print(body_weight)
        trip_text = parent.text
        trip_text = '\n'.join(trip_text.split('\n')[:-2])  # take all these things in a list and join them with this string -> \n in beginning

        for quote in quotes:
            if quote.text in trip_text:
                trip_text = trip_text.replace(quote.text, '', 1)
                print(quote.text)
        print(trip_text)

        #for quote in list(quotes):
            ### print(quote.text) # prints all quotes
    except NoSuchElementException as e:
        pass

## grab all the text (citation, dose, body weight, up until date published and views, )
## export the text into a .txt file

main_url = 'https://www.erowid.org/experiences/exp_list.shtml'
#browser.get(main_url)


#substance_parents = browser.find_elements_by_tag_name('b')[3:]
#for parent in tqdm(list(substance_parents)):
    #try:
input()
browser.quit()
