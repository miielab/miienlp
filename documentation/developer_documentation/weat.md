# WEAT
## WEAT metrics
The metrics specific to the WEAT tests are defined as follows:

* **Association**: mean of all the pairwise cosine similarities between word embeddings from two sets of words. Sometimes referred to as the association/the cosine similarity between two sets of words.
* **Female** or **Male Association**: if the domain is stated as X, then the female or male association is the association between female or male words and words of the X domain.
* **Gender Centeredness**: female-domain association minus male-domain association. Might also be referred to as *gender bias*.
* **EWP**: Percentage of WEAT test words that had a valid word embedding vector.

## WEAT modules

The file used for running WEAT analysis and cleaning (to prepare for visualizations) is [`main.py`](https://github.com/miielab/miienlp/blob/main/miienlp/weat/main.py). There are three modules that WEAT analysis calls: `fetchvec`, `wordtest`, and `utils`. The WEAT cleaning module is: `cleaning`.

To run visualizations, you can run [`line_graphs_viz.R`](https://github.com/miielab/miienlp/blob/main/miienlp/weat/line_graphs_viz.R) (line graphs) and [`bar_graphs_viz.R`](https://github.com/miielab/miienlp/blob/main/miienlp/weat/bar_graphs_viz.R) (for bar graphs).

### `Fetchvec`

Fetchvec looks at your input embeddings and extracts only the embeddings that will be needed to run the tests. These extracted embeddings are stored in a TEMP file (the location of the TEMP file is determined by the `out_dir` you specify in the YAML file - see the YAML file input descriptions for more details).

### `Wordtest`

Wordtest runs the actual calculations on the embeddings. The test we are currently using is called the T1 test, which measures male-domain and female-domain associations. For example, if the domain is *'science'*, we will get:
* the association (i.e., cosine similarity) between the word embeddings for male words and the word embeddings for science words; 
* the association between the word embeddings for female words and the word embeddings for science words; 
* the gender centerdness, which is female-science association minus male-science association; 
* the absolute value of the centeredness;  
* the effective word percentage, which tells one how many of the words that were tested are actually in the data;
* statistics, like t-statistic, p-value, n1 (total # of pairwise cosine similarities calculated between group 1 and the domain), and n2 (total # of pairwise cosine similarities calculated between group 2 and the domain).

### `Utils`

Contains YAML file parsing functionality and includes helpers for loading tests, loading models, and calculating scores (e.g., association between two sets of words) needed in the `Wordtest` module.

## `Cleaning`

Cleans up JSON files that were outputed by the WEAT analysis. It converts multiple JSON files into a single CSV file to prepare for visualizations.

### `line_graphs_viz.R`

Running this will save line graphs of centeredness or cosine similarity over time. You can edit this file to specify which graphs you want (under the headers *'Graphs'* and *'Saving graphs'*) and the input/output locations  (under the header *'Import Data'*).

### `bar_graphs_viz.R`

Running this will save bar graphs of centeredness or cosine similarity for each collection of books. You can edit this file to specify which graphs you want (under the headers *'Graphs'* and *'Saving graphs'*) and the input/output locations (under the header *'Import Data'*).


