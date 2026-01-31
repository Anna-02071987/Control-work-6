from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = "https://bonigarcia.dev/selenium-webdriver-java/data-types.html"


def test_form_validation():
    driver = webdriver.Edge()
    wait = WebDriverWait(driver, 20)

    try:
        driver.get(URL)

        def inp(name: str):
            return wait.until(EC.presence_of_element_located(
                (By.NAME, name)))

        def set_value(name: str, value: str):
            el = inp(name)
            el.clear()
            el.send_keys(value)

        set_value("first-name", "Ivan")
        set_value("last-name", "Petrov")
        set_value("address", "Lenina, 55-3")
        set_value("e-mail", "test@skypro.com")
        set_value("phone", "+7985899998787")
        set_value("city", "Moscow")
        set_value("country", "Russia")
        set_value("job-position", "QA")
        set_value("company", "SkyPro")

        wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[type='submit']"))
        ).click()
        wait.until(EC.url_contains("data-types-submitted"))

        def result_alert(field_id: str):
            loc = (By.ID, field_id)
            el = wait.until(EC.presence_of_element_located(loc))
            return el.get_attribute("class") or ""

        assert "alert-danger" in result_alert("zip-code")

        ok_ids = [
            "first-name",
            "last-name",
            "address",
            "e-mail",
            "phone",
            "city",
            "country",
            "job-position",
            "company",
        ]
        for fid in ok_ids:
            assert "alert-success" in result_alert(fid), f"{fid} not green"

    finally:
        driver.quit()
