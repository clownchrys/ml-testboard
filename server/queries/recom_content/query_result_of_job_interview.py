from models.recom_content import ResultByIdInput


def func(body: ResultByIdInput):
    query = f"""
with RESULT as (

	with PARAM(uid) as (

		select {body.uid!r} as uid

		)



	select uid, rst.cont_no, user_act.cont_type, rst.tag_type, rst.tag, user_act.Activity_Count, -1*(RANK() over (partition by rst.tag order by rst.score desc) - log2(user_act.Activity_Count)) as score

	from (

  	select act.uid,cont_type,tag_type,tag,Activity_Count

	from mlresult_staging.contents_useractivity as act , PARAM

	where act.uid=PARAM.uid

	) as user_act

	inner join mlresult_staging.contents_jobinterview as rst

	on ( cast( user_act.tag_type as INT) =rst.tag_type and user_act.tag = cast(rst.tag as varchar))

),

--filter condition 

CONDITION as (

	select A.itv_no as cont_no

	from job_db30_gi.Co1000_Job_Itv as A

	WHERE A.Display_Stat = 1

	AND (A.Display_Start_Dt < current_timestamp OR A.Display_Start_Dt IS NULL)

),





--convert code to name

NAME as (

  select cast(c_idx as varchar) as tag , c_name as tag_name , 1 as tag_type

  from job_db30_gi.co_recruite_genealogy

  

  union all

  

  select cast(bizjobtype_code as varchar) as tag, bizjobtype_name as tag_name, 2 as tag_type

  from job_db30_gi.code_bizjobtype

  

  union all 

  

  select cmmn_code as tag, cmmn_code_name as tag_name, 3 as tag_type

  from job_db30_gi.Code_Job_Itv



  union all

  

  select cast(job_itv_kwrd_code as varchar) as tag, job_itv_kwrd_nm as tag_name, 5 as tag_type

  from job_db30_gi.code_job_itv_kwrd

  ),



-- prefer contents

PREFER_CONTENT as (



select 'prefer' as uid, a.itv_no as cont_no, NULL as tag_type ,NULL as tag_name, a.click_cnt as activity_count, NULL as score, a.reg_dt



FROM job_db30_gi.Co1000_Job_Itv a

INNER JOIN job_db30_gi.Code_Job_Itv b ON a.Job_Ctgr_Str_Code = b.Cmmn_Code

INNER JOIN job_db30_gi.CO_Recruite_Genealogy c ON a.C_Idx = c.C_IDX

WHERE A.Display_Stat = 1

AND (A.Display_Start_Dt < current_timestamp OR A.Display_Start_Dt IS NULL  
))





-- result View

select *, 1 as sort_idx

from (

  select r.uid, r.cont_no, r.tag_type, n.tag_name, r.activity_count, r.score,

  concat('https://www.jobkorea.co.kr/starter/interview/View/?itv_no=',cast(r.cont_no as varchar)) as url

  from RESULT as r

  inner join NAME  as n

  on r.tag_type=n.tag_type and cast(r.tag as varchar)=n.tag

  inner join CONDITION as c

  on r.cont_no=c.cont_no

  order by score desc

  limit 30

  )



union all



select *, 2 as sort_idx

from (

  select uid, cont_no, tag_type, tag_name, activity_count, score, concat('https://www.jobkorea.co.kr/start/review/view?job_epil_no=',cast(cont_no as varchar)) as url

  from PREFER_CONTENT

  where DATE_DIFF('DAY',reg_dt, current_timestamp ) < 14

  order by activity_count desc

  limit 30

  )



union all



select * , 3 as sort_idx

from (

select uid, cont_no, tag_type, tag_name, activity_count, score, concat('https://www.jobkorea.co.kr/start/review/view?job_epil_no=',cast(cont_no as varchar)) as url

from PREFER_CONTENT

order by reg_dt desc

limit 30)

order by sort_idx, score desc

limit 30
    """
    return query

