from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
import time
import psutil



class crims_bot():
    def __init__(self, login, password, counter=0):
        self.login = login
        self.password = password
        self.browser = webdriver.Chrome("C:\projects\selenium\The-crims---selenium-robbery-bot\chromedriver.exe")
        self.browser.get("https://www.thecrims.com/")
        self.action = ActionChains(self.browser)
        self.counter = None
        
        
        
        if self.log_in():
            while True:
                try:
                    self.assassult()
                    self.restore_stamina()
                    self.restore()
                except:
                    raise
        else:
            self.log_in()
            
                

    def log_in(self):
        log = self.browser.find_element_by_xpath('//input[@placeholder="Username"]')
        pas = self.browser.find_element_by_xpath('//input[@name="password"]')
        logged = None
        if log:
            try:
                log.send_keys(f'{self.login}')
            except:
                print("problem with login")
        if pas:
            try:
                pas.send_keys(f'{self.password}')
            except:
                print("problem with password")
        if log.get_attribute("value") == f'{self.login}' and pas.get_attribute("value") == f'{self.password}':
            try:
                click_but = self.browser.find_element_by_xpath('//button[@class="btn btn-large btn-inverse"]') 
                click_but.click()
            except:
                print('problem with loging in')

        check = self.browser.find_element_by_xpath('//div[@id="user-profile-username"]')
        if check:
            if check.text == f'{self.login}':
                print("succesfuly logged in: "+check.text)
                logged = True
                return logged
        else:
            print("not logged in")
            logged = False
            return logged

    def assassult(self):
        
        
        but = WebDriverWait(self.browser, 12).until(EC.visibility_of_element_located((By.XPATH, '//div[@id="menu-sprite-robbery"]')))
        if but:
            but.click()
        
        current_stamina = self.browser.find_element_by_xpath('//div[@class="progressbar-bar"]').value_of_css_property("width")
        self.percent_stamina = round(100*float(current_stamina[:-2])/128)
        
        
        select = WebDriverWait(self.browser, 12).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='content_middle']//div//div[4]//table//tr//td//select[@id='singlerobbery-select-robbery']")))
        if select:
            if self.counter != 1:
                select.click()
                for x in range(12): #/// picks 12th position from list
                    select.send_keys(Keys.ARROW_DOWN)
                select.send_keys(Keys.ENTER)
            
            
            while self.percent_stamina >= 25:
                print(self.percent_stamina)
                self.percent_stamina = self.percent_stamina - 25
                try:
                    WebDriverWait(self.browser, 12).until(EC.element_to_be_clickable((By.XPATH, "//tr//table//tr//button[@id='singlerobbery-rob']"))).click()
                    time.sleep(0.5)
                except:
                    raise
                
            


    def restore_stamina(self):
        club = self.browser.find_element_by_xpath('//div[@id="menu-nightlife"]')
        self.action.move_to_element(club).click().perform()

        
        clubs = WebDriverWait(self.browser, 12).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ul.nightclubs.unstyled > li > table.table.table-condensed button.btn.btn-inverse.btn-small.pull-right")))
        clubs.click()
        time.sleep(1)
        
        
        

    def restore(self):
        current_stamina = self.browser.find_element_by_xpath('//div[@class="progressbar-bar"]').value_of_css_property("width")
        percent_stamina = 100*float(current_stamina[:-2])/128
        stamina_number = []
        try:
            inside_club = WebDriverWait(self.browser, 12).until(EC.presence_of_all_elements_located((By.XPATH,"//table[@class='table table-condensed table-top-spacing']//tbody//tr//td[2]")))
        except:
            raise
        stamina_number.extend([float(elem.text[:-1]) for elem in inside_club]) #// saves each element text as float so it can be compared in next step

        for i in inside_club:
            if float(i.text[:-1]) == max(stamina_number):
                needed_to_100 = 100/max(stamina_number)
                needed_now = percent_stamina/max(stamina_number)
                final_score = needed_to_100 - needed_now
                i.find_element_by_xpath("./following::td/input[@name='quantity']").click()
                i.find_element_by_xpath("./following::td/input[@name='quantity']").send_keys(f'{round(final_score)}')
                i.find_element_by_xpath("./following::td/button[@class='btn btn-inverse btn-small']").click()
                WebDriverWait(self.browser, 12).until(EC.invisibility_of_element_located((By.CLASS_NAME, "overlay"))) #/// waits until covering element is gone
                self.counter = 1


if __name__ == "__main__":
    login = "ledi13"
    password = "maniek12"
    try:
        app = crims_bot(login, password)
    except:
        try:
            for p in psutil.process_iter():
                if "chrome" in p.name():
                    p.kill()
            app = crims_bot(login, password)
        except psutil.NoSuchProcess:
            app = crims_bot(login, password)

