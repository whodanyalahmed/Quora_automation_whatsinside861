import pandas as pd

# get data from xlsx file only return column data
def get_data_from_xlsx(file_name, sheet_name, column_name):
    data = pd.read_excel(file_name, sheet_name=sheet_name)
    # data = data[column_name]
    return data[column_name]

questions = get_data_from_xlsx('data.xlsx', 'Question', 'Question')

for question in range(len(questions)):
    print(question)