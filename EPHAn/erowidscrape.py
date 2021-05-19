from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
from tqdm import tqdm
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import os

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
'''
## grab all the text (citation, dose, body weight, up until date published and views, )
## export the text into a .txt file

main_url = 'https://www.erowid.org/experiences/exp_list.shtml'
#browser.get(main_url)


#substance_parents = browser.find_elements_by_tag_name('b')[3:]
#for parent in tqdm(list(substance_parents)):
    #try:


# navigate to deepest iterator in CSV: Substance, Experience type, then data (list of all experience links, columns for each link, category, and drug name)
# make folders for each substance inside of which i make a folder for each experience type
# and make files inside that are named by their ID
# os.path.exists: then makedires
# os makedirs export text file into a directory

'''        if row == substance_name:
            for substance in substance_name:
                if substance != substance + i:
                    substance_link = 'https://www.erowid.org/experiences/' + substance_name
                    browser.get(substance_link)'''

data_dir = '/Users/Ethan/Documents/Documents/Documents - Ethan’s MacBook Pro/GitHub/ErowidScraper/Orreen/data'
substance_path = data_dir + '/substance_text_folder'
exp_type_path = substance_path + '/experience_types_text_folder'
report_file = 'exp_type_text.txt'


def create_folders():
    experience_types_csv = pd.read_csv('experience_types.csv')
    experience_links_csv = pd.read_csv('experience_links.csv')
    for i, row in tqdm(list(experience_links_csv.iterrows())):
        substance_name = row['substance_name']
        # start by substance then go to experience type
        if not os.path.exists(substance_path):
            for sub_folder in substance_name:
                substance_folders = os.mdir(os.path.join(substance_path, sub_folder))
                for j, roww in tqdm(list(experience_types_csv.iterrows())):
                    experience_type = roww['experience_type']
                    if not os.path.exists(exp_type_path):
                        experience_type_links = roww['experience_type_link']
                        for exp_type in list(experience_type): # create sub_folder for each experience
                            experience_type_folders = os.mkdir(os.path.join(exp_type_path, exp_type))
                            return substance_folders, experience_type_folders


create_folders = create_folders()


def get_exp_reports():
    save_path = exp_type_path
    for folder in exp_type_path: # the directory
        for file in folder: # write files to each folder
            file_exists = os.path.isfile(file)
            for i, row in tqdm(list(experience_types_csv.iterrows())):
                experience_type_link = row['experience_type_link']
                full_exp_type_link = 'https://www.erowid.org/experiences/subs/' + experience_type_link
                browser.get(full_exp_type_link)
                report_parent_1 = browser.find_elements_by_tag_name('div')
                for parent1 in tqdm(list(report_parent_1)):
                    try:
                        report_title = parent1.find_element_by_class_name("title")
                        report_substance = parent1.find_element_by_class_name("substance")
                        author = parent1.find_element_by_class_name("author")
                        citation = parent1.find_element_by_class_name("ts-citation")
                    except NoSuchElementException as E:
                        pass

                report_parent_2 = browser.find_elements_by_class_name("report-text-surround")
                for parent2 in tqdm(list(report_parent_2)):
                    qs = parent2.find_elements_by_class_name("pullquote-right1")
                    try:
                        dose_chart = parent2.find_element_by_class_name("dosechart").text
                        body_weight = parent2.find_element_by_class_name("bodyweight").text
                        trip_txt = parent2.text
                        trip_txt = '\n'.join(trip_txt.split('\n')[:-2])
                        for q in qs:
                            if q.text in trip_txt:
                                trip_txt = trip_txt.replace(q.text, '', 1)
                                # print(q.text)
                        # print(trip_txt)
                    except NoSuchElementException as E:
                        pass

                file_name = report_title
                if not file_exists:
                    txt_file = os.path.join(save_path, file_name+".txt")
                    with open(txt_file, 'w') as text_file:
                        write_txt_files = text_file.write(trip_txt)
                        write_txt_files.close()

input()
browser.quit()