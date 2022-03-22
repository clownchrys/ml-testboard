string = """
WITH RAW_TABLE AS
(
  SELECT
 
  t.gno,
  t.recom_gno,
  t.score
  FROM
  (
    SELECT gno, recom_gno, score, rank
    FROM (
        SELECT gno, recom_gno, rank()
               over (PARTITION BY gno ORDER BY score DESC) as rank, score
        FROM mlresult.mf_gi_sim where gno in
              (
                SELECT tt.gno gno
                from
                  (
                  SELECT gno, bizjobtype_code, rank() OVER (PARTITION BY bizjobtype_code ORDER BY rand()) AS rn
                  FROM (SELECT * from job_db30_gi.agi_bizjobtype where gno in (SELECT DISTINCT(gno) gno from mlresult.mf_gi_sim))
                  ) tt
                WHERE tt.rn=1
              )
    ) ranked_table
   
    WHERE ranked_table.rank <= 5
  ) t
  ORDER BY t.gno, t.score DESC
)
 
select
    t.gno
  , t.recom_gno
  , t.score
  , gno_info.gi_title AS title
  , recom_gno_info.gi_title AS title_recom
  , bzt._1 AS BZT_1
  , bzt._2 AS BZT_2
  , localty._1 AS LOCAL_1
  , localty._2 AS LOCAL_2
 
from RAW_TABLE t
 
-- title
LEFT JOIN (SELECT gno, gi_title FROM JOB_DB30_GI.AGI WHERE year IN (2021, 2022)) gno_info ON t.Gno = gno_info.Gno
LEFT JOIN (SELECT gno, gi_title FROM JOB_DB30_GI.AGI WHERE year IN (2021, 2022)) recom_gno_info ON t.recom_gno = recom_gno_info.gno
 
--biz
LEFT JOIN
(
  SELECT
        tb.gno gno,
        array_join(array_distinct(array_agg(bztc.BizJobType_Bctgr_Name)), ' / ') AS _1,
        array_join(array_distinct(array_agg(bzt.BizJobType_Name)), ' / ') AS _2
    FROM (SELECT DISTINCT(gno) gno from mlresult.mf_gi_sim) tb
    LEFT JOIN JOB_DB30_GI.AGI_BizJobtype agi_bzt ON (tb.gno = agi_bzt.Gno)
    LEFT JOIN JOB_DB30_GI.Code_BizJobtype bzt ON (agi_bzt.BizJobtype_Code = bzt.BizJobtype_Code)
    LEFT JOIN JOB_DB30_GI.Code_BizJobtype_Bctgr bztc ON bzt.BizJobtype_Bctgr_Code = bztc.BizJobtype_Bctgr_Code
    GROUP BY tb.gno
) bzt On t.recom_gno = bzt.gno
 
-- Localty
LEFT JOIN (
  SELECT
    tl.gno,
    array_join(array_distinct(array_agg(localty_outer.local_name)), ' / ') AS _1,
    array_join(array_distinct(array_agg(localty_inner.local_name)), ' / ') AS _2
  FROM (SELECT DISTINCT(gno) gno from mlresult.mf_gi_sim) tl
  LEFT JOIN JOB_DB30_GI.AGI_Work_Local agi_local ON tl.Gno = agi_local.Gno
  LEFT JOIN JOB_DB30_GI.Code_Local localty_inner ON agi_local.Local_Code = localty_inner.Local_Code
  LEFT JOIN JOB_DB30_GI.Code_Local localty_outer ON localty_inner.local_ctgr_code = localty_outer.Local_Code
  GROUP BY tl.gno
) localty ON t.recom_gno = localty.gno
 
order by t.gno, t.score desc
"""