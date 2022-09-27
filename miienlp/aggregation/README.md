# DataAggregation
![Data Aggregation](https://github.com/miielab/DataAggregation/workflows/Data%20Aggregation/badge.svg)

## Description
This script combines your data in customizable ways based on a metadata CSV file provided by the user. 

Let's say for example you have a collection of books and you want to determine whether stories that have a female protagonist are told in a different way than stories that have male protagonists. You can create a metadata spreadsheet that has information on the gender of the protagonist and the narration style (first person, not first person) of each book in your dataset. It may look something like this:
```
path,narration_style,protagonist_gender
data/gv_clean_counts/americas/2000/2005_americas_commended_carlson.txt,1,female
data/gv_clean_counts/arab/2000/2007_arab_winner_khalidi.txt,1,male
data/gv_clean_counts/bloomer_nf/2010/2014_bloomer_nf_winner_abdi.txt,1,female
data/gv_clean_counts/newbery_ia/1940/1947_newbery_honor_barnes.txt,0,female
data/gv_clean_counts/americas/1990/1995_americas_winner_temple.txt,0,male
```
Instead of running analysis on each book individually to answer your research question, you can aggregate these books into larger collections which will give you more accurate, representative results. This script will do the aggregation for you based on how you would like your data grouped.

