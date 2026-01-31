"""Test for form submission with Chrome browser.
Note: Using Chrome instead of Edge due to driver download issues."""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_form():
    """Test form submission with validation checks."""
    driver = webdriver.Chrome()

    try:
        url = "https://bonigarcia.dev/selenium-webdriver-java/data-types.html"
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        # Заполняем форму (кириллицей как в задании)
        driver.find_element(By.NAME, "first-name").send_keys("Иван")
        driver.find_element(By.NAME, "last-name").send_keys("Петров")
        driver.find_element(By.NAME, "address").send_keys("Ленина, 55-3")
        driver.find_element(By.NAME, "e-mail").send_keys("test@skypro.com")
        driver.find_element(By.NAME, "phone").send_keys("+7985899998787")
        # Zip code оставляем пустым
        driver.find_element(By.NAME, "city").send_keys("Москва")
        driver.find_element(By.NAME, "country").send_keys("Россия")
        driver.find_element(By.NAME, "job-position").send_keys("QA")
        driver.find_element(By.NAME, "company").send_keys("SkyPro")

        # Нажимаем кнопку Submit
        submit_button = driver.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        )
        # Скроллим к кнопке, чтобы она была видимой
        driver.execute_script(
            "arguments[0].scrollIntoView(true);", submit_button
        )
        submit_button.click()

        # Ждем загрузки новой страницы
        wait.until(
            EC.url_contains("data-types-submitted.html")
        )

        # Проверяем поле Zip code (должно быть красным - alert-danger)
        zip_code_element = driver.find_element(By.ID, "zip-code")
        zip_classes = zip_code_element.get_attribute("class")
        assert "alert-danger" in zip_classes, (
            f"Zip code не подсвечен красным. Классы: {zip_classes}"
        )

        # Проверяем остальные поля (должны быть зелеными - alert-success)
        fields_to_check = [
            "first-name", "last-name", "address", "e-mail", "phone",
            "city", "country", "job-position", "company"
        ]

        for field_id in fields_to_check:
            element = driver.find_element(By.ID, field_id)
            class_attr = element.get_attribute("class")
            assert "alert-success" in class_attr, (
                f"Поле {field_id} не подсвечено зеленым. Классы: {class_attr}"
            )

    finally:
        driver.quit()
