from django.forms import NullBooleanField
from .oracle_config import Ora
import datetime
import pandas as pd




def check_user_pass(userid, userpass):
    user = Ora()
    user_d = user.check_user(userid,userpass)
    
    
    if user_d != None:
        for data in user_d:
            user_id = data[0]
            user_name = data[1]
            user_pass = data[2]

            return user_id, user_name ,user_pass

def date_formater(date):
        date = date.split('-')
        date_year = int(date[0])
        date_month = int(date[1])
        date_day = int(date[2])
        date_format = datetime.datetime(date_year, date_month, date_day)
        date = date_format.strftime('%d-%b-%Y')
        return date


def excel_generator(data,column,page_name):
    # add special characters here to avoid errors and breaks
    # Filter Special Characters
    if "/" in page_name:
        page_name = page_name.replace("/","")

    excel_file_path = "web_excel_files/" + page_name + ".xlsx"
    #excel_file_path = page_name + ".xlsx"
    excel_data = pd.DataFrame(data=data, columns=list(column))
    
    #Set destination directory to save excel.
    generate_excel = pd.ExcelWriter(excel_file_path,
                        engine='xlsxwriter',
                        datetime_format='dd-mm-yyyy hh:mm:ss',
                        date_format='dd-mm-yyyy')

    #Write excel to file using pandas to_excel
    if len(page_name) > 31:
        page_name = page_name[0:31]
    excel_data.to_excel(generate_excel, startrow = 0, sheet_name=page_name, index=False)

    #Indicate workbook and worksheet for formatting
    workbook = generate_excel.book
    worksheet = generate_excel.sheets[page_name]

    # Iterate through each column and set the width == the max length in that column. A padding length of 2 is also added.
    for i, col in enumerate(excel_data.columns):

        # find length of column i
        try:
            column_len = excel_data[col].astype(str).str.len().max()
        
        except:
            pass
        
        # Setting the length if the column header is larger
        # than the max column value length
        try:
            column_len = max(column_len, len(col)) + 4
        
        except:
            pass
        

        # set the column length
        worksheet.set_column(i, i, column_len)

    generate_excel.save()
    return excel_file_path

