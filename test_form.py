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

# Тест с верными данными
def test_successful_login(driver):
    # Переходим на страницу
    driver.get("https://the-internet.herokuapp.com/login")

    # Находим элементы
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, ".fa.fa-2x.fa-sign-in")

    # Вводим данные
    username_field.send_keys("tomsmith")
    password_field.send_keys("SuperSecretPassword!")

    # Нажимаем кнопку 'Login'
    login_button.click()

    # Проверяем, что появилось сообщение об успешном входе
    success_message = driver.find_element(By.CLASS_NAME, "flash.success").text
    assert "You logged into a secure area!" in success_message

# Тест с неверными данными
def test_unsuccessful_login(driver):
    # Переходим на страницу
    driver.get("https://the-internet.herokuapp.com/login")

    # Находим элементы
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, ".fa.fa-2x.fa-sign-in")

    # Вводим неправильные данные
    username_field.send_keys("any_user")
    password_field.send_keys("any_password")

    # Отправляем форму
    login_button.click()

    # Проверяем, что появилось сообщение об ошибке
    error_message = driver.find_element(By.CLASS_NAME, "flash.error").text
    assert "Your username is invalid!" in error_message