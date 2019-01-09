# Scrape Google Trends results for presidential hopefuls
# Gabriel Perez-Putnam 1/8/19 - some code adapted from IM

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import time


def sleep_time(x):
    """Sleep for X seconds times a number between 0 and 1"""
    random_time = random.random() * x
    time.sleep(random_time)

def search_term(driver,name):
    """Pull up the google trends page and search a name"""
    driver.get(gtrends)
    # find search box (id = input-254)
    searchbox = driver.find_element_by_id("input-254")
    searchbox.send_keys(name)
    searchbox.send_keys(Keys.RETURN)
    time.sleep(1)

def get_states(driver):
    """Pull the items containing states from the page"""
    states = driver.find_elements_by_class_name("progress-label")
    return states

def get_text(objects,name):
    """Get text from first 5 objects (states)"""
    info = [name]
    for x in objects[:5]:
        line = split_row(x)
        for l in line:
            info.append(l)
    print(info)
    return info

def split_row(info):
    """Take the raw info and pull out state and index"""
    statex = info.get_attribute('innerText').strip()
    list1 = statex.split("\n")
    number = ""
    for c in list(list1[1]):
        if c.isdigit() == True:
            number += c
    state_clean = list1[1].replace(number,"").strip()
    return [state_clean,number]

def clean_row_for_export(variables):
    """Prepares a row of data for export"""
    row = ('\t').join(variables) + '\n'
    return row

def export_to_file(file_name, candidate_list):
    """Export the information to a file"""
    with open(file_name, 'w+', encoding='utf-8') as f:
        header = ['Candidate', 'State1', 'Index1', 'State2', 'Index2','State3',
                  'Index3','State4', 'Index4','State5', 'Index5']
        export_header = clean_row_for_export(header)
        f.write(export_header)
        for candidate in candidate_list:
            row = clean_row_for_export(candidate)
            f.write(row)

def iterate_candidates(candidates, driver):
    """Go through the list and return the google trend info"""
    results = []
    for person in candidates:
        sleep_time(7)
        search_term(driver,person)
        states = get_states(driver)
        results.append(get_text(states, person))
    return results

def main():
    """controller"""
    # create a new Chrome session
    driver = webdriver.Chrome(executable_path='C:/Users/perez_g/Desktop/Web Scrapping/env/Scripts/chromedriver.exe')
    driver.maximize_window()
    driver.implicitly_wait(30)

    # URL of initial search
    global gtrends
    gtrends = "https://trends.google.com/trends/?geo=US"

    candidates = ["Amy Klobuchar", "Joe Biden", "Elizabeth Warren",
                  "cory booker", "Bernie Sanders", "beto orourke",
                  "sherrod brown", "kamala harris", "julian castro",
                  "Kirsten Gillibrand"]

    candidates_info = iterate_candidates(candidates, driver)
    export_to_file('candidate_trends.txt', candidates_info)

main()
