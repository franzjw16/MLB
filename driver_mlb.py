#!/bin/python3.6

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import os
import PIL.Image as Image
from io import BytesIO
from time import sleep
import datetime
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_mlb_model import Base, MLB
import db_query

class MLB_Scrape:

    def __init__(self, start, end, headless=False):
        self.start_date = start
        self.end_date = end
        
        self.engine = create_engine('sqlite:///mlb.db')
        # Bind the engine to the metadata of the Base class so that the
        # declaratives can be accessed through a DBSession instance
        Base.metadata.bind = self.engine
         
        self.DBSession = sessionmaker(bind=self.engine)
        # A DBSession() instance establishes all conversations with the database
        # and represents a "staging zone" for all the objects loaded into the
        # database session object. Any change made against the objects in the
        # session won't be persisted into the database until you call
        # session.commit(). If you're not happy about the changes, you can
        # revert all of them back to the last commit by calling
        # session.rollback()
        self.session = self.DBSession()
        # Proxy
        myProxy2 = ''

        # Chromedriver
        # instantiate a chrome options object so you can set the size and headless preference
        chrome_options = Options()
#        chrome_options.add_argument('--proxy-server=%s' % myProxy2)
        if headless == True:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")

        script_path = 'chromedriver'
        self.driver1 = webdriver.Chrome(script_path, options=chrome_options)

        self.delay = 1 # seconds

        self.df_1 = pd.DataFrame(columns = ['Date', 'HomeTeam', 'AwayTeam', 'HomeTeamRuns', 'AwayTeamRuns'])

    def run(self):
        
        try:
            dates = pd.date_range(start=self.start_date, end=self.end_date, freq='D')
        except ValueError as e:
            self.driver1.quit()
            return False, 'Either date format is incorrect or date is not valid.\n'
        
        print(f'\nScraping MLB website from date "{self.start_date}" to "{self.end_date}".\n')

        for date in dates:
#            while True:
            stale_flag = False
            print(f">>> Navigating to https://www.mlb.com/scores/{str(date)[0:10]}")
            # Navigate to the application home page
            self.driver1.get(f"https://www.mlb.com/scores/{str(date)[0:10]}")

            while True:
                try:
                    WebDriverWait(self.driver1, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME,
                                 'g5-component--mlb-scores__team__info__name--long')))
                    break
                except TimeoutException:
                    print('Timeout exception')
                    try:
                        message = self.driver1.find_element_by_class_name('p-alert__text')
                        print(message.text)
                        if not message.text == '':
                            break
                    except NoSuchElementException:
                        pass
            
#                teams_temp = self.driver1.find_elements_by_class_name('g5-component--mlb-scores__team__info__name--long').text
#                runs_temp = self.driver1.find_elements_by_class_name('g5-component--mlb-scores__linescore__table--summary__cell--runs').text
            while True:
                try:
                    teams_temp = [el.text for el in self.driver1.find_elements_by_class_name("g5-component--mlb-scores__team__info__name--long")]
                    if teams_temp == [] and not message.text == '':
                        break
                    elif teams_temp == []:
                        print('pass')
                        pass
                    else:
                        break
                except StaleElementReferenceException:
                    print('Teams StaleElementReferenceException')
                    self.driver1.refresh()
                    sleep(5)
                    
            while True:
                try:       
                    runs = [el.text for el in self.driver1.find_elements_by_class_name("g5-component--mlb-scores__linescore__table--summary__cell--runs")]
                    if runs == [] and not message.text == '':
                        break
                    elif runs == []:
                        print('pass')
                        pass
                    else:
                        break
                except StaleElementReferenceException:
                    print('Runs StaleElementReferenceException')
                    self.driver1.refresh()
                    sleep(5)
                    
            while True:
                try:       
                    hits = [el.text for el in self.driver1.find_elements_by_class_name("g5-component--mlb-scores__linescore__table--summary__cell--hits")]
                    if hits == [] and not message.text == '':
                        break
                    elif hits == []:
                        print('pass')
                        pass
                    else:
                        break
                except StaleElementReferenceException:
                    print('hits StaleElementReferenceException')
                    self.driver1.refresh()
                    sleep(5)
                    
            while True:
                try:       
                    errors = [el.text for el in self.driver1.find_elements_by_class_name("g5-component--mlb-scores__linescore__table--summary__cell--errors")]
                    if errors == [] and not message.text == '':
                        break
                    elif errors == []:
                        print('pass')
                        pass
                    else:
                        break
                except StaleElementReferenceException:
                    print('errors StaleElementReferenceException')
                    self.driver1.refresh()
                    sleep(5)

            print(f'teams: {len(teams_temp)}')
            print(f'runs: {len(runs)}')
            print(f'hits: {len(hits)}')
            print(f'errors: {len(errors)}')

            teams = []

            for team in teams_temp:
                if not team == '':
                    teams.append(team)

            count = 1
            runs_count = 0
            game_count = 1
            team1 = ''
            
            if stale_flag == False:
                for team in teams:
                    if count % 2 == 0:
                        ht_runs = runs[runs_count]
                        ht_hits = hits[runs_count]
                        ht_errors = errors[runs_count]
                        at_runs = runs[runs_count+1]                            
                        at_hits = hits[runs_count+1]
                        at_errors = errors[runs_count+1]
                        
                        # Insert a MLB object
                        new_person = MLB(date=str(date)[0:10], home_team=team1, away_team=team, 
                                         ht_runs=ht_runs, ht_hits=ht_hits,
                                         ht_errors=ht_errors, at_runs=at_runs,
                                         at_hits=at_hits, at_errors=at_errors)
                        self.session.add(new_person)
                        self.session.commit()
                        runs_count+=2
                        game_count+=1
                    else:
                        team1 = team
                    count+=1
                print('Written to database.\n')
#                    break
        self.driver1.close()
        return True, '\nScraping MLB website completed.'




    

def scrape_menu():
    while True:
        start = input('Start date e.g."YYYY-MM-DD" (type quit to exit): ')
        if start == 'quit' or start == 'Quit':
            break
        end = input('End date e.g."YYYY-MM-DD" (type quit to exit): ')
        if end == 'quit' or end == 'Quit':
            break
        headless = False
        while True:
            headless = input('Display Browser? (Y/N): ')
            if headless == 'Y' or headless == 'y':
                headless = False
                break
            elif headless == 'N' or headless == 'n':
                headless = True
                break

        mlb = MLB_Scrape(start, end, headless)
        result, message = mlb.run()
        if result == True:
            break
    return result, message

def export_menu():
    while True:
        print("{0:4} {1:1}".format('1.', 'Export to CSV/EXCEL'))
        print('{0:4} {1:1}'.format('2.', 'Back'))
        option = input('Option: ')  
        if option == '1':
            result, message = db_query.export_to_csv_excel()
            print(message)
        elif option == '2':
            break
    return result, message
        
def main():
    while True:
        print("{0:4} {1:1}".format('1.', 'Start Scraping'))
        print('{0:4} {1:1}'.format('2.', 'Export Database to File'))
        print('{0:4} {1:1}'.format('3.', 'Exit'))
        option = input('Option: ')
        if option == '1':
            result, message = scrape_menu()
            print(message)
        elif option == '2':
            result, message = export_menu()
            print(message)
        elif option == '3':
            break   

main()