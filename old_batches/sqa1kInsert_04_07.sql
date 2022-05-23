INSERT INTO [dbo].[MR_Status]
           ([ClaimantID],[CaseID],[Status],[CreatedDate],[ModifiedDate],[FilePath],[ErrorMsg],[SID],[PageCount],[NLPStatus],[NLPInstanceID],[NLPRetry])
	VALUES
			(3874478, 3,'MRINDEX_COMPLETE', GetDate(), GetDate(),
			'\\qqtc-oc2\nonprod-nlp02\qcomtest\38\74\3874478_3_M.pdf',
			'Skipped',NULL,Null,Null,Null,Null)
GO
INSERT INTO [dbo].[MR_Status]
           ([ClaimantID],[CaseID],[Status],[CreatedDate],[ModifiedDate],[FilePath],[ErrorMsg],[SID],[PageCount],[NLPStatus],[NLPInstanceID],[NLPRetry])
	VALUES
			(3851408, 2,'MRINDEX_COMPLETE', GetDate(), GetDate(),
			'\\qqtc-oc2\nonprod-nlp02\qcomtest\38\51\3851408_2_M.pdf',
			'Skipped',NULL,Null,Null,Null,Null)
GO
INSERT INTO [dbo].[MR_Status]
           ([ClaimantID],[CaseID],[Status],[CreatedDate],[ModifiedDate],[FilePath],[ErrorMsg],[SID],[PageCount],[NLPStatus],[NLPInstanceID],[NLPRetry])
	VALUES
			(3821873, 8,'MRINDEX_COMPLETE', GetDate(), GetDate(),
			'\\qqtc-oc2\nonprod-nlp02\qcomtest\38\21\3821873_8_M.pdf',
			'Skipped',NULL,Null,Null,Null,Null)
GO
