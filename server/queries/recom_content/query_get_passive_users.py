string = """
select uid, count(*) as activity_count
from mlresult_staging.contents_useractivity as act
group by uid
order by activity_count
limit 30
"""

