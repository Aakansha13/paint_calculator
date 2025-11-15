"""
End-to-end tests using Playwright for the paint calculator application.
"""
import pytest
import re
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def app_url():
    """Base URL for the application (renamed to avoid conflict with pytest-base-url)."""
    return "http://localhost:9200"


@pytest.mark.e2e
class TestPaintCalculatorE2E:
    """End-to-end tests for the paint calculator application."""
    
    def test_home_page_loads(self, page: Page, app_url):
        """Test that the home page loads correctly."""
        page.goto(app_url)
        expect(page).to_have_title("Home")
        expect(page.locator("h1")).to_contain_text("Calculating Paint Required")
        expect(page.locator("text=Enter the number of rooms")).to_be_visible()
        expect(page.locator("input[name='rooms']")).to_be_visible()
        expect(page.locator("input[type='submit']")).to_be_visible()
    
    def test_navigation_to_dimensions_page(self, page: Page, app_url):
        """Test navigation from home to dimensions page."""
        page.goto(app_url)
        page.fill("input[name='rooms']", "2")
        page.click("input[type='submit']")
        
        # Should navigate to dimensions page
        expect(page).to_have_url(f"{app_url}/dimensions?rooms=2")
        # Verify table headers within the dimensions table using CSS (robust)
        headers = page.locator("table[name='dimensions_table'] th")
        expect(headers.filter(has_text="Room Number")).to_have_count(1)
        expect(headers.filter(has_text="Length")).to_have_count(1)
        expect(headers.filter(has_text="Width")).to_have_count(1)
        expect(headers.filter(has_text="Height")).to_have_count(1)
        
        # Should have 2 rows for room inputs
        length_inputs = page.locator("input[name^='length-']")
        expect(length_inputs).to_have_count(2)
    
    def test_dimensions_page_with_multiple_rooms(self, page: Page, app_url):
        """Test dimensions page with multiple rooms."""
        page.goto(f"{app_url}/dimensions?rooms=3")
        
        # Should have 3 rows
        length_inputs = page.locator("input[name^='length-']")
        width_inputs = page.locator("input[name^='width-']")
        height_inputs = page.locator("input[name^='height-']")
        
        expect(length_inputs).to_have_count(3)
        expect(width_inputs).to_have_count(3)
        expect(height_inputs).to_have_count(3)
        
        # Room numbers: assert in first column cells (not footer)
        first_col_cells = page.locator("table[name='dimensions_table'] tr td:nth-child(1)")
        expect(first_col_cells.nth(0)).to_have_text("1")
        expect(first_col_cells.nth(1)).to_have_text("2")
        expect(first_col_cells.nth(2)).to_have_text("3")
    
    def test_submit_dimensions_to_results_page(self, page: Page, app_url):
        """Test submitting dimensions and navigating to results page."""
        page.goto(f"{app_url}/dimensions?rooms=2")
        
        # Fill in dimensions for room 1
        page.fill("input[name='length-0']", "10")
        page.fill("input[name='width-0']", "12")
        page.fill("input[name='height-0']", "8")
        
        # Fill in dimensions for room 2
        page.fill("input[name='length-1']", "15")
        page.fill("input[name='width-1']", "10")
        page.fill("input[name='height-1']", "9")
        
        # Submit form
        page.click("input[type='submit']")
        
        # Should navigate to results page
        expect(page).to_have_url(f"{app_url}/results")
        expect(page.locator("button:has-text('View Results')")).to_be_visible()
    
    def test_results_modal_displays_calculations(self, page: Page, app_url):
        """Test that the results modal displays correct calculations."""
        page.goto(f"{app_url}/dimensions?rooms=1")
        
        # Fill in dimensions: 10x12x8 room
        page.fill("input[name='length-0']", "10")
        page.fill("input[name='width-0']", "12")
        page.fill("input[name='height-0']", "8")
        
        page.click("input[type='submit']")
        
        # Wait for results page to load
        expect(page).to_have_url(f"{app_url}/results")
        
        # Click View Results button
        page.click("button:has-text('View Results')")
        
        # Wait for modal to appear and API call to complete (wait for AJAX)
        page.wait_for_timeout(6000)  # Wait for the setTimeout(5000) + API call
        
        # Check modal is visible
        modal = page.locator("#resultsModal")
        expect(modal).to_be_visible()
        
        # Verify table headers within the modal's results table using CSS
        modal_headers = modal.locator(".modal-body table[name='Results'] th")
        expect(modal_headers.filter(has_text="Room #")).to_have_count(1)
        expect(modal_headers.filter(has_text="Amount of Feet to Paint")).to_have_count(1)
        expect(modal_headers.filter(has_text="Gallons Required")).to_have_count(1)
        
        # Verify calculations are displayed
        # Room 1: ((10*2) + (12*2)) * 8 = 352 ft, 1 gallon
        expect(page.locator("#room-1 .room-number")).to_contain_text("1")
        expect(page.locator("#room-1 .room-feet")).to_contain_text("352")
        expect(page.locator("#room-1 .room-total-gallons")).to_contain_text("1")
        
        # Verify total gallons
        expect(page.locator("#sumGallons")).to_contain_text("Total Gallons Required: 1")
    
    def test_multiple_rooms_calculation(self, page: Page, app_url):
        """Test calculation with multiple rooms."""
        page.goto(f"{app_url}/dimensions?rooms=2")
        
        # Room 1: 10x10x10 = 400 ft, 1 gallon
        page.fill("input[name='length-0']", "10")
        page.fill("input[name='width-0']", "10")
        page.fill("input[name='height-0']", "10")
        
        # Room 2: 15x12x9 = 486 ft, 2 gallons
        page.fill("input[name='length-1']", "15")
        page.fill("input[name='width-1']", "12")
        page.fill("input[name='height-1']", "9")
        
        page.click("input[type='submit']")
        expect(page).to_have_url(f"{app_url}/results")
        
        # Open results modal
        page.click("button:has-text('View Results')")
        page.wait_for_timeout(6000)
        
        # Verify both rooms are displayed
        expect(page.locator("#room-1 .room-number")).to_contain_text("1")
        expect(page.locator("#room-1 .room-feet")).to_contain_text("400")
        expect(page.locator("#room-1 .room-total-gallons")).to_contain_text("1")
        
        expect(page.locator("#room-2 .room-number")).to_contain_text("2")
        expect(page.locator("#room-2 .room-feet")).to_contain_text("486")
        expect(page.locator("#room-2 .room-total-gallons")).to_contain_text("2")
        
        # Verify total gallons (1 + 2 = 3)
        expect(page.locator("#sumGallons")).to_contain_text("Total Gallons Required: 3")
    
    def test_negative_rooms_sanitized(self, page: Page, app_url):
        """Test that negative room numbers are sanitized."""
        page.goto(f"{app_url}/dimensions?rooms=-5")
        
        # Should still show 5 rooms (negative sanitized to positive)
        length_inputs = page.locator("input[name^='length-']")
        expect(length_inputs).to_have_count(5)
    
    def test_form_validation_required_fields(self, page: Page, app_url):
        """Test that form fields are required."""
        page.goto(f"{app_url}/dimensions?rooms=1")
        
        # Try to submit without filling fields
        page.click("input[type='submit']")
        
        # Should still be on dimensions page (HTML5 validation prevents submission)
        # Check that inputs are still present
        expect(page.locator("input[name='length-0']")).to_be_visible()
    
    def test_home_button_on_results_page(self, page: Page, app_url):
        """Test that home button navigates back to home."""
        page.goto(f"{app_url}/dimensions?rooms=1")
        page.fill("input[name='length-0']", "10")
        page.fill("input[name='width-0']", "10")
        page.fill("input[name='height-0']", "10")
        page.click("input[type='submit']")
        
        expect(page).to_have_url(f"{app_url}/results")
        
        # Click home button
        page.click("input[type='submit'][value='Home']")
        
        # Should navigate back to home (allow optional trailing '?')
        expect(page).to_have_url(re.compile(rf"^{re.escape(app_url)}/?\??$"))
    
    def test_footer_information_displayed(self, page: Page, app_url):
        """Test that footer information is displayed correctly."""
        page.goto(app_url)
        
        expect(page.locator("text=1 gallon of paint is required for every 400ft of surface")).to_be_visible()
        expect(page.locator("text=((Length * 2) + (Width * 2)) * Height")).to_be_visible()
        expect(page.locator("text=Gallons required will be rounded up")).to_be_visible()
