import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestCalculator:
    @pytest.fixture(scope="function")
    def driver(self):
        """Фикстура для инициализации драйвера Chrome."""
        driver = webdriver.Chrome()
        driver.maximize_window()
        yield driver
        driver.quit()

    def test_slow_calculator(self, driver):
        """Тест медленного калькулятора."""
        # Открываем страницу
        url = "https://bonigarcia.dev/selenium-webdriver-java/" \
              "slow-calculator.html"
        driver.get(url)

        wait = WebDriverWait(driver, 50)  # 45 секунд + запас

        # Вводим задержку 45
        delay_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#delay"))
        )
        delay_input.clear()
        delay_input.send_keys("45")

        # Нажимаем кнопки: 7 + 8 =
        buttons = ["7", "+", "8", "="]
        for button in buttons:
            btn = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//span[text()='{button}']")
                )
            )
            btn.click()

        # Ожидаем результат 15 через 45 секунд
        wait.until(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, "screen"), "15"
            )
        )

        # Проверяем результат
        screen = driver.find_element(By.CLASS_NAME, "screen")
        assert screen.text == "15", (
            f"Ожидался результат 15, но получили {screen.text}"
        )


if __name__ == "__main__":
    pytest.main([__file__])
