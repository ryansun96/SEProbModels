> This project was originally prepared for a course at Washington University in St. Louis. The project was not sponsored, reviewed, or endorsed by Stack Exchange or its affiliates in any way.

## Background

Stack Exchange is a famous online Q&A community featuring high quality content. It started in 2008 as Stack Overflow, and has gained tremendous popularity in ten years. Recently, however, people begin to criticize the site (network) for being less and less friendly. In particular, new questions are no longer answered in a timely manner; instead, they are likely to cause "downvote" or "flag as duplicate / off-topic" with no constructive input from community on how to improve the quality.

## Objective

The project tries to evaluate the aforementioned claim. Particularly, it tries to answer the following questions, and analyze the trend by time:

- How many answers does a question get?
- How many answers does a user contribute?
- How many answers does an OP have to wait, before the accepted answer was posted?

## Data source and processing

Stack Exchange publishes its data dump regularly on [archive.org](https://archive.org/details/stackexchange). The archive contains all questions and answers (collectively - posts) on the network since its creation till the time of the data dump. For the purpose of this project, we only care about metadata of the posts, i.e. creation date, user, etc.

[Special treatment](https://www.reddit.com/r/learnprogramming/comments/ax3etg/fastest_way_to_remove_an_attribute_in_very_large/) is required to extract attribute from Stack Overflow's **huge** (> 20GB) XML. Basically, it needs to be read in chunk by chunk, and parsed chunk by chunk. `xml_parser.py` in the repo does this job.


