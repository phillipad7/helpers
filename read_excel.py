# pip install openpyxl

'''
Read an excel file from the same directory
Return a list of panda frames, each panda frame is a sheet of this excel file
'''
def read_uat_result(file_name='sample.xlsx'):
    import pandas as pd
    import os

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, file_name)

    xlsx = pd.ExcelFile(file_path)

    return [xlsx.parse(s) for s in xlsx.sheet_names]



if __name__=='__main__':

    sample2_file = read_uat_result('sample2.xlsx')

    num_of_sheets = len(sample2_file)
    print(num_of_sheets)

    sheet1 = sample2_file[0]
    # print(sheet1['Page Number'])
    # print(sheet1.head)
    print(sheet1[:5])

    # for index, row in sheet1.iterrows():
        # print(row)
        # break