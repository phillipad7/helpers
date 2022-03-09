from doctest import OutputChecker
import pandas as pd
import os
from datetime import datetime

qva_root = '\\\qva\qcom'
# excp_list = []
# file_list = []


def export_path_param(excelBook:str, excelSheet:str, excelHeader:str, outBatchFile:str, exceptionFile:str):
    mr_list = read_excel_param(excelBook, excelSheet, excelHeader, exceptionFile)
    write_batch_file(outBatchFile, mr_list)


def read_excel_param(excelBook: str, excelSheet:str, excelHeader:str, exceptionFile:str):
    print('**** Processing Excel File ****')

    excel = pd.read_excel(open(excelBook, 'rb'),sheet_name=excelSheet)  
    file_list = []
    excp_list = []
    for row in excel[excelHeader]:
        isRow, row = clean_row(row)
        if isRow:
            fpath = construct_file_path(row)
            if os.path.isfile(fpath):
                file_list.append(fpath)
            else:
                excp_list.append(fpath)
        else:
            excp_list.append(row)

    with open(exceptionFile, 'w') as ex:
        for i in excp_list:
            ex.write(str(i))
            ex.write('\n')

    return sorted(list(set(file_list)))

def write_batch_file(outBatchFile:str, mr_list:str):
    with open(outBatchFile, 'w') as wf:
        print('**** Writing to File ****')
        for i in mr_list:
            seg1, seg2 = i.split('\\')[-3:-1]
            # wf.write('echo n | xcopy /s /y "' + i + '" "\\\dsrc3\shared\qcomtest\{}\{}"'.format(seg1,seg2))
            wf.write('echo n | xcopy /s /y "' + i + r'" "\\qqtc-oc2\nonprod-nlp02\qcomtest\{}\{}"'.format(seg1,seg2))

            # wf.write('echo n | xcopy /s /y "' + i + '" "'+ r'\\qqtc\nonprod-nlp01\devnlpapp01a\tmp_uat' + '"')
            wf.write('\n')
    
    print('**** DONE Writing ****')

    



# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

def export_path(fileName:str):
    mr_list = read_excel(fileName)
    with open('export_15_file_list.bat', 'w') as wf:
        print('**** Writing to File ****')
        for i in mr_list:
            seg1, seg2 = i.split('\\')[-3:-1]
            wf.write('echo n | xcopy /s /y "' + i + '" "\\\dsrc3\shared\qcomtest\{}\{}"'.format(seg1,seg2))
            # wf.write('echo n | xcopy /s /y "' + i + '" "\\\devqva\DevNLPShare\\temp"' )
            wf.write('\n')
    
    print('**** DONE Writing ****')



def read_excel(fileName: str):
    print('**** Processing Excel File ****')

    excel = pd.read_excel(open(fileName, 'rb'),sheet_name='Sheet1')  
    file_list = []
    excp_list = []
    for row in excel['Filename']:
        isRow, row = clean_row(row)
        if isRow:
            fpath = construct_file_path(row)
            if os.path.isfile(fpath):
                file_list.append(fpath)
            else:
                excp_list.append(fpath)
        else:
            excp_list.append(row)

    with open('exception_files.txt', 'w') as ex:
        for i in excp_list:
            ex.write(str(i))
            ex.write('\n')

    return sorted(list(set(file_list)))


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


def is_good_row(raw:str):
    return False if type(raw) is datetime else True


def clean_row(raw:str):    
    if type(raw) is datetime:
        return False, raw
    rawlst = str(raw).strip().replace('_', '.').replace(' ', '').split('.')
    if len(rawlst) >1:
        rawlst = [i for i in rawlst if i]
        return True, rawlst
    else:
        return False, raw


'''
raw = x.y
'''
def construct_file_path(raw:str):
    claimantID, caseID = raw[0], raw[1]
    fileName = claimantID + '_' + caseID + '_M.pdf'
    raw = claimantID.zfill(6)
    dir1 = raw[:2]
    dir2 = raw[2:4]
    fpath = os.path.join(qva_root, dir1, dir2, fileName)
    return fpath
 


def mark_cxcel(excel:os.path):
    excel = pd.read_excel(open(excel, 'rw'),sheet_name='2021')
    pass












if __name__=='__main__':
    import time
    start_time = time.time()
    # fileName = '181_file_list.xlsx'


    # print('**** START @ {} ****'.format(start_time))
    # export_path(fileName)
    # print('**** DONE @ {} ****'.format(time.time() - start_time))


# ----------------------------------------------------------------------------------------------


    # inputExcelBook = r'C:\Users\pwang\Desktop\New_15_UAT_FOR_5.1_FROM_DESTINY_03022022.xlsx'
    # excelSheet = 'Sheet1'
    # excelHeader = 'Production'
    # outBatchFile = '15_uat_0302.bat' 
    # exceptionFile =  '15_uat_0302_exception'


    inputExcelBook = r'C:\Users\pwang\Downloads\NLP__\nlp_baseline_eval\181_file_list.xlsx'
    excelSheet = 'Sheet1'
    excelHeader = 'Filename'
    outBatchFile = '181_prod_0309.bat'
    exceptionFile = '181_prod_0309_exception'
    

    print('**** START @ {} ****'.format(start_time))
    export_path_param(inputExcelBook, excelSheet, excelHeader, outBatchFile, exceptionFile)
    print('**** DONE @ {} ****'.format(time.time() - start_time))



