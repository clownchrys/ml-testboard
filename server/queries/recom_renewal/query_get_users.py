string = """
SELECT DISTINCT m_id
FROM (
  SELECT m_id, gno FROM job_db30_gg.log_gg_actvt
  UNION ALL
  SELECT m_id, gno FROM job_db30_etc.agi_click_login_hist
) t
WHERE EXISTS (SELECT 1 FROM mlresult.mf_gi_sim sim WHERE sim.gno = t.gno)
"""