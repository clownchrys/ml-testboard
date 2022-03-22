string = """
SELECT M_Id
FROM
(
  SELECT
    A.M_Id
    , B.Gno
    , C.BizJobType_Code
    , C.BizJobtype_Bctgr_Code
    , row_number() OVER (PARTITION BY C.BizJobtype_Bctgr_Code, C.BizJobType_Code ORDER BY random()) AS rownum
  FROM (
    SELECT M_Id, Gno FROM job_db30_gg.log_gg_actvt
    UNION ALL
   
    SELECT M_Id, Gno FROM job_db30_etc.agi_click_login_hist
  ) A
  INNER JOIN JOB_DB30_GI.AGI_BizJobType B ON A.Gno = B.Gno
  INNER JOIN JOB_DB30_GI.Code_BizJobType C ON B.BizJobType_Code = C.BizJobType_Code
  WHERE A.Gno IN (SELECT Gno FROM mlresult.mf_gi_sim)
)
WHERE rownum <= 1
"""