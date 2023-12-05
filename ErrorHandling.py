import time
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.support.ui import WebDriverWait
import pymsteams
import datetime
import requests


#Path to the Excel file
excel_file_path = r"C:\Users\parth\Downloads\Book3.xlsx"

# Open the spreadsheet
workbook = openpyxl.load_workbook(r"C:\Users\parth\Downloads\Book3.xlsx")

# Get the first sheet
sheet = workbook.worksheets[0]

column_titles = [cell.value for cell in sheet[1][2:]]
LLM_Model=list(column_titles)
print(LLM_Model)

# Create a list to store the values
question = []
failed_question = []

# Iterate through rows
for i, row in enumerate(sheet):
    # Skip the first row (the row with the column names)
    if i == 0:
        continue
    # Get the value of the first cell in the row
    question_text = row[1].value
    # Add the value to the list
    question.append(question_text)


# Create a new instance of the Chrome web driver
driver = webdriver.Chrome()

# Navigate to the website
driver.get('https://genaipoc.apa.org/')
driver.implicitly_wait(2)


def EvaluateModel(Model_Xpath, ans_Starting_column):
    j: int = 2
    ans = []
    for p in question:
        if p:
            try:
                search_question = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@data-baseweb="base-input"]/textarea')))
                send_question = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'svg.eyeqlp51.css-9ilocf.ex0cdmw0')))
                search_question.send_keys(p)
                print(p)
                send_question.click()
                time.sleep(20)
                xpath_1 = "(//div[@class='stChatMessage css-4oy321 eeusbqq4']//div[@data-testid='stMarkdownContainer']//p)[" + str(
                    j) + "]"
                j = j + 1
                try:
                    ans_xpath = driver.find_element(By.XPATH, xpath_1)
                    if ans_xpath:
                        get_ans = ans_xpath.text
                        ans.append(get_ans)
                    else:
                        print("ALERT ERROR HAS OCCURED")

                except Exception as E:
                    webhook_url ="https://simformsolutionspvtltd.webhook.office.com/webhookb2/948cab11-d1a3-408c-b1cd-7889c39ec8ae@f4814d23-3835-4d87-a7dc-57a19c04684a/IncomingWebhook/d6705a828d7149bea361d0693bd2f7eb/16405cc0-a836-4bef-8870-8557a16b91d7"

                    myTeamsMessage={
                    "text" : "############## AN ERROR HAS OCCURED ##############"
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
                search_question = driver.find_element(By.XPATH, '//div[@data-baseweb="base-input"]/textarea')
                print("2nd choice" + p)
                time.sleep(10)

    print(ans)
    Error_text = ["error processing your request"]

    try:

        for i, answer in enumerate(ans):

            sheet.cell(row=i + 2, column=ans_Starting_column, value=answer)
            # Check if any element in Error_text is present in the answer
            if any(error in answer for error in Error_text):
                print("An error has occurred in answer:", answer)

        # Save the modified Excel file
        workbook.save(excel_file_path)


    except Exception as e:
        print(f"Error writing answers to Excel: {e}")


for cases in LLM_Model:

    if cases == 'AzureOpenAIGPT35Turbo':
        driver.find_element(By.XPATH, '//div[@value="0"]').click()
        Model_Xpath = driver.find_element(By.XPATH, '//div[@value="0"]')

    elif cases == 'AzureOpenAIGPT35Turbo16k':
        driver.find_element(By.XPATH, '//div[@value="0"]').click()
        Model_Xpath = driver.find_element(By.XPATH, '//div[@value="1"]')

    elif cases == 'Llama7bChat':
        driver.find_element(By.XPATH, '//div[@value="0"]').click()
        time.sleep(2)
        Model_Xpath = driver.find_element(By.XPATH, '//div[text()="Llama-2-7b-Chat"]')
        driver.implicitly_wait(2)
        ans_Starting_column = 3
        EvaluateModel(Model_Xpath, ans_Starting_column)

    elif cases == 'Falcon7BInstructBF16':
        driver.get('https://genaipoc.apa.org/')
        driver.implicitly_wait(2)
        driver.find_element(By.XPATH, '//div[@value="0"]').click()
        time.sleep(2)
        Model_Xpath = driver.find_element(By.XPATH, '//div[text()="Falcon 7B Instruct BF16"]')
        ans_Starting_column = 4
        EvaluateModel(Model_Xpath,ans_Starting_column)




