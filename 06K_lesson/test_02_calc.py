from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"


def test_slow_calculator():
    options = Options()
    options.page_load_strategy = "none"

    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(10)

    wait = WebDriverWait(driver, 50)

    try:
        driver.get("about:blank")
        try:
            driver.get(URL)
        except Exception:
            pass
        driver.execute_script(f"window.location.href = '{URL}';")

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#delay")))

        delay = driver.find_element(By.CSS_SELECTOR, "#delay")
        delay.clear()
        delay.send_keys("45")

        def click_btn(text: str):
            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//span[normalize-space()='{text}']")
                )
            ).click()

        click_btn("7")
        click_btn("+")
        click_btn("8")
        click_btn("=")

        wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, ".screen"), "15"
            )
        )
        assert driver.find_element(By.CSS_SELECTOR, ".screen").text == "15"

    finally:
        driver.quit()
