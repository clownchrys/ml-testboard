string = """
WITH CTE AS (
  SELECT *
  FROM (
    SELECT
        M_Id
      , t.Gno
      , min(t.Actvt_Code) AS Actvt_Code
      , row_number() OVER (PARTITION BY M_Id ORDER BY max(Dt) DESC, min(Actvt_Code) ASC) AS Sort_Order -- SORT: LATEST TRAINED INTERACTIONj
    FROM (
      SELECT M_Id, Gno, Actvt_Code, Log_Dt AS Dt
      FROM JOB_DB30_GG.Log_GG_Actvt
      UNION ALL

      SELECT M_Id, Gno, 5 AS Actvt_Code, Hist_Dt AS Dt
      FROM JOB_DB30_ETC.AGI_Click_Login_Hist t
    ) t
    INNER JOIN mlresult.mf_gi_sim sim ON t.gno = sim.gno
    GROUP BY t.M_Id, t.Gno
  )
  WHERE Sort_Order <= 10
)

SELECT m_id, bizjobtype_bctgr_name, bizjobtype_name
FROM (
  SELECT *
      -- , row_number() OVER (PARTITION BY BizJobtype_Bctgr_Code, BizJobType_Code ORDER BY random()) AS rownum -- random sampling
      , row_number() OVER (PARTITION BY BizJobtype_Bctgr_Code, BizJobType_Code ORDER BY cnt DESC) AS rownum -- max sampling
  FROM (
    SELECT
        A.M_Id
      , B.Gno
      , B.BizJobType_Code, C.BizJobType_Name
      , C.BizJobtype_Bctgr_Code, D.BizJobType_Bctgr_Name
      , count() OVER (PARTITION BY A.M_Id, C.BizJobtype_Bctgr_Code, C.BizJobType_Code) AS cnt
    FROM CTE A
    INNER JOIN JOB_DB30_GI.AGI_BizJobType B ON A.Gno = B.Gno
    INNER JOIN JOB_DB30_GI.Code_BizJobType C ON B.BizJobType_Code = C.BizJobType_Code
    INNER JOIN JOB_DB30_GI.Code_BizJobtype_Bctgr D ON C.BizJobtype_Bctgr_Code = D.BizJobtype_Bctgr_Code -- to display bctgr name
  ) 
)
WHERE rownum <= 1
"""

