from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup the WebDriver
driver = webdriver.Chrome()

try:
    # 1. Navigate to the FitPeo Homepage
    driver.get('https://fitpeo.com')
    wait = WebDriverWait(driver, 20)  # Increase the wait time to 20 seconds

    # Print the current URL and title to debug
    print("Current URL:", driver.current_url)
    print("Current page title:", driver.title)

    # 2. Check for iframes
    iframes = driver.find_elements(By.TAG_NAME, 'iframe')
    print(f"Number of iframes on the page: {len(iframes)}")
    for index, iframe in enumerate(iframes):
        print(f"Iframe {index}: {iframe.get_attribute('src')}")

    # If there is an iframe, switch to it (example, if there's one iframe)
    if iframes:
        driver.switch_to.frame(iframes[0])
        print("Switched to the iframe.")

    # 3. Use different locators to find the link
    try:
        revenue_calculator_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Revenue Calculator')))
    except:
        print("Link text 'Revenue Calculator' not found. Trying partial link text.")
        revenue_calculator_link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Revenue')))

    print("Found 'Revenue Calculator' link, clicking...")
    revenue_calculator_link.click()

    # 4. Scroll Down to the Slider section
    slider_section = wait.until(EC.visibility_of_element_located((By.ID, 'slider_section')))
    driver.execute_script("arguments[0].scrollIntoView();", slider_section)

    # 5. Adjust the Slider to 820
    slider = driver.find_element(By.ID, 'slider')
    actions = ActionChains(driver)
    actions.click_and_hold(slider).move_by_offset(820, 0).release().perform()
    time.sleep(1)  # Give time for the slider to move

    # 6. Update the Text Field with 560
    text_field = driver.find_element(By.ID, 'text_field')
    text_field.click()
    text_field.clear()
    text_field.send_keys('560')
    text_field.send_keys(Keys.RETURN)
    time.sleep(1)  # Give time for the slider to update

    # 7. Validate Slider Value
    assert slider.get_attribute('value') == '560', "Slider value did not update correctly"

    # 8. Select CPT Codes
    cpt_codes = ['99091', '99453', '99454', '99474']
    for code in cpt_codes:
        checkbox = driver.find_element(By.ID, f'cpt_{code}')
        if not checkbox.is_selected():
            checkbox.click()

    # 9. Validate Total Recurring Reimbursement
    total_reimbursement = driver.find_element(By.ID, 'total_reimbursement')
    assert total_reimbursement.text == '$110700', "Total Reimbursement value is incorrect"

finally:
    # Close the WebDriver
    driver.quit()