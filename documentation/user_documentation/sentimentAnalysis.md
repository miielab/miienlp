# Sentiment Analysis with Categorization

## How to Run 

1. Fork or clone the Sentiment Analysis repository. 
2. (Optional) Create a virtual (or conda) environment and activate that environment (this will ensure that any packages you already have downloaded on your personal computer do not conflict with the packages you will be installing for this analysis).
3. Download the dependencies:
    - In the `sentiment_analysis` folder, type:
    ```
    $ pip install --user -r requirements.txt
    ```
4. Fill out the empty `categories.csv` in the `category` folder. In the `Specific_Word` column, write specific words to be grouped into categories, and in the `category` column,write the actual category name for each of these words. For instance, "apple", "orange", and "mango" could all be assigned the "fruit" category label. In such an example, the `categories.csv` file would look like the following:

    | Specific_Word | Category |
    | --- | --- |
    | apple | fruit
    | orange | fruit
    | mango | fruit

5. Edit and save `sentiment_analysis/src/input.yaml` file with the data directory and output directory.

6. Navigate to the `src` folder (`cd src`) and run the pipeline:
    ```
    $ python src/main.py
    ```