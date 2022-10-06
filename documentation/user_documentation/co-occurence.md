# Co-occurence
## How to Run
1. Fork or clone the Co-occurrence repository
2. Change directories to the Co-occurrence repository `$ cd Co-occurrence`
3. Make sure Python3 is installed on your device and download the dependencies in one of two ways:
    - In the Co-occurrence directory type:
    ```
    $ pip install --user -r requirements.txt
    ```
    - OR Activate the virtual environment in the adukia project space on Midway
    ```
    $ source /project2/adukia/miie/text_analysis/dependencies/co_occurrence/co_occurrence/bin/activate
    ```
3. Edit the text, domains, and groups parameters in the default input.yaml file (located at `src/input.yaml`) to include the path where your data is located and save the file. For example, your input.yaml file could look like:
```
---
# Co-Occurrence inputs
text: /home/Downloads/testing_file.txt
domains: /home/supplemental_data/Categories/domain
groups: /home/supplemental_data/Categories/group
...
```
5. Run the default pipeline:
  ```
  $ python src/main.py
  ```
  
  
**IMPORTANT:** To customize your co-occurrence pipeline (see this [section](https://github.com/miielab/miienlp/blob/main/documentation/developer_documentation/co-occurence.md) for options), edit and save the `src/input.yaml` file, and then rerun step #5. 


## Dependencies
- [pandas](https://pandas.pydata.org/)
- [yaml](https://pyyaml.org/)
- Get more details: [requirements](https://github.com/adas-7/Co-occurrence/blob/main/requirements.txt)
