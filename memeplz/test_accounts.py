from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color
from django.contrib.auth.models import User
from uuid import uuid1

PATH = "C:\Program Files (x86)\chromedriver.exe"

class HostTest(TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(PATH)
        self.driver.implicitly_wait(5)

        self.driver.get('http://127.0.0.1:8000/')
        self.driver.maximize_window()

    def test_home_page(self):
        assert "Śmieszne obrazki" in self.driver.title

    def tearDown(self):
        self.driver.quit()


class LoginFormTest(TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(PATH)

        self.driver.implicitly_wait(5)

        self.driver.get('http://127.0.0.1:8000/auth/login/')
        self.driver.maximize_window()

        self.user = User.objects.create_user(username="Anon123", password="zaq1@WSX", email="anon123@email.com")


    def test_login_successful(self):
        """
        fill form with correct data and check response
        """
        username = self.driver.find_element(By.ID, 'id_username')
        username.send_keys("Anon123")

        password = self.driver.find_element(By.ID, 'id_password')
        password.send_keys("zaq1@WSX")

        login_button = self.driver.find_element(By.ID, 'id_button_login')
        login_button.click()

        assert self.driver.current_url == 'http://127.0.0.1:8000/'

        alert_login_message = self.driver.find_element(By.ID, 'id_login_successful').text
        
        assert "Witaj Anon123" in alert_login_message


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

        assert self.driver.current_url == "http://127.0.0.1:8000/auth/login/"

        alert_login_message = self.driver.find_element(By.ID, 'id_login_alert').text

        assert "Logowanie nieudane. Sprawdź login lub hasło" in alert_login_message

    def tearDown(self):
        self.user_delete = User.objects.filter(username="Anon123").delete()
        self.driver.quit()


class RegisterFormTest(TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(PATH)
        self.driver.implicitly_wait(5)

        self.driver.get('http://127.0.0.1:8000/auth/register/')
        self.driver.maximize_window()

        # create a user
        self.user = User.objects.create_user(username="Anon123", email="anon123@email.com", password="zaq1@WSX")


    def test_register_successful(self):
        """
        Test registration with correct data
        """

        self.user_username = f"TestUser{uuid1()}"

        username = self.driver.find_element(By.ID, 'id_username')
        username.send_keys(self.user_username)

        email = self.driver.find_element(By.ID, 'id_email')
        email.send_keys(f"TestEmail{uuid1()}@email.com")

        # the same 2 uuid for passwords
        passwd = f"TestPassword{uuid1()}"

        password = self.driver.find_element(By.ID, 'id_password1')
        password.send_keys(passwd)

        confirm_password = self.driver.find_element(By.ID, 'id_password2')
        confirm_password.send_keys(passwd)

        register_button = self.driver.find_element(By.ID, 'id_button_register')
        register_button.click()

        alert_register_successful_message = self.driver.find_element(By.ID, 'id_login_alert').text

        assert self.driver.current_url == "http://127.0.0.1:8000/auth/login/"
        assert alert_register_successful_message == "Rejestracja zakończona pomyślnie. Możesz zalogować się na swoje konto."

    def test_register_unsuccessful_username_to_short(self):
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

        register_button = self.driver.find_element(By.ID, 'id_button_register')
        register_button.click()

        # check redirect to the same page
        assert self.driver.current_url == 'http://127.0.0.1:8000/auth/register/'

        # check text under username input
        username_error_label = self.driver.find_element(By.CSS_SELECTOR, "p[id='error_1_id_username'] strong").text

        assert username_error_label == "Nazwa użytkownika musi mieć conajmniej 5 znaków"

        # check color of border with wrong entry
        username = self.driver.find_element(By.ID, 'id_username')
        username_entry_border_color = username.value_of_css_property("border-color")
        rgb = Color.from_string(username_entry_border_color).hex
    
        assert rgb == "#dc3545"

    def test_register_unsuccessful_email_already_exist(self):
        """
        Test registration is unsuccessful.
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        In this case we provide an user with some email.
        Then try to create a user with email that 
        already exist.
        """

        username_entry = self.driver.find_element(By.ID, "id_username")
        username_entry.send_keys("DummyUser")

        # the same email as above
        email = self.driver.find_element(By.ID, 'id_email')
        email.send_keys(f"anon123@email.com")


        password = self.driver.find_element(By.ID, 'id_password1')
        password.send_keys("zaq1@WSXcde3")

        confirm_password = self.driver.find_element(By.ID, 'id_password2')
        confirm_password.send_keys("zaq1@WSXcde3")

        register_button = self.driver.find_element(By.ID, 'id_button_register')
        register_button.click()

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
        # delete user after every TestCase
        self.dummy_user = User.objects.filter(username="DummyUser")
        for user in self.dummy_user:
            user.delete()
        self.user_delete = User.objects.filter(username="Anon123").delete()
        self.driver.quit()