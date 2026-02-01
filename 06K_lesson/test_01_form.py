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

        # Fill form fields (By.NAME as mentor suggested)
        driver.find_element(By.NAME, "first-name").send_keys("Ivan")
        driver.find_element(By.NAME, "last-name").send_keys("Petrov")
        driver.find_element(By.NAME, "address").send_keys("Lenina, 55-3")
        driver.find_element(By.NAME, "e-mail").send_keys("test@skypro.com")
        driver.find_element(By.NAME, "phone").send_keys("+7985899998787")
        # Zip code left empty
        driver.find_element(By.NAME, "city").send_keys("Moscow")
        driver.find_element(By.NAME, "country").send_keys("Russia")
        driver.find_element(By.NAME, "job-position").send_keys("QA")
        driver.find_element(By.NAME, "company").send_keys("SkyPro")

        # Click Submit button
        submit_button = driver.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        )
        driver.execute_script(
            "arguments[0].scrollIntoView(true);", submit_button
        )
        submit_button.click()

        # Wait for new page
        wait.until(
            EC.url_contains("data-types-submitted.html")
        )

        # Check zip code is red (alert-danger)
        zip_code = driver.find_element(By.ID, "zip-code")
        zip_classes = zip_code.get_attribute("class")
        assert "alert-danger" in zip_classes, (
            f"Zip code not highlighted red. Classes: {zip_classes}"
        )

        # Check other fields are green (alert-success)
        valid_fields = [
            "first-name", "last-name", "address", "e-mail", "phone",
            "city", "country", "job-position", "company"
        ]

        for field_id in valid_fields:
            element = driver.find_element(By.ID, field_id)
            class_attr = element.get_attribute("class")
            assert "alert-success" in class_attr, (
                f"Field {field_id} not highlighted green. "
                f"Classes: {class_attr}"
            )

    finally:
        driver.quit()
