from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from uuid import uuid1

class LoginFormTest(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

        self.driver.implicitly_wait(5)

        self.driver.get('http://127.0.0.1:8000/auth/login/')
        self.driver.maximize_window()


    def test_login_successful(self):
        """
        fill form with correct data and check response

        For this test user with theese credencial is needed:

        # user = Anon203458374
        # password = Anon2020
        """

        test_user_username = "Anon203458374"
        # test_email = "Anon203458374@email.com"
        test_password = "Anon2020"

        username_el = self.driver.find_element(By.ID, 'id_username')
        username_el.send_keys(test_user_username)

        password_el = self.driver.find_element(By.ID, 'id_password')
        password_el.send_keys(test_password)

        login_button_el = self.driver.find_element(By.ID, 'id_button_login')
        login_button_el.click()

        assert self.driver.current_url == 'http://127.0.0.1:8000/'

        alert_login_message = self.driver.find_element(By.ID, 'id_login_successful').text
        
        assert "Witaj Anon203458374" in alert_login_message


    def test_login_unsuccessful(self):
        """
        fill form with incorrect data and check response
        """

        test_user_username = "incorrect_login2137"
        test_password = "incorrect_password2137"

        username_el = self.driver.find_element(By.ID, 'id_username')
        username_el.send_keys(test_user_username)

        password_el = self.driver.find_element(By.ID, 'id_password')
        password_el.send_keys(test_password)

        login_button_el = self.driver.find_element(By.ID, 'id_button_login')
        login_button_el.click()

        assert self.driver.current_url == "http://127.0.0.1:8000/auth/login/"

        alert_login_message = self.driver.find_element(By.ID, 'id_login_alert').text

        assert "Logowanie nieudane. Sprawdź login lub hasło" in alert_login_message

    def tearDown(self):
        self.user_delete = User.objects.filter(username="Anon123").delete()
        self.driver.quit()