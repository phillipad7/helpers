import os
import re
# import datetime
from datetime import date, datetime
from pathlib import Path


qcom = r'\\qva\qcom'
# ptn = re.compile(r'\d{4,7}_\d{1,2}_[M|m]\.pdf.')
mrlist = set()

insert_temp = r'''INSERT INTO [dbo].[MR_Status]
           ([ClaimantID],[CaseID],[Status],[CreatedDate],[ModifiedDate],[FilePath],[ErrorMsg],[SID],[PageCount],[NLPStatus],[NLPInstanceID],[NLPRetry])
	VALUES
			({2}, {3},'MRINDEX_COMPLETE', GetDate(), GetDate(),
			'\\qva\nonprod-nlp-sqa02\qcomtest\{0}\{1}\{2}_{3}_M.pdf',
			'Skipped',NULL,Null,Null,Null,Null)
GO'''



def regenBatchFiles(batchFileName, sqlScriptName, numOfFiles, inputFile):
    mrlist = sortFileBySize(numOfFiles, inputFile)
    writeToFile(batchFileName, sqlScriptName, mrlist)



def sortFileBySize(numOfFiles, inputFile):
    print('-----  START sorting @ {:24s}  --------------------------------\n'.format(str(ntime)))
    
    with open(inputFile, 'r') as f:
        fl = f.readlines()
        # fl = fl[:numOfFiles]

        fl = [re.split('\s|"', i)[7] if os.stat(re.split('\s|"', i)[7]).st_size <630000000 else '' for i in fl]

        # fl = [re.split('\s|"', i)[7] for i in fl]
        # fl = [Path(re.split('\s|"', i)[7]) for i in fl][:10]
        # fl = sorted(fl, key=lambda x: os.stat(x).st_size, reverse=True)

    print(fl)
    print('------  DONE sorting @ {:24s}  --------------------------------\n'.format(str(ntime)))
    return fl




def writeToFile(batchFileName, sqlScriptName, mrlist:list):
    print('-----  START writing to file @ {:24s}  --------------------------------\n'.format(str(ntime)))
    
    tdate = date.today().strftime('%m_%d')
    sqa2kCopyBatch = '{}_{}.bat'.format(batchFileName, tdate)
    sqa2kInsertSql = '{}_{}.sql'.format(sqlScriptName, tdate)

    removeFile(sqa2kCopyBatch)
    removeFile(sqa2kInsertSql)

    with open(sqa2kCopyBatch, 'w') as wf:
        for f in mrlist:
            if f != '':
                print(f)
                f = getFileParts(f)
                wf.write(r'echo n | xcopy /s /y "{}" "\\qva\nonprod-nlp-sqa02\qcomtest\{}\{}"'.format(f[0],f[1],f[2]))
                wf.write('\n')


    with open(sqa2kInsertSql, 'w') as wf:
        for f in mrlist:
            if f != '':
                f = getFileParts(f)
                wf.write(insert_temp.format(f[1],f[2], f[3], f[4]))
                wf.write('\n')


def removeFile(fl:os.path):
    if os.path.isfile(fl):
        os.remove(fl)


def getFileParts(f):
    dir1, dir2, fileName = f.split('\\')[4:]
    claimantID, caseID = fileName.split('_')[:2]

    print(dir1,dir2,fileName,claimantID, caseID)
    return f, dir1, dir2, claimantID, caseID




if __name__=='__main__':
    ntime = datetime.now()    
    print('-----  START @ {:24s}  -------------------------------------------------------\n'.format(str(ntime)))
    
    batchFileName = 'sqa1kList_600M_add200file'
    sqlScriptName =  'sqa1kInsert_600M_add200file'
    numOfFiles = 200

    # fname = r'C:\Users\pwang\Downloads\helpers\sqa3kList_04_11_copy.bat'
    fname = r'C:\Users\pwang\Downloads\helpers\sqa1kList_06_07.bat'
    regenBatchFiles(batchFileName, sqlScriptName, numOfFiles, fname)

  
    print('\n-----  TOTAL {:24s} SECONDS --------------------------------------------------\n'.format(str(datetime.now() - ntime)))
    print('-----  END @ {:24s}  ---------------------------------------------------------------\n'.format(str(datetime.now())))

