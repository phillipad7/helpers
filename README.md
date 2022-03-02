# helpers

## UPDATE on 2022-03-02 

* Refined the code with more helper functions and parameters



## review_copy_audit_file.py 
1. Read an excel sheet with a single column contains file information( mostly clamaintID.caseID, with some exceptions)
2. Generate qva\qcom path
3. Write to a bat file so that user can run the batch file in remote windows and copy all available files to the destination
4. Export an exception list contains non-file(DATE info in the column), non-exist files(files not available in qva/qcom), wrong files(incorrect information in excel)
