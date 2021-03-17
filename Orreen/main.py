import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm
import time
import random
import numpy as np


data_dir = 'data'


def sleep_random(min_sec, max_sec):
    time.sleep(np.random.uniform(min_sec, max_sec))


def get_substances(browser=None, return_df=True):
    if not browser:
        browser = webdriver.Chrome()
        
    browser.get('https://www.erowid.org/experiences/exp_list.shtml')
    root = browser.find_element_by_tag_name('body')
    root_html = root.get_attribute('outerHTML')
    root_soup = BeautifulSoup(root_html, 'html.parser')
        
    substance_parents = root_soup.find_all('b')[3:]

    substance_dict = {'substance_name':[], 'substance_link':[]}

    for i, parent in tqdm(list(enumerate(substance_parents))):
        '''
        print(i)
        children = parent.find_elements_by_css_selector("*")  
        c_names = [c.tag_name for c in children]
        print(c_names)
        '''
        substance_tags = parent.find_all('a')
        
        if len(substance_tags) > 1:
            substance_tag = substance_tags[1]
            substance_link = substance_tag['href']
            substance_name_tag = substance_tag.find('u')
            substance_name = substance_name_tag.string
            substance_dict['substance_name'].append(substance_name)
            substance_dict['substance_link'].append(substance_link)

    substance_df = pd.DataFrame(substance_dict)

    substance_path = os.path.join(data_dir, 'substances.csv')
    substance_df.to_csv(substance_path, index=False)
    
    if return_df:
        return substance_df
    else:
        return None


def get_experience_types(browser=None, return_df=True):
    if not browser:
        browser = webdriver.Chrome()
        
    substance_path = os.path.join(data_dir, 'substances.csv')
    substance_df = pd.read_csv(substance_path)
    
    experience_type_dict = {'substance_name':[], 'experience_type':[], 'experience_type_link':[]}
    
    for i, row in tqdm(list(substance_df.iterrows())):
        substance_name = row['substance_name']
        substance_link = row['substance_link']
        full_substance_link = 'https://www.erowid.org/experiences/' + substance_link
        browser.get(full_substance_link)
        table = browser.find_elements_by_xpath('.//table[@border="0"][@cellspacing="0"][@cellpadding="4"]')
        if not table:
            continue
        table = table[0]
        table_html = table.get_attribute('outerHTML')
        table_soup = BeautifulSoup(table_html, 'html.parser')
        experience_types = table_soup.find_all('u')
        for exp_type in experience_types:
            exp_type_name = exp_type.string
            exp_parent = exp_type.find_parent('a')
            exp_type_link = exp_parent['href']
            experience_type_dict['substance_name'].append(substance_name)
            experience_type_dict['experience_type'].append(exp_type_name)
            experience_type_dict['experience_type_link'].append(exp_type_link)
        
        sleep_random(5, 7)
    
    experience_type_df = pd.DataFrame(experience_type_dict)

    experience_type_path = os.path.join(data_dir, 'experience_types.csv')
    experience_type_df.to_csv(experience_type_path, index=False)
    
    if return_df:
        return experience_type_df
    else:
        return None


def get_experience_links(browser=None, return_df=True):
    if not browser:
        browser = webdriver.Chrome()
    
    experience_type_path = os.path.join(data_dir, 'experience_types.csv')
    experience_type_df = pd.read_csv(experience_type_path)
    
    experience_dict = {'substance_name':[], 'experience_type':[], 'experience_link':[], 'rating':[], 'title':[], 'author':[], 'substance_list':[], 'pub_date':[]}
    
    def get_experience_links_page(page_soup, experience_dict, substance_name, experience_type):
        exp_table = page_soup.select('table[class="exp-list-table"]')
        if not exp_table:
            return
        exp_table = exp_table[0]
        exp_rows = exp_table.select('tr[class]')
        for exp_row in exp_rows:
            cells = exp_row.find_all('td')
            rating = ""
            rating_opt = cells[0].select('img[alt]')
            if rating_opt:
                rating_cell = rating_opt[0]
                rating = rating_cell['alt']
            title = cells[1].string
            link_cell = cells[1].find('a')
            if not link_cell:
                print("NO LINK NOT GOOD!")
                print("Substance =", substance_name)
                print("Experience Type =", experience_type)
                print("Title =", title)
                continue
            link = link_cell['href']
            author = cells[2].string
            substance_list = cells[3].string
            pub_date = cells[4].string
            experience_dict['substance_name'].append(substance_name)
            experience_dict['experience_type'].append(experience_type)
            experience_dict['experience_link'].append(link)
            experience_dict['rating'].append(rating)
            experience_dict['title'].append(title)
            experience_dict['author'].append(author)
            experience_dict['substance_list'].append(substance_list)
            experience_dict['pub_date'].append(pub_date)
    
    for i, row in tqdm(list(experience_type_df.iterrows())):
        substance_name = row['substance_name']
        experience_type = row['experience_type']
        experience_type_link = row['experience_type_link']
        full_exp_type_link = 'https://www.erowid.org/experiences/subs/' + experience_type_link
        browser.get(full_exp_type_link)
        page_exists = True
        while(page_exists):
            page_html = browser.find_element_by_tag_name('body').get_attribute("outerHTML")
            page_soup = BeautifulSoup(page_html, 'html.parser')
            get_experience_links_page(page_soup, experience_dict, substance_name, experience_type)
            results_table = page_soup.select('table[class="results-table"]')
            if not results_table:
                page_exists = False
                break
            results_table = results_table[0]
            next_button = results_table.select('img[alt="next"]')
            if not next_button:
                page_exists = False
                break
            next_button = next_button[0]
            next_page_element = next_button.find_parent('a')
            next_page_link = next_page_element['href']
            full_next_page_link = 'https://www.erowid.org' + next_page_link
            browser.get(full_next_page_link)
            ##print("Multiple pages for", substance_name, ":", experience_type)
            
            sleep_random(5, 7)
        
        sleep_random(5, 7)
        
    experience_df = pd.DataFrame(experience_dict)

    experience_path = os.path.join(data_dir, 'experience_links.csv')
    experience_df.to_csv(experience_path, index=False)
    
    if return_df:
        return experience_df
    else:
        return None
        

if __name__ == "__main__":
    browser = webdriver.Chrome()

    get_experience_links(browser=browser, return_df=False)

    input("Press ENTER to continue...")
    browser.quit()

