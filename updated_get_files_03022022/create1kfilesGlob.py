import glob
import re
import os
import random
import datetime
import itertools
from datetime import date


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




def getBatchFiles(batchFileName, sqlScriptName, numOfFiles):
    mrlist = getMrList(numOfFiles)
    writeToFile(batchFileName, sqlScriptName, mrlist)


def getMrList(numOfFiles):
    randListA = shuffledList()
    randListB = shuffledList()

    mrlist = set()
    # print('getMRList', datetime.datetime.now())

    for i, j in itertools.product(randListA, randListB):
        if len(mrlist)==numOfFiles:
            return mrlist

        fpath = os.path.join(qcom, str(i).zfill(2), str(j).zfill(2), '*_M.pdf')
        # fl = glob.glob(fpath, recursive='True')
        fl = glob.glob(fpath)
        fl = fl[:50]

        # fl = sorted(fl, key= lambda x:os.stat(x).st_size)
        # for i in fl:
        #     print(i, os.stat(i).st_size)

        if len(fl) > 1:
            # random.shuffle(fl)
            fl = sorted(fl, key= lambda x:os.stat(x).st_size)
            mrlist.add(getFileParts(fl[0]))
            mrlist.add(getFileParts(fl[1]))

        print(datetime.datetime.now(), i, j, len(fl))



def writeToFile(batchFileName, sqlScriptName, mrlist:list):
    tdate = date.today().strftime('%m_%d')
    sqa2kCopyBatch = '{}_{}.bat'.format(batchFileName, tdate)
    sqa2kInsertSql = '{}_{}.sql'.format(sqlScriptName, tdate)

    removeFile(sqa2kCopyBatch)
    removeFile(sqa2kInsertSql)

    with open(sqa2kCopyBatch, 'w') as wf:
        for f in mrlist:
            wf.write(r'echo n | xcopy /s /y "{}" "\\qva\nonprod-nlp-sqa02\qcomtest\{}\{}"'.format(f[0],f[1],f[2]))
            wf.write('\n')

    with open(sqa2kInsertSql, 'w') as wf:
        for f in mrlist:
            wf.write(insert_temp.format(f[1],f[2], f[3], f[4]))
            wf.write('\n')



# ----------------------------------------------------------------------------------------------

def removeFile(fl:os.path):
    if os.path.isfile(fl):
        os.remove(fl)

    
def shuffledList():
    rndlist = [i for i in range(1,100)]
    random.shuffle(rndlist)
    return rndlist[:70]


def getFileParts(f):
    # random.shuffle(fl)
    # f = fl[0]
    dir1, dir2, fileName = f.split('\\')[4:]
    claimantID, caseID = fileName.split('_')[:2]
    return f, dir1, dir2, claimantID, caseID
    mrlist.add((f, dir1, dir2, claimantID, caseID))


# ----------------------------------------------------------------------------------------------

if __name__=='__main__':
    
    ntime = datetime.datetime.now()    
    print('-----  START @ {:24s}  -------------------------------------------------------\n'.format(str(ntime)))
    
    batchFileName = 'sqa1kList'
    sqlScriptName =  'sqa1kInsert'
    numOfFiles = 1000

    getBatchFiles(batchFileName, sqlScriptName, numOfFiles)

    
    print('\n-----  TOTAL {:24s} SECONDS --------------------------------------------------\n'.format(str(datetime.datetime.now() - ntime)))
    print('-----  END @ {:24s}  ---------------------------------------------------------------\n'.format(str(datetime.datetime.now())))

