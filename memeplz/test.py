from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color
from uuid import uuid1
import time
import re

class HostTest(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

        self.driver.get('http://127.0.0.1:8000/')
        self.driver.maximize_window()

    def test_home_page(self):
        assert "Śmieszne obrazki" in self.driver.title

    def tearDown(self):
        self.driver.quit()


class LoginFormTest(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

        self.driver.get('http://127.0.0.1:8000/auth/login/')
        self.driver.maximize_window()

    def test_login_successful(self):
        """
        fill form with correct data and check response
        """
        username = self.driver.find_element(By.ID, 'id_username')
        username.send_keys("admin")

        password = self.driver.find_element(By.ID, 'id_password')
        password.send_keys("admin")

        login_button = self.driver.find_element(By.ID, 'id_button_login')
        login_button.click()

        time.sleep(1)

        assert self.driver.current_url == 'http://127.0.0.1:8000/'

        alert_login_message = self.driver.find_element(By.ID, 'id_login_successful').text
        
        assert "Witaj admin" in alert_login_message

    def test_login_unsuccessful(self):
        """
        fill form with incorrect data and check response
        """
        username = self.driver.find_element(By.ID, 'id_username')
        username.send_keys("incorrect_login")

        password = self.driver.find_element(By.ID, 'id_password')
        password.send_keys("incorrect_password")

        login_button = self.driver.find_element(By.ID, 'id_button_login')
        login_button.click()

        time.sleep(1)

        assert self.driver.current_url == "http://127.0.0.1:8000/auth/login/"

        alert_login_message = self.driver.find_element(By.ID, 'id_login_alert').text

        assert "Logowanie nieudane. Sprawdź login lub hasło" in alert_login_message

    def tearDown(self):
        self.driver.quit()

class RegisterFormTest(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

        self.driver.get('http://127.0.0.1:8000/auth/register/')
        self.driver.maximize_window()


    def test_register_successful(self):
        """
        Test registration with correct data
        """
        username = self.driver.find_element(By.ID, 'id_username')
        username.send_keys(f"TestUser{uuid1()}")

        email = self.driver.find_element(By.ID, 'id_email')
        email.send_keys(f"TestEmail{uuid1()}@email.com")

        # the same 2 uuid for passwords
        passwd = f"TestPassword{uuid1()}"

        password = self.driver.find_element(By.ID, 'id_password1')
        password.send_keys(passwd)

        confirm_password = self.driver.find_element(By.ID, 'id_password2')
        confirm_password.send_keys(passwd)

        time.sleep(1)

        register_button = self.driver.find_element(By.ID, 'id_button_register')
        register_button.click()

        time.sleep(1)

        alert_register_successful_message = self.driver.find_element(By.ID, 'id_login_alert').text

        assert self.driver.current_url == "http://127.0.0.1:8000/auth/login/"
        assert alert_register_successful_message == "Rejestracja zakończona pomyślnie. Możesz zalogować się na swoje konto."

    def test_register_unsuccessful(self):
        """
        Test registration with incorrect data
        this one fill a form with incorrect username
        (the username is to short for this example)
        """

        username = self.driver.find_element(By.ID, 'id_username')
        username.send_keys("ab")

        email = self.driver.find_element(By.ID, 'id_email')
        email.send_keys(f"TestEmail{uuid1()}@email.com")

        # the same 2 uuid for passwords
        passwd = f"TestPassword{uuid1()}"

        password = self.driver.find_element(By.ID, 'id_password1')
        password.send_keys(passwd)

        confirm_password = self.driver.find_element(By.ID, 'id_password2')
        confirm_password.send_keys(passwd)

        time.sleep(1)

        register_button = self.driver.find_element(By.ID, 'id_button_register')
        register_button.click()

        time.sleep(1)

        # check redirect to the same page
        assert self.driver.current_url == 'http://127.0.0.1:8000/auth/register/'

        # check color of border with wrong entry
        username = self.driver.find_element(By.ID, 'id_username')
        username_entry_border_color = username.value_of_css_property("border-color")
        rgb = Color.from_string(username_entry_border_color).hex
    
        assert rgb == "#dc3545"


    def tearDown(self):
        self.driver.quit()





