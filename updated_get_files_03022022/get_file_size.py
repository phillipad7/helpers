'''
Script to get file sizes with given file list (imported from excel sheet)
Input: an excelsheet with tab and column names
Output: an excelsheet contains filename and fize size pairs
'''

import os
import pandas as pd
import datetime
datetime.datetime.strptime

qva_root =r'\\qva\qcom'


'''
for given raw file name in excel cell
remove extra whitespaces
split filename into parts (claimantID,caseID,fileType, fileExtensions)
'''
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
Input: root source file path, raw filename parts
Output: Complete [ABS] source file path
'''
def construct_file_path(qva_root, raw):
    claimantID, caseID = raw[0], raw[1]
    fileName = claimantID + '_' + caseID + '_M.pdf'
    raw = claimantID.zfill(6)
    dir1 = raw[:2]
    dir2 = raw[2:4]
    fpath = os.path.join(qva_root, dir1, dir2, fileName)
    return fpath


'''
get file list from given excelbook/sheet/colomn
'''
def get_file_list(excelBook:os.path, excelSheet:str, excelHeader:str ):

    excel = pd.read_excel(excelBook, sheet_name=excelSheet) 
    # print(excel.head())
    # len(excel['filename'].unique())
    # fl = [i for i in excel[excelHeader]]
    # print(len(fl))
    # return fl
    return [i for i in excel[excelHeader]]


'''
for each file in the given file list
check and get file size
Output: list of tuple of filename and filesize
'''
def get_file_size_list(filelist:list):
    fsizelist = []
    for i in filelist:
        isRow, row = clean_row(i)
        if isRow:
            f = construct_file_path(qva_root, row)
            # fn = f.split('\\')[-1]
            size = os.stat(f).st_size if os.path.isfile(f) else 0
            # fz.append((f.split('\\')[-1], os.stat(f).st_size))
            if size > 1024*1024*1024:
                hsize = '{} GB'.format(round(size/(1024*1024*1024), 2))
            elif size > 1024*1024:
                hsize = '{} MB'.format( int(round(size/(1024*1024),0)) )
            elif size > 1024:
                hsize = '{} KB'.format(int(round(size/1024,0)))
            else:
                hsize = '{} Byte'.format(size)
            fsizelist.append((f.split('\\')[-1], hsize, size))

    return fsizelist
    # pass


def writeFileSizeListToFile(excelbook:os.path, excelsheet:str, excelHeader:str):
    fileList = get_file_list(excelbook, excelsheet, excelHeader)
    print('len fileList',len(fileList))

    fSizeList = get_file_size_list(fileList)
    print('len fileSizeList', len(fSizeList))

    for tp in fSizeList:
        print(tp)


    df = pd.DataFrame(fSizeList, columns = ['filename','hsize','rsize'])
    print(df.head)
    
    print('**** {:24s} ****'.format('Writing to File'))
    df.to_csv('sqa_2k_outcomplete_file_with_Hsize.csv', index=False)
    print('**** {:24s} ****'.format('DONE Writing'))





if __name__=='__main__':
    # import time
    # start_time = time.time()
    ntime = datetime.datetime.now()

    print('-----  START @ {:30s}  -------------------------------------------------------\n'.format(str(ntime)))

    excelBook = r'C:\Users\pwang\Desktop\2k3k_load_testing_analysis\2k3k_errored_files.xlsx'
    excelSheet ='2k_OutComplete'
    excelHeader ='filename'

    writeFileSizeListToFile(excelBook,excelSheet,excelHeader)


    print('\n-----  TOTAL {:30s} SECONDS --------------------------------------------------\n'.format(str(datetime.datetime.now() - ntime)))
    print('-----  END @ {:30s}  ---------------------------------------------------------------\n'.format(str(datetime.datetime.now())))

