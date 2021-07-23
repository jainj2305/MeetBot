import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys

def read_credentials():
    secrets = 'secrets.json'
    with open(secrets) as f:
        keys = json.loads(f.read())
        return keys

class Meet:
    def __init__(self, loginID, password):
        self.loginID = loginID
        self.password = password
        self.base_url = "https://mail.google.com/"
        self.meet_url = input("Enter Meet URL : ")
        self.opt = Options()
        self.opt.add_argument("--disable-infobars")         #disable imformation bar
        self.opt.add_argument("start-maximized")            #Start browser in full screen
        self.opt.add_argument("--disable-extensions")       #disable all the extensions of browser
        self.opt.add_experimental_option("prefs", { \
        "profile.default_content_setting_values.media_stream_mic": 1,               #Allow sites to use mic
        "profile.default_content_setting_values.media_stream_camera": 1,            #Allow sites to use camera
        "profile.default_content_setting_values.geolocation": 2,                    #Turn off location
        "profile.default_content_setting_values.notifications": 2                   #Turn off notifications
        })

        self.driver = webdriver.Chrome(executable_path="F:\setup\chrome driver\chromedriver\chromedriver.exe", options=self.opt)           #path to your chrome driver, replace with yours
        self.COMMAND_OR_CONTROL = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL                #COMMAND for Mac and CONTROL for windows

    def attendMeet(self):
        self.login_to_Gmail()
        self.openMeet()
        self.joinMeet()
        # self.driver.quit()                    #close browser 

    def openMeet(self):
        self.driver.get(self.meet_url)
        time.sleep(10)
        action1 = ActionChains(self.driver)
        action1.key_down(self.COMMAND_OR_CONTROL).send_keys('d').key_up(self.COMMAND_OR_CONTROL).perform()  #Turn off mic
        action2 = ActionChains(self.driver)
        action2.key_down(self.COMMAND_OR_CONTROL).send_keys('e').key_up(self.COMMAND_OR_CONTROL).perform()  #Turn off camera
        

    def joinMeet(self):
        try:
            self.driver.find_element_by_class_name("Fxmcue").click()    #Join Now
        except NoSuchElementException:
            self.driver.find_element_by_link_text("Ask to join").click()  #Ask to join
        

    def login_to_Gmail(self):
        self.driver.get(self.base_url)
        self.put_credentials()
    
    def put_credentials(self):
        try:
            email_field = self.driver.find_element_by_id("identifierId")
            email_field.send_keys(self.loginID + Keys.ENTER)
            time.sleep(5)
            password_field = self.driver.find_element_by_name("password")
            password_field.send_keys(self.password + Keys.ENTER)
            time.sleep(10)
        except NoSuchElementException:
            print("Exception NoSuchElementException\n Wrong page!!")
            self.driver.quit()
            time.sleep(10)

if __name__ == "__main__":
    credentials = read_credentials()
    bot = Meet(credentials['username'], credentials['password'])            #replace username and password in secrets.json file with yours
    bot.attendMeet()