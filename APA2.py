import time
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
import datetime
import requests
import pymsteams
from ddt import ddt , data , unpack

#Path to the Excel file
excel_file_path = r"C:\Users\parth\Downloads\Book5.xlsx"

# Open the spreadsheet
workbook = openpyxl.load_workbook(r"C:\Users\parth\Downloads\Book5.xlsx")

# Get the first sheet
sheet = workbook.worksheets[0]

# Get the first sheet
sheet = workbook.worksheets[0]

# Create a list to store the values
question = []
failed_question =[]

# Create a new instance of the Chrome web driver
driver = webdriver.Chrome()

# Navigate to the website
driver.get('https://genaipoc.apa.org/');
driver.implicitly_wait("3")
driver.find_element(By.XPATH, '//div[@value="0"]').click()
driver.find_element(By.XPATH, '//*[text()="Llama-2-13b-Chat (On Demand)"]').click()


time.sleep(5)
send_question = driver.find_element(By. CSS_SELECTOR, 'svg.eyeqlp51.css-9ilocf.ex0cdmw0')

# Iterate through rows
for i, row in enumerate(sheet):
    # Skip the first row (the row with the column names)
    if i == 0 :
        continue
    # Get the value of the first cell in the row
    question_text = row[1].value
    # Add the value to the list
    question.append(question_text)

j: int=2
ans= []

for p in question:
    if p:
        try:
            search_question = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@data-baseweb="base-input"]/textarea')))
            send_question = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'svg.eyeqlp51.css-9ilocf.ex0cdmw0')))
            search_question.send_keys(p)
            print(p)
            send_question.click()
            time.sleep(40)
            xpath_1 = "(//div[@class='stChatMessage css-4oy321 eeusbqq4']//div[@data-testid='stMarkdownContainer']//p)[" + str(j) + "]"
            j=j+1
            try:
                ans_xpath =driver.find_element(By.XPATH, xpath_1)
                if ans_xpath:
                    get_ans =ans_xpath.text
                    ans.append(get_ans)
                else:
                    print("ALERT ERROR HAS OCCURED")


            except Exception as E:

                webhook_url = "https://simformsolutionspvtltd.webhook.office.com/webhookb2/948cab11-d1a3-408c-b1cd-7889c39ec8ae@f4814d23-3835-4d87-a7dc-57a19c04684a/IncomingWebhook/d6705a828d7149bea361d0693bd2f7eb/16405cc0-a836-4bef-8870-8557a16b91d7"

                myTeamsMessage = {

                    "text": "############## AN ERROR HAS OCCURED ##############"

                }

                current_datetime = datetime.datetime.now()

                screenshot_file = f"screenshot_{current_datetime}.png"

                driver.save_screenshot(screenshot_file)

                response = requests.post(webhook_url, data=myTeamsMessage, files=screenshot_file)

                if response.status_code == 200:

                    print("Message with screenshot sent successfully")

                else:

                    print("Failed to send message with screenshot:", response.status_code, response.text)

        except StaleElementReferenceException:
            #search_question = driver.find_element(By.XPATH, '//div[@data-baseweb="base-input"]/textarea')
            #print("2nd choice" + p)
            time.sleep(10)



Error_text = ["error processing your request"]

try:
    for i, answer in enumerate(ans):
        sheet.cell(row=i + 2, column=3, value=answer)
        # Check if any element in Error_text is present in the answer
        if any(error in answer for error in Error_text):
            print("An error has occurred in answer:", answer)

    # Save the modified Excel file
    workbook.save(excel_file_path)
except Exception as e:
    print(f"Error writing answers to Excel: {e}")


