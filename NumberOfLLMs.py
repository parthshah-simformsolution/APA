import openpyxl

# Open the spreadsheet
workbook = openpyxl.load_workbook(r"C:\Users\parth\Downloads\Book3.xlsx")

# Get the first sheet
sheet = workbook.worksheets[0]

LLM_Model = []

column_titles = [cell.value for cell in sheet[1][2:]]
LLM_Model=list(column_titles)
print(LLM_Model)