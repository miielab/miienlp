
# Co-occurence
### Custom flag and default options:


| Input | Description |
| --- | --- |
| Text ***(required)*** | User filepath to text data for co-occurrence|
| Domains ***(required)*** | User filepath to directory containing text files of domain word lists|
| Groups ***(required)*** | User filepath to directory containing text files of group word lists|
| Subcategories | List of categories to be included from files within group and domain folders if user does not want to include all categories *(default is [])*|
| Method | Please enter `sentence` |
| Window | How many words the context window should be if using specified context *(default is 4)*|
| Scaled | Whether to scale counts in co-occurrence matrix by the total group or domain counts. Possible inputs include False, `group`, `domain` *(default is group)*|
| Output | User filepath to desired output CSV storage *(default is ./co_occurrence.csv)*|
| Difference | Whether to find the difference between the two co-occurrence columns *(default is True)*|
