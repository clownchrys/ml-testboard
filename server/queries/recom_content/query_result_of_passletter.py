from models.recom_content import ResultByIdInput


def func(body: ResultByIdInput):
    query = f"""
with RESULT as (

    with PARAM(uid) as (

            select {body.uid!r} as uid --variable input

                    )

                        select uid, rst.cont_no, user_act.cont_type, rst.tag_type, rst.tag, user_act.Activity_Count, -1*(RANK() over (partition by rst.tag order by rst.score desc) - log2(user_act.Activity_Count)) as score

                            from (

                                select act.uid,cont_type,tag_type,tag,Activity_Count

                                    from mlresult_staging.contents_useractivity as act , PARAM

                                        where act.uid=PARAM.uid

                                            ) as user_act

                                                inner join mlresult_staging.contents_passletter as rst

                                                    on ( cast( user_act.tag_type as INT) =rst.tag_type and user_act.tag = cast(rst.tag as varchar) )

                                                    ),





                                                    --filter condition 

                                                    CONDITION as (

                                                        select A.job_epil_no as cont_no

                                                            FROM job_db30_gi.Ort_Job_Epil a

                                                                WHERE A.Front_Display_Stat = 1 and a.Job_Epil_Ctgr_Code=1

                                                                ),





                                                                --convert code to name

                                                                NAME as (

                                                                  select c_idx as tag , c_name as tag_name , 1 as tag_type

                                                                    from job_db30_gi.co_recruite_genealogy

                                                                      

                                                                        union all

                                                                          

                                                                            select bizjobtype_code as tag, bizjobtype_name as tag_name, 2 as tag_type

                                                                              from job_db30_gi.code_bizjobtype

                                                                                

                                                                                  union all 

                                                                                    

                                                                                      select job_news_kwrd_code as tag, job_news_kwrd_name as tag_name , 4 as tag_type

                                                                                        from job_db30_gi.code_job_news_kwrd



                                                                                          union all

                                                                                            

                                                                                              select job_itv_kwrd_code as tag, job_itv_kwrd_nm as tag_name, 5 as tag_type

                                                                                                from job_db30_gi.code_job_itv_kwrd

                                                                                                  ),

                                                                                                    

                                                                                                    -- prefer contents

                                                                                                    PREFER_CONTENT as (

                                                                                                      

                                                                                                        select 'prefer' as uid, a.job_epil_no as cont_no, NULL as tag_type ,NULL as tag_name, a.read_cnt as activity_count, NULL as score , a.reg_dt

                                                                                                            FROM job_db30_gi.Ort_Job_Epil a

                                                                                                                INNER JOIN job_db30_gi.CO_Recruite_Genealogy b ON a.C_Idx = b.C_IDX

                                                                                                                    INNER JOIN job_db30_gi.Ort_Pass_Pfl_Spec c ON a.Pass_Spec_No = c.Pass_Spec_No

                                                                                                                        INNER JOIN (select distinct(job_epil_no) from job_db30_gi.Ort_Job_Epil_Pass_Pfl_Item) d ON a.Job_Epil_No = d.Job_Epil_No

                                                                                                                            INNER JOIN job_db30_gi.Code_BizJobtype f ON a.BizJobtype_Code = f.BizJobtype_Code

                                                                                                                                WHERE A.Front_Display_Stat = 1 and a.Job_Epil_Ctgr_Code=1

                                                                                                                                )





                                                                                                                                -- result View

                                                                                                                                select *, 1 as sort_idx

                                                                                                                                from (

                                                                                                                                  select r.uid, r.cont_no, r.tag_type, n.tag_name, r.activity_count, r.score,

                                                                                                                                    concat('https://www.jobkorea.co.kr/starter/passassay/View?job_epil_no=',cast(r.cont_no as varchar)) as url

                                                                                                                                      from RESULT as r

                                                                                                                                        inner join NAME  as n

                                                                                                                                          on r.tag_type=n.tag_type and r.tag=n.tag

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

