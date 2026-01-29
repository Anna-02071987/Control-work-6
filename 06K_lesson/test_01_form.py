import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestForm:
    @pytest.fixture(scope="function")
    def driver(self):
        """Фикстура для инициализации драйвера Edge."""
        driver = webdriver.Edge()
        driver.maximize_window()
        yield driver
        driver.quit()

    def test_form_submission(self, driver):
        """Тест заполнения формы и проверки подсветки полей."""
        # Открываем страницу
        driver.get(
            "https://bonigarcia.dev/selenium-webdriver-java/data-types.html"
        )

        wait = WebDriverWait(driver, 10)

        # Заполняем форму
        test_data = {
            "first-name": "Иван",
            "last-name": "Петров",
            "address": "Ленина, 55-3",
            "e-mail": "test@skypro.com",
            "phone": "+7985899998787",
            # "zip-code": "",  # Оставляем пустым специально
            "city": "Москва",
            "country": "Россия",
            "job-position": "QA",
            "company": "SkyPro"
        }

        # Заполняем все поля по ID (на сайте есть ID)
        for field_id, value in test_data.items():
            field = wait.until(
                EC.presence_of_element_located((By.ID, field_id))
            )
            field.clear()
            field.send_keys(value)

        # Нажимаем кнопку Submit
        submit_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[text()='Submit']")
            )
        )
        submit_button.click()

        # Ждем когда применится подсветка
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".is-invalid, .is-valid")
            )
        )

        # Проверяем, что поле Zip code подсвечено красным
        zip_code_field = driver.find_element(By.ID, "zip-code")
        zip_code_class = zip_code_field.get_attribute("class")
        assert "is-invalid" in zip_code_class, (
            f"Поле Zip code должно быть красным. Класс: {zip_code_class}"
        )

        # Список полей, которые должны быть зелеными
        green_fields = [
            "first-name",
            "last-name",
            "address",
            "e-mail",
            "phone",
            "city",
            "country",
            "job-position",
            "company"
        ]

        # Проверяем, что остальные поля подсвечены зеленым
        for field_id in green_fields:
            field = driver.find_element(By.ID, field_id)
            field_class = field.get_attribute("class")
            assert "is-valid" in field_class, (
                f"Поле {field_id} должно быть зеленым. Класс: {field_class}"
            )


if __name__ == "__main__":
    pytest.main([__file__])
