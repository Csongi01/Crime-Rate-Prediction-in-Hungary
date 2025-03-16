import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from app import app

# -------------------------
# Unit Tests (Backend Tests)
# -------------------------
class TestCrimePrediction(unittest.TestCase):

    # Setup pytest fixture for client if using pytest
    @classmethod
    def setUpClass(cls):
        with app.test_client() as client:
            cls.client = client

    def test_city_search_valid(self):
        """Test: Valid city search for autocomplete."""
        response = self.client.get('/autocomplete-cities?query=de')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Debrecen", response.json)

    def test_city_search_invalid(self):
        """Test: Invalid city search should return empty list."""
        response = self.client.get('/autocomplete-cities?query=xyz')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_crimes_for_a_given_city(self):
        """Test: Fetch crime types for a specific city."""
        # Predefined list of crimes, with exact matching crime names
        predefined_crimes = [
            "Orgazdaság", "Garázdaság", "A közlekedés biztonsága elleni bűncselekmény",
            "Kiskorú veszélyeztetése", "Közokirat-hamisítás", "Okirattal visszaélés", ]
    
        # Fetch the crime types for the city 'Veresegyház'
        response = self.client.get('/crimes?city=Veresegyház')
    
    
        self.assertEqual(response.status_code, 200)    
    
        crime_types = [crime['Crime'] for crime in response.json]
    
   
        for crime in predefined_crimes:
       
            self.assertIn(crime, crime_types, f"'{crime}' not found in crime types for Veresegyház")


    def test_all_fields_missing(self):
        """Test: All form fields are missing."""
        response = self.client.post('/predict', data={
            'city': '',
            'crime': '',
            'year': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter a year!', response.data)
        self.assertIn(b'Please enter a city!', response.data)
        self.assertIn(b'Please select a crime type!', response.data)


# -------------------------
# Selenium Tests (Frontend Tests)
# -------------------------
class TestCrimePredictionPage(unittest.TestCase):

    def setUp(self):
        """Setup Chrome WebDriver."""
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get("http://localhost:5000/")  # Home page URL

    def test_fill_form_and_submit(self):
        """Test: Fill out the form on the home page and submit it to access the prediction page."""
        city_input = self.driver.find_element(By.ID, "city-input")
        city_input.send_keys("Veresegyház")  # Enter a valid city name

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//ul[@class='suggestions-list']/li"))
        )
        time.sleep(1)
        first_suggestion = self.driver.find_element(By.XPATH, "//ul[@class='suggestions-list']/li[1]")
        first_suggestion.click()  # Click the first suggestion
        time.sleep(1)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "crime-dropdown"))
        )
        crime_dropdown = self.driver.find_element(By.ID, "crime-dropdown")
        crime_dropdown.click()
        crime_dropdown.find_element(By.XPATH, "//option[text()='Lopás']").click()

        year_dropdown = self.driver.find_element(By.ID, "year-dropdown")
        year_dropdown.click()
        year_dropdown.find_element(By.XPATH, "//option[text()='2035']").click()

        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/predict")
        )
        self.assertIn("/predict", self.driver.current_url)   

    def test_verify_chart_on_prediction_page(self):
        """Test: Verify that the chart is rendered on the prediction page."""
        self.test_fill_form_and_submit()  # Ensure the form is filled and submitted

        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/predict")
        )

        chart_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "crimeRateChart"))
        )
        self.assertTrue(chart_element.is_displayed(), "Chart is not displayed on the prediction page.")

    def test_verify_map_on_prediction_page(self):
        """Test: Verify that the map is rendered on the prediction page."""
        self.test_fill_form_and_submit()  # Ensure the form is filled and submitted

        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/predict")
        )       

        map_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "map"))
        )
        self.assertTrue(map_element.is_displayed(), "Map is not displayed on the prediction page.")
  

    def tearDown(self):
        """Close the browser after each test."""
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
