> ## Abstract
> Stack Exchange

## Background

Stack Exchange is a famous online Q&A community featuring high quality content. It started in 2008 as Stack Overflow, and has gained tremendous popularity in ten years. Recently, however, people begin to criticize the site (network) for being less and less friendly. In particular, new questions are no longer answered in a timely manner; instead, they are likely to cause "downvote" or "flag as duplicate / off-topic" with no constructive input from community on how to improve the quality.

## Objective

The project tries to evaluate the aforementioned claim. Particularly, it tries to answer the following questions, and analyze the trend by time:

- How many answers does a question get, on average?
- How many answers does a user contribute, on average?
<!-- - How many answers does an OP have to wait, before the accepted answer was posted, on average? -->

## Data and pre-processing

Stack Exchange publishes its data dump regularly on [archive.org](https://archive.org/details/stackexchange). The archive contains all questions and answers (collectively - posts) on the network since its creation till the time of the data dump. For the purpose of this project, we only care about metadata of the posts, i.e. creation date, user, etc.

[Special treatment](https://www.reddit.com/r/learnprogramming/comments/ax3etg/fastest_way_to_remove_an_attribute_in_very_large/) is required to extract attribute from Stack Overflow's **huge** (> 20GB) XML. Basically, it needs to be read in chunk by chunk, and parsed chunk by chunk. `xml_parser.py` in the repo does this job.

The resulting `csv` file is imported into relational database. A few indices are added for performance reasons.

- SQL for distribution of # of answers for a question, within the first month it was posted:
```
with cte as (
select q.site, date_trunc('month', q.creationdate)::date as ym, q.postid, count(*) as answercount
from questions as q
left join answers as a on a.site = q.site and a.parentid = q.postid
				and a.creationdate between q.creationdate and q.creationdate + interval '30 days'
join (select site, max(creationdate) as creationdate
	  from questions
	  group by site) as md on md.site = q.site and q.creationdate <= md.creationdate - interval '30 days'
group by q.site, date_trunc('month', q.creationdate), q.postid
)
select site, ym, answercount, count(*) as question_cnt
from cte
group by site, ym, answercount;
```

- SQL for distribution of # of answers by a user, within each calendar month:
```
with summary as (
    select site, date_trunc('month', creationdate)::date as YM, owneruserid, count(*) as answer_cnt
from answers as a
where owneruserid is not null
group by site, date_trunc('month', creationdate), owneruserid
)
select site, YM, answer_cnt, count(*) as usr_cnt
from summary
group by 1,2,3;
```

<!-- - SQL for distribution of # of answers before the accepted one
```
with answer_rank as (
    select site, postid, parentid, rank() over(partition by site, parentid order by creationdate asc) as rnk
    from answers
)
select q.site, date_trunc('month', q.creationdate)::date as YM, a.rnk, count(*) as question_cnt
from questions as q
left join answer_rank as a on a.site = q.site and a.postid = q.acceptedanswerid and a.parentid = q.postid
group by q.site, date_trunc('month', q.creationdate), a.rnk;
``` -->

## Methodology

A simplistic approach would be to calculate the average by time, and make a plot. However, the author recognizes a few shortcoming of this method:

- 

> This project was originally prepared for a course at Washington University in St. Louis. The project was not sponsored, reviewed, or endorsed by Stack Exchange or its affiliates in any way.