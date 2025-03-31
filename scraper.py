from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import uuid
import pymongo
from config import *

class TwitterRobot:
    def __init__(self):
        # Connect to our database
        self.client = pymongo.MongoClient(MONGODB_URI)
        self.db = self.client['twitter_trends']
        self.collection = self.db['trends']
    
    def start_browser(self):
        # Set up our proxy with ProxyMesh credentials
        proxymesh_url = '__'
        proxy_username = '__'
        proxy_password = '__'

        # Form the Proxy URL
        proxy = f'http://{proxy_username}:{proxy_password}@{proxymesh_url}'

        # Set up our browser with proxy settings
        options = webdriver.ChromeOptions()
        options.add_argument(f'--proxy-server={proxy}')
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options), proxymesh_url

    def login_to_twitter(self, driver):
        # Go to Twitter and log in
        driver.get('https://x.com/?lang=en-in')
        wait = WebDriverWait(driver, 20)
        
        # Type username
        username = wait.until(EC.presence_of_element_located((By.NAME, "text")))
        username.send_keys(TWITTER_USERNAME)
        driver.find_element(By.XPATH, "//span[text()='Next']").click()
        
        # Type password
        password = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password.send_keys(TWITTER_PASSWORD)
        driver.find_element(By.XPATH, "//span[text()='Log in']").click()

    def get_trending_topics(self):
        # Start our browser
        driver, ip_address = self.start_browser()
        try:
            # Log in to Twitter
            self.login_to_twitter(driver)
            wait = WebDriverWait(driver, 20)
            
            # Find trending topics
            trends = wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@data-testid='trend']//span[contains(text(),'Trending')]/../../..//span")))
            
            # Get the top 5 trends
            trending_topics = [trend.text for trend in trends[:5]]
            
            # Save what we found
            record = {
                "_id": str(uuid.uuid4()),
                "nameoftrend1": trending_topics[0],
                "nameoftrend2": trending_topics[1],
                "nameoftrend3": trending_topics[2],
                "nameoftrend4": trending_topics[3],
                "nameoftrend5": trending_topics[4],
                "timestamp": datetime.now(),
                "ip_address": ip_address
            }
            
            # Store in our database
            self.collection.insert_one(record)
            return record
            
        finally:
            # Close our browser
            driver.quit()
