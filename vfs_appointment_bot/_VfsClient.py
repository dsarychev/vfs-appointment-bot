from asyncio import sleep
from cmath import exp
import email
from re import X
from sqlite3 import converters
import time
import logging
import datetime
from numpy import empty
import pandas as da
from sqlalchemy import null


#from _TwilioClient import _TwilioClient
from _ConfigReader import _ConfigReader

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
class _VfsClient:

 #   def __init__(self):
 #       self._twilio_client = _TwilioClient()
        #self._config_reader = _ConfigReader()

    def _init_web_driver(self):
        firefox_options = Options()

        # open in headless mode to run in background
        firefox_options.headless = True
        # firefox_options.add_argument("start-maximized")
        
        # following options reduce the RAM usage
        firefox_options.add_argument("disable-infobars")
        firefox_options.add_argument("--disable-extensions")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-application-cache")
        firefox_options.add_argument("--disable-gpu")
        firefox_options.add_argument("--disable-dev-shm-usage")
        self._web_driver = webdriver.Firefox(options=firefox_options)
        
        # make sure that the browser is full screen, 
        # else some buttons will not be visible to selenium
        self._web_driver.maximize_window()

    def _login(self, vfs_email, vfs_password):
       
       # _section_header = "VFS"
        _email = vfs_email #self._config_reader.read_prop(_section_header, "vfs_email");
        _password = vfs_password;

        print( _email, ' ', _password )
        
        logging.debug("Logging in with email: {}".format(_email))
        
        # logging in
        time.sleep(10)  
        
        # sleep provides sufficient time for all the elements to get visible
        _email_input = self._web_driver.find_element_by_xpath("//input[@id='mat-input-0']")
        _email_input.send_keys(_email)
        _password_input = self._web_driver.find_element_by_xpath("//input[@id='mat-input-1']")
        _password_input.send_keys(_password)
        _login_button = self._web_driver.find_element_by_xpath("//button/span")
        _login_button.click()
        time.sleep(10)
        
    def _validate_login(self):
        try:
            _new_booking_button = self._web_driver.find_element_by_xpath("//section/div/div[2]/button/span")
            if _new_booking_button == None:
                logging.debug("Unable to login. VFS website is not responding")
                raise Exception("Unable to login. VFS website is not responding")
            else:
                logging.debug("Logged in successfully")
        except:
            logging.debug("Unable to login. VFS website is not responding")
            raise Exception("Unable to login. VFS website is not responding")

    def _get_appointment_date(self, visa_centre, category, sub_category):
        logging.info("Getting appointment date: Visa Centre: {}, Category: {}, Sub-Category: {}".format(visa_centre, category, sub_category)) 
        # select from drop down
        _new_booking_button = self._web_driver.find_element_by_xpath(
            "//section/div/div[2]/button/span"
        )
        _new_booking_button.click()
        time.sleep(5)
        _visa_centre_dropdown = self._web_driver.find_element_by_xpath(
            "//mat-form-field/div/div/div[3]"
        )
        _visa_centre_dropdown.click()
        time.sleep(2)

        try:
            _visa_centre = self._web_driver.find_element_by_xpath(
                "//mat-option[starts-with(@id,'mat-option-')]/span[contains(text(), '{}')]".format(visa_centre)
            )
        except NoSuchElementException:
            raise Exception("Visa centre not found: {}".format(visa_centre))
        
        logging.debug("VFS Centre: " + _visa_centre.text)
        self._web_driver.execute_script("arguments[0].click();", _visa_centre)
        time.sleep(5)
        
        _category_dropdown = self._web_driver.find_element_by_xpath(
            "//div[@id='mat-select-value-3']"
        )
        _category_dropdown.click()
        time.sleep(5)
        
        try:
            _category = self._web_driver.find_element_by_xpath(
                "//mat-option[starts-with(@id,'mat-option-')]/span[contains(text(), '{}')]".format(category)
            )
        except NoSuchElementException:
            raise Exception("Category not found: {}".format(category))
        
        logging.debug("Category: " + _category.text)
        self._web_driver.execute_script("arguments[0].click();", _category)
        time.sleep(5)
        
        _subcategory_dropdown = self._web_driver.find_element_by_xpath(
            "//div[@id='mat-select-value-5']"
        )
     
        self._web_driver.execute_script("arguments[0].click();", _subcategory_dropdown)
        time.sleep(5)
        
        try:
            _subcategory = self._web_driver.find_element_by_xpath(
                "//mat-option[starts-with(@id,'mat-option-')]/span[contains(text(), '{}')]".format(sub_category)
            )
        except NoSuchElementException:
            raise Exception("Sub-category not found: {}".format(sub_category))
        
        self._web_driver.execute_script("arguments[0].click();", _subcategory)
        logging.debug("Sub-Cat: " + _subcategory.text)
        time.sleep(5)

        # read contents of the text box
        return self._web_driver.find_element_by_xpath("//div[4]/div")

    def _receive_appointment(self, visa_centre, category, sub_category, Registration_Number, fname, lname, gender, dob, nationality, passport, pasexp, fnumber, persemail ):
        
        _section_header = "Contact"
        _Registration_Number = Registration_Number
        _First_Name = fname
        _Last_Name = lname
        _Gender = gender
        _Date_of_Birth = dob
        _Current_Nationality = nationality
        _Passport_Number = passport
        _pass_exp_d = pasexp
        _Contact_number = fnumber
        _PersEmail = persemail
        _CountryCode = 7;
        
        try:
            _new_booking_button = self._web_driver.find_element_by_xpath(
             "//*[@id='onetrust-accept-btn-handler'] "
         )
            _new_booking_button.click()
        except NoSuchElementException:
            time.sleep(5)
        available = self._web_driver.find_element_by_xpath("//div[4]/div")
        self._web_driver.save_screenshot('/Users/dsarychev/Botscreens/appdata1.png')
            
        time.sleep(5)
        try:
            _next_button = self._web_driver.find_element_by_xpath(
             "/html/body/app-root/div/app-eligibility-criteria/section/form/mat-card[2]/button"
         )
            _next_button.click()
        except NoSuchElementException:
            time.sleep(5)
        time.sleep(30)    
        self._web_driver.save_screenshot('/Users/dsarychev/Botscreens/appdata2.png')
        _regnumber_input = self._web_driver.find_element_by_xpath("//*[contains(@placeholder, 'FRAXXXAAAAYNNNNNN')]")
        _regnumber_input.send_keys(_Registration_Number)
        self._web_driver.save_screenshot('/Users/dsarychev/Botscreens/appdata3.png')
        
        _fname_input = self._web_driver.find_element_by_xpath("//*[contains(@placeholder, 'Enter your first name')]")
        _fname_input.send_keys(_First_Name)
        self._web_driver.save_screenshot('/Users/dsarychev/Botscreens/appdata4.png')
        _lname_input = self._web_driver.find_element_by_xpath("//*[contains(@placeholder, 'Please enter last name.')]")
        _lname_input.send_keys(_Last_Name)
        self._web_driver.save_screenshot('/Users/dsarychev/Botscreens/appdata5.png')
        
        #_gender_dropdown = self._web_driver.find_element_by_xpath("/html/body/app-root/div/app-applicant-details/section/mat-card[1]/form/app-dynamic-form/div/div/app-dynamic-control[4]/div/div[1]/div/app-dropdown/div/div")
        
        _gender_dropdown = self._web_driver.find_element_by_xpath(
            "/html/body/app-root/div/app-applicant-details/section/mat-card[1]/form/app-dynamic-form/div/div/app-dynamic-control[4]/div/div[1]/div/app-dropdown/div/mat-form-field/div/div[1]/div[3]"
        )
        _gender_dropdown.click()
        time.sleep(5)
        self._web_driver.save_screenshot('/Users/dsarychev/Botscreens/appdata6_1.png')
        
        try:
            _gender = self._web_driver.find_element_by_xpath("//mat-option[starts-with(@id,'mat-option-')]/span[contains(text(), '"+_Gender+"' )]")
           
        except NoSuchElementException:
            raise Exception("Gender not found: {}".format(_Gender))
        self._web_driver.execute_script("arguments[0].click();", _gender)
        time.sleep(5)
        
       
        self._web_driver.execute_script("arguments[0].click();", _gender_dropdown)
        time.sleep(5)
        
        _dob_input = self._web_driver.find_element_by_id("dateOfBirth")
        _dob_input.send_keys(_Date_of_Birth)
        self._web_driver.save_screenshot('/Users/dsarychev/Botscreens/appdata7.png')
           
        _nationality_dropdown = self._web_driver.find_element_by_xpath("/html/body/app-root/div/app-applicant-details/section/mat-card[1]/form/app-dynamic-form/div/div/app-dynamic-control[5]/div/div/div/app-dropdown/div/mat-form-field/div/div[1]/div[3]")
     
        self._web_driver.execute_script("arguments[0].click();", _nationality_dropdown)
        time.sleep(5)
        
        try:
            _nationality= self._web_driver.find_element_by_xpath("//mat-option[starts-with(@id,'mat-option-')]/span[contains(text(), '"+_Current_Nationality+"' )]")
        except NoSuchElementException:
            raise Exception("Nationality not found: {}".format(_Current_Nationality))
        self._web_driver.execute_script("arguments[0].click();", _nationality)
        time.sleep(5)
        self._web_driver.save_screenshot('/Users/dsarychev/Botscreens/nationality.png')
 
        _passport_input = self._web_driver.find_element_by_xpath("//*[contains(@placeholder, 'Enter passport number')]")
        _passport_input.send_keys(_Passport_Number)
        _pass_valid_input = self._web_driver.find_element_by_id("passportExpirtyDate")
        _pass_valid_input.send_keys(_pass_exp_d)
        _ccode_input = self._web_driver.find_element_by_xpath("//*[contains(@placeholder, '44')]")
        _ccode_input.send_keys(_CountryCode)
        _pnumber_input = self._web_driver.find_element_by_xpath("//*[contains(@placeholder, '012345648382')]")
        _pnumber_input.send_keys(_Contact_number)
        _cemail_input = self._web_driver.find_element_by_xpath("//*[contains(@placeholder, 'Enter Email Address')]")
        _cemail_input.send_keys(_PersEmail)
            
        self._web_driver.save_screenshot('/Users/dsarychev/Botscreens/appdatapprefinal.png')
            
        _save_button = self._web_driver.find_element_by_xpath("/html/body/app-root[@class='d-flex flex-column min-vh-100']/div[@class='clearfix main-container']/app-applicant-details[@class='ng-star-inserted']/section[@class='container py-15 py-md-30']/mat-card[@class='mat-card mat-focus-indicator form-card p-0 border-0 shadow-none ng-star-inserted']/app-dynamic-form/div[@class='row ng-star-inserted']/div[@class='col-lg-12']/app-dynamic-control[@class='ng-star-inserted']/div[@class='ng-untouched ng-pristine ng-valid ng-star-inserted']/div[@class='row']/div[@class='col-sm mt-20 ng-star-inserted'][2]/button[@class='mat-focus-indicator mat-stroked-button mat-button-base btn btn-block btn-brand-orange mat-btn-lg']")
        self._web_driver.execute_script("arguments[0].scrollIntoView()", _save_button)

        self._web_driver.save_screenshot('/Users/dsarychev/Botscreens/appdatasave.png')
        time.sleep(5)
        try:    
            self._web_driver.execute_script("arguments[0].click()", _save_button)
        except NoSuchElementException:
            raise Exception("Unable to save pers data")
            
        time.sleep(20)
        self._web_driver.save_screenshot('/Users/dsarychev/Botscreens/yourdetail.png')

        _continue_button = self._web_driver.find_element_by_xpath("/html/body/app-root[@class='d-flex flex-column min-vh-100']/div[@class='clearfix main-container']/app-applicant-details[@class='ng-star-inserted']/section[@class='container py-15 py-md-30']/mat-card[@class='mat-card mat-focus-indicator form-card p-0 border-0 shadow-none ng-star-inserted']/div[@class='row']/div[@class='col-sm mt-20'][2]/button[@class='mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-stroked-button mat-button-base']")
        self._web_driver.execute_script("arguments[0].scrollIntoView()", _continue_button)
        self._web_driver.execute_script("arguments[0].click()", _continue_button)
        time.sleep(20)
        self._web_driver.save_screenshot('/Users/dsarychev/Botscreens/calendarview.png')
       
        #dayforselect = datetime.datetime.strptime(date_available, "dd/mm/yyyy")

        _cdate = self._web_driver.find_elements_by_xpath("//*/td[contains(@class, 'date')]") 
        time.sleep(5)
        for cdate in _cdate:
             
            #self._web_driver.execute_script("arguments[0].click()", cdate);
            cdate.click()

            self._web_driver.save_screenshot('/Users/dsarychev/Botscreens/dateselected.png')
            self._web_driver.execute_script("arguments[0].scrollIntoView()", cdate);
            break
       
        self._web_driver.save_screenshot('/Users/dsarychev/Botscreens/RADIO.png')
        self._web_driver.find_element_by_xpath("//*[@id='STRadio1']").click()
        time.sleep(5)
        self._web_driver.save_screenshot('/Users/dsarychev/Botscreens/readytorecord.png')

        self._web_driver.find_element_by_xpath("/html/body/app-root/div/app-book-appointment/section/mat-card[2]/div/div[2]/button").click()
        
        time.sleep(30)
        self._web_driver.save_screenshot('/Users/dsarychev/Botscreens/passedtoinsuarance.png')
        self._web_driver.find_element_by_xpath("/html/body/app-root[@class='d-flex flex-column min-vh-100']/div[@class='clearfix main-container']/app-travel-medical-insurance[@class='ng-star-inserted']/section[@class='container py-15 py-md-30']/mat-card[@class='mat-card mat-focus-indicator form-card p-0 border-0 shadow-none']/div[@class='row']/div[@class='col-12 col-sm-6 mt-20'][2]/button[@class='mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-stroked-button mat-button-base ng-star-inserted']").click()
        
        time.sleep(5)
        self._web_driver.save_screenshot('/Users/dsarychev/Botscreens/insuaranceskip.png')

        
       # self._web_driver.find_element_by_xpath("/html[@class='cdk-global-scrollblock']/body/div[@class='cdk-overlay-container']/div[@class='cdk-global-overlay-wrapper']/div[@id='cdk-overlay-3']/mat-dialog-container[@id='mat-dialog-0']/div[@class='mat-modal-delete-document ng-star-inserted']/div[@class='row']/div[@class='col-12 col-sm-6 col-sm'][2]/button[@class='mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mb-10 mb-sm-0 mat-stroked-button mat-button-base'").click()
        self._web_driver.implicitly_wait(10)

        _buttons = self._web_driver.find_elements_by_xpath("//*/div/div[2]/div[2]/button")
        _buttons[1].click()
        #self._web_driver.implicitly_wait(30)
        self._web_driver.save_screenshot('/Users/dsarychev/Botscreens/insuaranceskip_2.png')
        #WebDriverWait(self._web_driver, 10).until(EC.presence_of_element_located(By.XPATH, "//*[2]/button[@class='mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mb-10 mb-sm-0 mat-stroked-button mat-button-base']"))
        time.sleep(30)
        self._web_driver.save_screenshot('/Users/dsarychev/Botscreens/insuaranceskip_3.png')
        
        self._web_driver.find_element_by_xpath("//*/span[contains(text(), 'I accept the')]").click()
        time.sleep(5)
        self._web_driver.find_element_by_xpath("//*/span[contains(text(), ' Confirm ')]").click()
                                                
        time.sleep(30)
        self._web_driver.execute_script("arguments[0].scrollIntoView()", self._web_driver.find_element_by_xpath("/html/body/app-root/div/app-payment-confirmation/section/mat-card[2]/h2[3]"))
        self._web_driver.save_screenshot('/Users/dsarychev/Botscreens/applicationregistered_'+time.strftime("%x") +'.png')

            
        # read contents of the text box
      #  return self._web_driver.find_element_by_xpath("//div[4]/div")

    def check_slot(self, visa_centre, category, sub_category):
        
        df = da.read_excel('/Users/dsarychev/vsf.xlsx',keep_default_na=False, converters={'regnum':str, 'fname':str, 'lname':str, 'gender':str, 'dob':str, 'nat':str, 'pasp':str, 'pep':str, 'cnumb':str, 'pem':str, 'acc':str, 'pwd':str }) 
        for rows in df.itertuples():
            if rows[2]!=rows[2]:
                break
            else :
               
                vfs_email = rows[11]
                vfs_password = rows[12]
                FranceVisas_Registration_Number = rows[1]
                First_Name = rows[2]
                Last_Name = rows[3]
                Gender = rows[4]
                Date_of_Birth = rows[5]
                Current_Nationality = rows[6]
                Passport_Number = rows[7]
                PassExpDate = rows[8]
                Contact_number = rows[9]
                persemail = rows[10]

                print(visa_centre, category, sub_category,  FranceVisas_Registration_Number, First_Name, Last_Name, Gender, Date_of_Birth, Current_Nationality, Passport_Number, PassExpDate, Contact_number, persemail)

                self._init_web_driver()

    #     # open the webpage
                self._web_driver.get("https://visa.vfsglobal.com/rus/en/fra/login")

                self._login(vfs_email, vfs_password)
                self._validate_login()

                _message = self._get_appointment_date(visa_centre, category, sub_category)
                logging.debug("Message: " + _message.text)

                if len(_message.text) != 0 and _message.text != "No appointment slots are currently available" and _message.text != "Currently No slots are available for selected category, please confirm waitlist\nTerms and Conditions":
                 logging.info("Appointment slots available: {}".format(_message.text))
        
                 _message2 = self._receive_appointment(visa_centre, category, sub_category,  FranceVisas_Registration_Number, First_Name, Last_Name, Gender, Date_of_Birth, Current_Nationality, Passport_Number, PassExpDate, Contact_number, persemail)
                else:
                 logging.info("No slots available")
        # Close the browser
            self._web_driver.close()
            self._web_driver.quit()
