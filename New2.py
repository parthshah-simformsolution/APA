import time
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC


# Open the spreadsheet
workbook = openpyxl.load_workbook(r"C:\Users\parth\Downloads\APAQuestions.xlsx")

# Get the first sheet
sheet = workbook.worksheets[0]

# Create a list to store the values
question = []
failed_question =[]

# Create a new instance of the Chrome web driver
driver = webdriver.Chrome()

# Navigate to the website
driver.get('https://82ce-14-99-102-226.ngrok-free.app/');
#driver.get('https://5cdd-14-99-102-226.ngrok-free.app/')
driver.implicitly_wait("6")
driver.find_element(By.XPATH, '//div[@value="0"]').click()
#driver.find_element(By.XPATH, '//*[text()="Falcon 7B Instruct BF16"]').click()
driver.find_element(By.XPATH, '//*[text()="Llama-2-13b-Chat (On Demand)"]').click()

time.sleep(5)
send_question = driver.find_element(By. CSS_SELECTOR, 'svg.eyeqlp51.css-9ilocf.ex0cdmw0')

# Iterate through rows
for i, row in enumerate(sheet):
    # Skip the first row (the row with the column names)
    if i < 37 :
        continue
    # Get the value of the first cell in the row
    question_text = row[1].value
    # Add the value to the list
    question.append(question_text)


for p in question:


    try:
        search_question = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@data-baseweb="base-input"]/textarea')))
        send_question = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'svg.eyeqlp51.css-9ilocf.ex0cdmw0')))
        search_question.send_keys(p)
        print(p)
        send_question.click()
        time.sleep(30)
    except StaleElementReferenceException:
        search_question = driver.find_element(By.XPATH, '//div[@data-baseweb="base-input"]/textarea')
        print("2nd choice" + p)
        time.sleep(40)
        try:
            search_question.clear()
            search_question.send_keys(p)
            send_question.click()
        except StaleElementReferenceException:
            failed_question.append(search_question)

for q in failed_question:
    search_question = driver.find_element(By.XPATH, '//div[@data-baseweb="base-input"]/textarea')
    search_question.send_keys(q)
    print("failed " + q)
    question.click()



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