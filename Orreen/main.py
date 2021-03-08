import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm


data_dir = 'data'


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
    

if __name__ == "__main__":
    browser = webdriver.Chrome()

    print(get_substances(browser, return_df=True))

    input()
    browser.quit()

