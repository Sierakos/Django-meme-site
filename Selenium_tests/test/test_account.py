import sys
import os

from selenium import webdriver
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

from config.config import HOME_PAGE

import pytest
import time


admin_users = [
    ("admin", "admin")
]

normal_users = [
    ("Anon123456", "zaq1@WSX")
]

incorrect_users = [
    ("WrongLogin", "WrongPassowrd")
]

class TestHost():
    driver = None

    @pytest.fixture()
    def set_up(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.implicitly_wait(5)

        self.driver.get(HOME_PAGE)
        self.driver.maximize_window()

        yield 'setup'

        self.driver.quit()

    def test_home_page(self, set_up):
        assert "Śmieszne obrazki" in self.driver.title

class TestLoginRegister():

    @pytest.fixture
    def set_up(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

        self.driver.implicitly_wait(5)

        self.driver.get(f'{HOME_PAGE}/auth/login/')
        self.driver.maximize_window()

        yield 'setup'

        self.driver.quit()

    @pytest.mark.parametrize("login, password", admin_users)
    def test_login_admin_successful(self, set_up, login: str, password: str):
        """
        fill form with correct data and check response
        """
        username_input = self.driver.find_element(By.ID, 'id_username')
        username_input.send_keys(login)

        password_input = self.driver.find_element(By.ID, 'id_password')
        password_input.send_keys(password)

        login_button = self.driver.find_element(By.ID, 'id_button_login')
        login_button.click()

        assert self.driver.current_url == HOME_PAGE

        # check if in home page exist success message
        assert self.driver.find_element(By.ID, 'id_login_successful')

    @pytest.mark.parametrize("login, password", incorrect_users)
    def test_login_unsuccessful(self, set_up, login: str, password: str):
        """
        fill form with incorrect data and check response
        """
        username_input = self.driver.find_element(By.ID, 'id_username')
        username_input.send_keys(login)

        password_input = self.driver.find_element(By.ID, 'id_password')
        password_input.send_keys(password)

        login_button = self.driver.find_element(By.ID, 'id_button_login')
        login_button.click()

        assert self.driver.current_url == f"{HOME_PAGE}/auth/login/"

        # check if in login page exist error message
        assert self.driver.find_element(By.ID, 'id_login_alert')
