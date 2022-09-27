import pytest, sys
import pandas as pd
sys.path.insert(0, '../../miienlp/aggregation')
from aggregation import Aggregation

class TestAggregation(object):
    def test_group1(self):
        # tests grouping of dataframe
        ag = Aggregation("metadata.csv", "")
        grouped_df = ag.group(["collection", "decade"])
        assert len(grouped_df) == 5
    
    def test_group2(self):
        # tests grouping of dataframe
        ag = Aggregation("metadata.csv", "")
        grouped_df = ag.group(["collection"])
        assert len(grouped_df) == 2
    
    def test_group3(self):
        # tests grouping of dataframe
        ag = Aggregation("metadata.csv", "")
        grouped_df = ag.group(["decade"])
        assert len(grouped_df) == 3

    def test_output1(self):
        # tests output filename creation
        ag = Aggregation("metadata.csv", "")
        columns = ["collection"]
        grouped_df = ag.group(columns)
        group = grouped_df.get_group('diversity')
        output_file = ag.construct_output_filename(group, columns)
        assert output_file == "diversity.txt"

    def test_combine(self):
        # tests combine method
        ag = Aggregation("metadata.csv", "")
        paths = ['test_data/gv_clean_counts/mainstream/1950/testing5m.txt', 
                'test_data/gv_clean_counts/diversity/1920/testing2d.txt']
        test_df = pd.DataFrame(paths, columns=['path'])
        string = ag.combine(test_df)
        assert string == "this is testing for mainstream 1950\n\nthis is diversity 1920\ndata!\n\n"

