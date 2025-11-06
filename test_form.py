import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    # Selenium Manager will auto-download the appropriate driver
    options = Options()
    options.add_argument("--headless")  # run without UI
    options.add_argument("--no-sandbox")  # required in many CI environments
    options.add_argument("--disable-dev-shm-usage")  # overcome limited /dev/shm size on Linux

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@allure.epic("Авторизация")
@allure.title("Тест с верными данными")
@allure.description("Авторизация с вводом верных данных")
def test_successful_login(driver):
    with allure.step("Переходим на страницу"):
        driver.get("https://the-internet.herokuapp.com/login")

    with allure.step("Находим элементы"):
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.CSS_SELECTOR, ".fa.fa-2x.fa-sign-in")

    with allure.step("Вводим данные"):
        username_field.send_keys("tomsmith")
        password_field.send_keys("SuperSecretPassword!")

    with allure.step("Нажимаем кнопку 'Login'"):
        login_button.click()

    with allure.step("Проверяем, что появилось сообщение об успешном входе"):
        success_message = driver.find_element(By.CLASS_NAME, "flash.success").text
        assert "You logged into a secure area!" in success_message

@allure.epic("Авторизация")
@allure.title("Тест с неверными данными")
@allure.description("Авторизация с вводом неверных данных")
def test_unsuccessful_login(driver):
    with allure.step("Переходим на страницу"):
        driver.get("https://the-internet.herokuapp.com/login")

    with allure.step("Находим элементы"):
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.CSS_SELECTOR, ".fa.fa-2x.fa-sign-in")

    with allure.step("Вводим неправильные данные"):
        username_field.send_keys("any_user")
        password_field.send_keys("any_password")

    with allure.step("Отправляем форму"):
        login_button.click()

    with allure.step("Проверяем, что появилось сообщение об ошибке"):
        error_message = driver.find_element(By.CLASS_NAME, "flash.error").text
        assert "Your username is invalid!" in error_message