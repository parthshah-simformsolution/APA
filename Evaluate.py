import time
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.support.ui import WebDriverWait

# Create a new instance of the Chrome web driver
driver = webdriver.Chrome()

ans =[]

# Navigate to the website
driver.get('https://genaipoc.apa.org/')
driver.implicitly_wait(10)
driver.find_element(By.XPATH, '//div[@value="0"]').click()
Model_Xpath = driver.find_element(By.XPATH, '//*[text()="AI21Labs Jurassic-v2 Mid"]')
Model_Xpath.click()
search_question = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@data-baseweb="base-input"]/textarea')))
send_question = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'svg.eyeqlp51.css-9ilocf.ex0cdmw0')))
search_question.send_keys("memory")
send_question.click()
time.sleep(3)
xpath_1 = "(//div[@class='stChatMessage css-4oy321 eeusbqq4']//div[@data-testid='stMarkdownContainer']//p//parent::div[@class='css-5rimss e1nzilvr5'])[2]"
ans_xpath = driver.find_element(By.XPATH, xpath_1)
if ans_xpath:
   get_ans = ans_xpath.text
ans.append(get_ans)
search_question = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@data-baseweb="base-input"]/textarea')))
send_question = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'svg.eyeqlp51.css-9ilocf.ex0cdmw0')))
search_question.send_keys("weather updates")
send_question.click()
time.sleep(3)
i=0

i= "count(//div[@class='stChatMessage css-4oy321 eeusbqq4']//div[@data-testid='stMarkdownContainer']//p//parent::div[@class='css-5rimss e1nzilvr5'])"
ans_xpath = driver.find_element(By.XPATH, xpath_1)
if ans_xpath:
   get_ans2 = ans_xpath.text
ans.append(get_ans2)
print(ans)
# driver.get('https://genaipoc.apa.org/')
# driver.implicitly_wait(2)
# driver.find_element(By.XPATH,'//*[@class="st-cf st-d3 st-bt st-d4 st-d5"]').click()
# Model_Xpath = driver.find_element(By.XPATH, '//*[text()="Falcon 7B Instruct BF16"]')
# Model_Xpath.click()
#

try:
    while True:
        user_input = input("Press 'q' to quit the browser: ")
        if user_input.lower() == 'q':
            break

except KeyboardInterrupt:
    pass  # Handle keyboard interrupt gracefully

finally:
    # Quit the browser
    driver.quit()
