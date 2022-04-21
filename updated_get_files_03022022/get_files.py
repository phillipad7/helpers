from doctest import OutputChecker
import pandas as pd
import os
from datetime import datetime

qva_root = '\\\qva\qcom'
# excp_list = []
# file_list = []


insert_temp = r'''INSERT INTO [dbo].[MR_Status]
           ([ClaimantID],[CaseID],[Status],[CreatedDate],[ModifiedDate],[FilePath],[ErrorMsg],[SID],[PageCount],[NLPStatus],[NLPInstanceID],[NLPRetry])
	--VALUES(<ClaimantID, numeric(18,0),>,<CaseID, numeric(18,0),>,<Status, varchar(50),>,<CreatedDate, datetime,>,<ModifiedDate, datetime,>,<FilePath, varchar(300),>,<ErrorMsg, varchar(5000),>,<SID, varchar(100),>,<PageCount, int,>,<NLPStatus, datetime,>,<NLPInstanceID, varchar(200),>,<NLPRetry, smallint,>)
	VALUES
			({0},
			{1},
			'MRINDEX_COMPLETE',
			GetDate(),--CreatedDate,
			GetDate(),
			'\\qqtc-oc2\nonprod-nlp02\qcomtest\{2}\{3}\{0}_{1}_M.pdf',
			'Skipped',NULL,Null,Null,Null,Null)
GO'''



def export_path_param(excelBook:str, excelSheet:str, excelHeader:str, outBatchFile:str, exceptionFile:str):
    mr_list = read_excel_param(excelBook, excelSheet, excelHeader, exceptionFile)
    write_batch_file(outBatchFile, mr_list)


def read_excel_param(excelBook: str, excelSheet:str, excelHeader:str, exceptionFile:str):
    print('**** {:22s} ****'.format('Processing Excel File'))

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
        print('**** {:24s} ****'.format('Writing to File'))
        for i in mr_list:
            seg1, seg2, seg3 = i.split('\\')[-3:]
            claimantID, caseID = seg3.split('_')[:2]
            # print(seg1, seg2, seg3, claimantID, caseID, '/n')

            '''
            #### Write to batch copy to QQTC-OC2 ####
            '''
            # wf.write('echo n | xcopy /s /y "' + i + r'" "\\qva\nonprod-nlp-uat02\qcomtest\{}\{}"'.format(seg1,seg2))
            # wf.write('echo n | xcopy /s /y "' + i + r'" "\\Devqva\devnlpshare\TEMP_50_"')
            wf.write('echo n | xcopy /s /y "' + i + '" "'+ r'\\qqtc\nonprod-nlp01\devnlpapp01b\temp_ann_err"')
            
            '''
            ##### SQL Insert Script ####
            '''
            # wf.write(insert_temp.format(claimantID, caseID, seg1, seg2))



            wf.write('\n')
    
    print('**** {:24s} ****'.format('DONE Writing'))

    

'''
add src and desc argument to identify source location to copy from and destination where will copy to.
'''
def write_batch_file_arg(outBatchFile:os.path, mr_list:str, src:os.path, desc:os.path):
    pass






# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

def export_path(fileName:str):
    mr_list = read_excel(fileName)
    with open('export_15_file_list.bat', 'w') as wf:
        print('**** {:20s} ****'.format('Writing to File'))

        for i in mr_list:
            seg1, seg2 = i.split('\\')[-3:-1]
            wf.write('echo n | xcopy /s /y "' + i + '" "\\\dsrc3\shared\qcomtest\{}\{}"'.format(seg1,seg2))
            # wf.write('echo n | xcopy /s /y "' + i + '" "\\\devqva\DevNLPShare\\temp"' )
            wf.write('\n')
    
    print('**** {:20s} ****'.format('DONE Writing'))



def read_excel(fileName: str):
    print('**** {:20s} ****'.format('Processing Excel File'))

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
def construct_file_path(raw):
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



    inputExcelBook = r'C:\Users\pwang\Desktop\NLP5.2_UAT_20.xlsx'
    excelSheet = 'Sheet1'
    excelHeader = 'Production'
    outBatchFile = 'NLP5.2_UAT_20_batch_0418_TP.bat'
    exceptionFile = 'NLP5.2_UAT_20_exception_0418'
    # outBatchFile = 'NLP5.2_UAT_20_insert_0418.sql'
    # exceptionFile = 'NLP5.2_UAT_20_insert_exception_0418'


    # inputExcelBook = r'C:\Users\pwang\Desktop\50_dup_page_test_file.xlsx'
    # outBatchFile = '50_dup_page_test_batch_0315.bat'
    # exceptionFile = '50_dup_page_test_exception_0315'

    # inputExcelBook = r'C:\Users\pwang\Desktop\all_annotation_error.xlsx'
    # outBatchFile = 'all_prod_annotation_error_batch_0316.bat'
    # exceptionFile = 'all_prod_annotation_exception_0316'



    import datetime
    ntime = datetime.datetime.now()    
    print('-----  START @ {:30s}  -------------------------------------------------------\n'.format(str(ntime)))

    export_path_param(inputExcelBook, excelSheet, excelHeader, outBatchFile, exceptionFile)


    # for s in ['batch1','batch2','batch3','batch4']:
    #     export_path_param(inputExcelBook, s, excelHeader, outBatchFile+'_{}'.format(s), exceptionFile+'_{}'.format(s))



    print('\n-----  TOTAL {:30s} SECONDS --------------------------------------------------\n'.format(str(datetime.datetime.now() - ntime)))
    print('-----  END @ {:30s}  ---------------------------------------------------------------\n'.format(str(datetime.datetime.now())))

