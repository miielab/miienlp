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

**Note:** we provide three example files ([domain](https://github.com/miielab/miienlp/blob/main/examples/test_data/test_domain/example_domain_appearance.txt) and [group](https://github.com/miielab/miienlp/tree/main/examples/test_data/test_group)) which contain specific words we are interested in (for our analysis in particular). One may create new categories, depending on the analysis that needs to be performed. 

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
subcats: [male, female, family, appearance, business]. # those are the names of your domain txt files, and groups txt files. Please see the example yaml file for more information 
method: sentence
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


