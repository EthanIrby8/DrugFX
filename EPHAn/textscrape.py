from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import pandas as pd


'''Method 3'''
browser = webdriver.Chrome(executable_path='/Users/Ethan/Library/Python/3.7/lib/python/site-packages/selenium/chromedriver')
browser.get('https://www.erowid.org/experiences/subs/exp_Salvia_divinorum_General.shtml')

reports = browser.find_elements_by_class_name('exp-list-table') # use this to loop through each value of interest under the table

# parentElement = find_elements_by_tag_name("tr")
# titleList = parentElement.find_elements_by_xpath("td[2]")

'''
("//*[id="results-form"]/table/tbody/tr[3]/td[2]/a)[1]
"//a[contains(text(), 'Goodbye Reality, Goodbye Universe')]"
'''
trip_reports = []
# I;ve concluded that the html for Erowid is fucking awful and i shouldnt waste my time trying to decipher the code any longer
for report in reports:
    element2 = report.find_element_by_xpath("//tr[@class='']")
    title = element2.find_element_by_xpath(".//*[@href='/experiences/exp.php?ID=86484']").text

    # element4 = report.find_element_by_css_selector("#results-form > table > tbody > tr:nth-child(3) > td:nth-child(4)")
    element4 = report.find_element_by_css_selector("tr.' '")
    # .//tr[@class='']
    substance_names = element4.text.split('/n') #want the the 4th td child element text
    # substance = element4.text

    hrefs = report.find_element_by_xpath("//a[@href]")
    report_links = hrefs.get_attribute("href")

    print(title, substance_names, hrefs)
    # report_dict = {'title': title, 'substance': substance, 'links': report_links}

    '''
    elements = report.find_elements_by_css_selector(".exp-list-table[href]")
    report_links = [elements.getattribute('href') for element in elements]
    '''
    # report_links = report.find_elements_by_css_selector('a[href*="exp.php?ID"]')
    # report_links = report.find_element_by_xpath("//*[@id='results-form']/table/tbody/tr[3]/td[2]/a")

# get text data
# create dataframe and export to csv
'''
for index, view in enumerate(view_links):
    html = view.get_attribute('innerHTML')
    href = html.split('"')[1]

    view_links[index] = href

for href in view_links:
    browser.get(href)

    text = browser.find_element_by_class_name('report-text-surround').text.encode('utf-8')
    print(text)
'''
