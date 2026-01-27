import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestShop:
    @pytest.fixture(scope="function")
    def driver(self):
        """Фикстура для инициализации драйвера Firefox."""
        driver = webdriver.Firefox()
        driver.maximize_window()
        yield driver
        driver.quit()

    def test_shopping_cart(self, driver):
        """Тест покупки товаров в магазине."""
        # Открываем сайт магазина
        driver.get("https://www.saucedemo.com/")

        wait = WebDriverWait(driver, 10)

        # Авторизуемся как standard_user
        username_field = wait.until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )
        username_field.send_keys("standard_user")

        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("secret_sauce")

        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()

        # Добавляем товары в корзину
        items_to_add = [
            "Sauce Labs Backpack",
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Onesie"
        ]

        for item_name in items_to_add:
            # Формируем ID кнопки добавления
            item_id = item_name.lower().replace(" ", "-")
            add_button = wait.until(
                EC.element_to_be_clickable(
                    (By.ID, f"add-to-cart-{item_id}")
                )
            )
            add_button.click()

        # Переходим в корзину
        cart_button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
        )
        cart_button.click()

        # Нажимаем Checkout
        checkout_button = wait.until(
            EC.element_to_be_clickable((By.ID, "checkout"))
        )
        checkout_button.click()

        # Заполняем форму
        first_name_field = wait.until(
            EC.presence_of_element_located((By.ID, "first-name"))
        )
        first_name_field.send_keys("Иван")

        last_name_field = driver.find_element(By.ID, "last-name")
        last_name_field.send_keys("Петров")

        postal_code_field = driver.find_element(By.ID, "postal-code")
        postal_code_field.send_keys("123456")

        # Нажимаем Continue
        continue_button = driver.find_element(By.ID, "continue")
        continue_button.click()

        # Читаем итоговую стоимость
        total_element = wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "summary_total_label")
            )
        )
        total_text = total_element.text

        # Извлекаем сумму из текста
        import re
        total_amount = re.search(r'\$(\d+\.\d+)', total_text).group(0)

        # Проверяем сумму
        assert total_amount == "$58.29", (
            f"Ожидалась сумма $58.29, но получили {total_amount}"
        )


if __name__ == "__main__":
    pytest.main([__file__])
