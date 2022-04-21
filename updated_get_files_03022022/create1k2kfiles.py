''' Randomly get files from \\qva\qcom pool took tramandously long time
    and also does not verify if created path is valid or not.
    Improved with glob library in other script
'''


import os
import random
from datetime import date

insert_temp = r'''INSERT INTO [dbo].[MR_Status]
           ([ClaimantID],[CaseID],[Status],[CreatedDate],[ModifiedDate],[FilePath],[ErrorMsg],[SID],[PageCount],[NLPStatus],[NLPInstanceID],[NLPRetry])
	VALUES
			({2}, {3},'MRINDEX_COMPLETE', GetDate(), GetDate(),
			'\\qqtc-oc2\nonprod-nlp02\qcomtest\{0}\{1}\{2}_{3}_M.pdf',
			'Skipped',NULL,Null,Null,Null,Null)
GO'''

qva_root = r'\\qva\qcom'
outFile = ''
alist = [i for i in range(1,91)]




# with open('sqa1kList', 'w') as wf:

def getOneKFile():
    oneKList=set()
    
    while len(oneKList) < 100:
        # print(len(oneKList)) 

        dir1, dir2 = str(random.choice(alist)), str(random.choice(alist)).zfill(2)
        rest = str(random.randrange(1,199)).zfill(2)
        claimantID = dir1+dir2+rest
        dir1 = dir1.zfill(2)

        # caseID = random.choice([1,2])
        # fileName = r'{}_{}_M.pdf'.format(claimantID, caseID)
        # fpath = os.path.join(qva_root, dir1, dir2, fileName)
        # print(claimantID, caseID, fpath)
        
        
        # if os.path.isfile(fpath):
        #     oneKList.add((fpath,dir1,dir2))


        caseID = [i for i in range(1,6)]

        for id in caseID:
            fileName = r'{}_{}_M.pdf'.format(claimantID, id)
            fpath = os.path.join(qva_root, dir1, dir2, fileName)
            if os.path.isfile(fpath):
                oneKList.add((fpath,dir1,dir2, claimantID, id))
                    
        print(dir1, dir2, claimantID, id, fpath)
        
        


    with open('sqa1kList_{}.bat'.format(date.today().strftime('%m_%d')), 'w') as wf:
        for i in oneKList:
            wf.write(r'echo n | xcopy /s /y "{}" "\\qva\nonprod-nlp-sqa02\qcomtest\{}\{}"'.format(i[0],i[1],i[2]))
            wf.write('\n')

    with open('sqa1kInsert_{}.sql'.format(date.today().strftime('%m_%d')), 'w') as wf:
        for c in oneKList:
            wf.write(insert_temp.format(c[1],c[2], c[3], c[4]))
            wf.write('\n')







if __name__=='__main__':
    getOneKFile()
    # pass