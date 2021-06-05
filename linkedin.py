# This script will help you to remove connection invites older than a month.

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

# Enter your Username and Password by changing the following strings using a Text Editor
USERNAME = 'username'
PASSWORD = 'password'

# Add your criteria below as shown just below the invitation cards on LinkedIn
criteria = '1 week ago'

SCROLL_PAUSE_TIME = 2.0

options = Options()

# If you want to see the process being automated, uncomment the line below
# options.add_argument('--headless')

# Add the PATH of your Chromium Browser
options.binary_location = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'

# Add the PATH to your ChromeDriver 
driver = webdriver.Chrome(chrome_options=options, executable_path='C:\\Tools\\ChromeDriver\\chromedriver.exe')

# Logging in and going to sent invitations page
driver.maximize_window()
driver.get("https://www.linkedin.com")
driver.find_element_by_xpath('//*[@id="session_key"]').send_keys(USERNAME)
driver.find_element_by_xpath('//*[@id="session_password"]').send_keys(PASSWORD)
driver.find_element_by_xpath('//*[@id="main-content"]/section[1]/div[2]/form/button').click()
driver.get('https://www.linkedin.com/mynetwork/invitation-manager/sent/')

withdraw_count = 0

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    time.sleep(SCROLL_PAUSE_TIME)
    
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    if new_height == last_height: break
    
    last_height = new_height
    

invitations = driver.find_elements_by_class_name('invitation-card')

for invite in invitations:
    time_ago = invite.find_element_by_tag_name('time').text
    
    if time_ago == criteria:
        withdraw = invite.find_element_by_tag_name('button')

        action = ActionChains(driver)
        
        action.move_to_element(withdraw).click().perform()

        driver.find_element_by_class_name('artdeco-button--primary').click()

        time.sleep(SCROLL_PAUSE_TIME)

        withdraw_count += 1


driver.close()

print('................FINISHING UP................')
print('Total Invites:', len(invitations))
print('Your Criteria: ', criteria)
print('Withdrawn Invites: ', withdraw_count)
