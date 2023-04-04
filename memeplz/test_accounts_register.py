from unittest import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color
from uuid import uuid1

class HostTest(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)

        self.driver.get('http://127.0.0.1:8000/')
        self.driver.maximize_window()

    def test_home_page(self):
        assert "Śmieszne obrazki" in self.driver.title

    def tearDown(self):
        self.driver.quit()


class RegisterFormTest(TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)

        self.driver.get('http://127.0.0.1:8000/auth/register/')
        self.driver.maximize_window()

        # create a user
        # self.user = User.objects.create_user(username="Anon123", email="anon123@email.com", password="zaq1@WSX")


    def test_register_successful(self):
        """
        Test registration with correct data
        """

        test_user_username = f"TestUser{uuid1()}"
        test_email = f"TestEmail{uuid1()}@email.com"
        test_password = f"TestPassword{uuid1()}"

        username_el = self.driver.find_element(By.ID, 'id_username')
        username_el.send_keys(test_user_username)

        email_el = self.driver.find_element(By.ID, 'id_email')
        email_el.send_keys(test_email)

        password_el = self.driver.find_element(By.ID, 'id_password1')
        password_el.send_keys(test_password)

        confirm_password_el = self.driver.find_element(By.ID, 'id_password2')
        confirm_password_el.send_keys(test_password)

        register_button_el = self.driver.find_element(By.ID, 'id_button_register')
        register_button_el.click()

        alert_register_successful_message = self.driver.find_element(By.ID, 'id_login_alert').text

        assert self.driver.current_url == "http://127.0.0.1:8000/auth/login/"
        assert alert_register_successful_message == "Rejestracja zakończona pomyślnie. Możesz zalogować się na swoje konto."

    def test_register_unsuccessful_username_to_short(self):
        """
        Test registration with incorrect data
        this one fill a form with incorrect username
        (the username is to short for this example)
        """

        test_user_username = f"hds"
        test_email = f"TestEmail{uuid1()}@email.com"
        test_password = f"TestPassword{uuid1()}"


        username_el = self.driver.find_element(By.ID, 'id_username')
        username_el.send_keys(test_user_username)

        email_el = self.driver.find_element(By.ID, 'id_email')
        email_el.send_keys(test_email)

        password_el = self.driver.find_element(By.ID, 'id_password1')
        password_el.send_keys(test_password)

        confirm_password_el = self.driver.find_element(By.ID, 'id_password2')
        confirm_password_el.send_keys(test_password)

        register_button_el = self.driver.find_element(By.ID, 'id_button_register')
        register_button_el.click()

        # check redirect to the same page
        assert self.driver.current_url == 'http://127.0.0.1:8000/auth/register/'

        # check text under username input
        username_error_label_el = self.driver.find_element(By.CSS_SELECTOR, "p[id='error_1_id_username'] strong").text

        assert username_error_label_el == "Nazwa użytkownika musi mieć conajmniej 5 znaków"

        # check color of border with wrong entry
        username_el = self.driver.find_element(By.ID, 'id_username')
        username_entry_border_color = username_el.value_of_css_property("border-color")
        rgb = Color.from_string(username_entry_border_color).hex
    
        assert rgb == "#dc3545"

    def test_register_unsuccessful_email_already_exist(self):
        """
        Test registration is unsuccessful.
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        In this case we provide an user with some email.
        Then try to create a user with email that 
        already exist (like "admin@email.com").
        """

        test_user_username = f"TestUser{uuid1()}"
        test_email = f"admin@email.com"
        test_password = f"TestPassword{uuid1()}"

        username_el = self.driver.find_element(By.ID, "id_username")
        username_el.send_keys(test_user_username)

        # the same email as above
        email_el = self.driver.find_element(By.ID, 'id_email')
        email_el.send_keys(test_email)

        password_el = self.driver.find_element(By.ID, 'id_password1')
        password_el.send_keys(test_password)

        confirm_password_el = self.driver.find_element(By.ID, 'id_password2')
        confirm_password_el.send_keys(test_password)

        register_button_el = self.driver.find_element(By.ID, 'id_button_register')
        register_button_el.click()

        # check redirect to the same page
        assert self.driver.current_url == "http://127.0.0.1:8000/auth/register/"

        # check text under email input
        username_error_label = self.driver.find_element(By.CSS_SELECTOR, "p[id='error_1_id_email'] strong").text

        assert username_error_label == "Użytkownik z tym adresem email już istnieje"

        # check color of border with wrong entry
        username = self.driver.find_element(By.ID, 'id_email')
        username_entry_border_color = username.value_of_css_property("border-color")
        rgb = Color.from_string(username_entry_border_color).hex
    
        assert rgb == "#dc3545"


    def tearDown(self):
        self.driver.quit()


