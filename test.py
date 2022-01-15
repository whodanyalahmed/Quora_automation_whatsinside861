import pandas as pd
# get column data from xls file from sheet spacename
#


def get_data_from_xlsx(file_name, sheet_name, column_name):
    data = pd.read_excel(file_name, sheet_name=sheet_name)
    # data = data[column_name]
    return data[column_name]

spaces = get_data_from_xlsx('data.xlsx', 'spacename', 'Space Name')
for space in spaces:
    print(space)
