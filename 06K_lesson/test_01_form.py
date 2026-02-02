# Test for form submission with Chrome browser 
# Note: Using Chrome instead of Edge due to driver download issues 
from selenium import webdriver 
from selenium.webdriver.common.by import By 
import time 
 
def test_form(): 
    driver = webdriver.Chrome() 
 
    try: 
        url = "https://bonigarcia.dev/selenium-webdriver-java/data-types.html" 
        driver.get(url) 
        time.sleep(2) 
 
        driver.find_element(By.NAME, "first-name").send_keys("Ivan") 
        driver.find_element(By.NAME, "last-name").send_keys("Petrov") 
        driver.find_element(By.NAME, "address").send_keys("Lenina, 55-3") 
        driver.find_element(By.NAME, "e-mail").send_keys("test@skypro.com") 
        driver.find_element(By.NAME, "phone").send_keys("+7985899998787") 
        driver.find_element(By.NAME, "city").send_keys("Moscow") 
        driver.find_element(By.NAME, "country").send_keys("Russia") 
        driver.find_element(By.NAME, "job-position").send_keys("QA") 
        driver.find_element(By.NAME, "company").send_keys("SkyPro") 
 
        time.sleep(1) 
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']") 
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button) 
        time.sleep(0.5) 
        driver.execute_script("arguments[0].click();", submit_button) 
 
        time.sleep(3) 
 
        zip_code = driver.find_element(By.ID, "zip-code") 
        zip_class = zip_code.get_attribute("class") 
        assert "alert-danger" in zip_class 
 
        fields = ["first-name", "last-name", "address", "e-mail", "phone", "city", "country", "job-position", "company"] 
        for field_id in fields: 
            element = driver.find_element(By.ID, field_id) 
            field_class = element.get_attribute("class") 
            assert "alert-success" in field_class 
 
    finally: 
        driver.quit() 
