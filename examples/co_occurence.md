# Co-occurrence

**The data directory containing raw text, domain and group directories are the only required inputs.**

## Default input.yaml file

```
---
text: test_data/example_co-occurence.txt
domains: test_data/test_domain
groups: test_data/test_group
...
```

Some possible [groups](https://github.com/miielab/Categories/tree/main/group) and [domains](https://github.com/miielab/Categories/tree/main/domain) for users without pre-determined categories. 

#### (IMPORTANT - MiiE Lab RA only) These files can also be found on Midway at: 

`/project2/adukia/miie/text_analysis/supplemental_data/Categories/group/` and 
`/project2/adukia/miie/text_analysis/supplemental_data/Categories/domain/`


## Customized input.yaml file 

Custom flag and default options are further detailed [here](https://github.com/miielab/miienlp/blob/main/documentation/developer_documentation/co-occurence.md).
```
---
text: /path/to/text
domains: /path/to/domain_directory
groups: /path/to/group_directory
subcats: [male, female, family, appearance, business]
method: context
window: 3
scaled: False
output: /path/to/output_csv
difference: True
...
```

## How to Run

1. Edit and replace the `input.yaml` file in the [co-occurence folder](https://github.com/miielab/miienlp/tree/main/miienlp/co_occurrence).
2. Run the pipeline:
    ```
    $ python main.py
    ```


