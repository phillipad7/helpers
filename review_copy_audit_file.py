import pandas as pd
import os
from datetime import datetime

qva_root = '\\\qva\qcom'
excp_list = []
# file_list = []


def export_path(fileName:str):
    mr_list = read_excel(fileName)
    with open('export_list.bat', 'w') as wf:
        print('**** Writing to File ****')
        # mr_list = read_excel(fileName)
        for i in mr_list:
            # wf.write('echo n | xcopy /s/y  "')
            # wf.write(str(i))
            # wf.write(' "   "\\\devqva\DevNLPShare\\tmp_for_cl"')
            # wf.write('\n')
            wf.write('echo n | xcopy /s /y "' + i + '" "\\\devqva\DevNLPShare\\tmp_for_cl"' )
            wf.write('\n')
    
    print('**** DONE Writing ****')



def read_excel(fileName: str):
    print('**** Processing Excel File ****')

    excel = pd.read_excel(open(fileName, 'rb'),sheet_name='2021')  
    file_list = []
    excp_list = []

    for row in excel['col_a']:
        isRow, row = clean_row(row)
        if isRow:
            fpath = construct_file_path(row)
            # print('--------')# print(fpath)# print('------\n')
            if os.path.isfile(fpath):
                file_list.append(fpath)
            else:
                excp_list.append(fpath)
        else:
            excp_list.append(row)
    print('\n\n\n\nlen file_list', len(file_list))
    for i in excp_list:
        print(i)
    # print(excp_list)
    with open('exception_files.txt', 'w') as ex:
        for i in excp_list:
            ex.write(str(i))
            ex.write('\n')

    return file_list




def is_good_row(raw:str):
    return False if type(raw) is datetime else True




def clean_row(raw:str):

    # RETURN Flase if row is datetime or row missed caseID
    # rawlst = str(raw).replace('_', '.').replace(' ', '').split('.')
    # if type(raw) is datetime or len(rawlst)<=1:
    #     return False, raw
    # else:
    #     return True, rawlst
    
    if type(raw) is datetime:
        return False, raw
    rawlst = str(raw).replace('_', '.').replace(' ', '').split('.')
    if len(rawlst) >1:
        return True, rawlst
    else:
        return False, raw

    # raw.replace('_', '.').replace(' ', '').split('.')
    

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
    
    # if len(raw)>1:
    #     claimantID, caseID = raw[0], raw[1]
    #     fileName = claimantID + '_' + caseID + '_M.pdf'
    #     raw = claimantID.zfill(6)
    #     dir1 = raw[:2]
    #     dir2 = raw[2:4]
    #     fpath = os.path.join(qva_root, dir1, dir2, fileName)
    #     # print('****************')
    #     # print(dir1, dir2, fileName)
    #     # print('^^^^^^^^^^')
    #     return fpath

    # else:
    #     excp_list.append(str(raw))
 
    




if __name__=='__main__':
    import time
    start_time = time.time()
    fileName = 'MR_2021_Audits.xlsx'

    print('**** START @ {} ****'.format(start_time))
    export_path(fileName)
    print('**** DONE @ {} ****'.format(time.time() - start_time))



