import pandas as pd
import utils

class Aggregation(object):
    def __init__(self, metadata, output_dir):
        self.metadata = pd.read_csv(metadata, dtype="str")
        self.output_dir = output_dir
    
    def group(self, columns):
        '''
        Groups the dataframe based on specified columns
        '''
        return self.metadata.groupby(columns)

    def combine(self, group):
        '''
        Combines the text files for a given grouped dataframe
        '''
        paths = group['path'].tolist()
        text = ""
        for path in paths:
            with open(path) as infile:
                try:
                    text += infile.read() + "\n"
                except:
                    print("The following file could not be combined: " + path)
        return text

    def construct_output_filename(self, df, columns):
        '''
        Constructs output filenames based on grouped column values
        '''
        group = []
        for column in columns:
            group.append(df[column].iloc[0])
        return "_".join(group) + ".txt"
    
    def aggregate_lst(self, group_names):
        '''
        Aggregates data
        '''
        utils.makedir(self.output_dir)
        for group_name in group_names:
            grouped_df = self.group(group_name)
            for key, item in grouped_df:
                one_group = grouped_df.get_group(key) 
                output_file = self.construct_output_filename(one_group, group_name)
                text = self.combine(one_group)
                utils.save_output(text, self.output_dir + output_file)
        return 

    def aggregate_dict(self, group_names):
        for key, group_name in group_names.items():
            utils.makedir(self.output_dir + key)
            grouped_df = self.group(group_name)
            for key2, item in grouped_df:
                one_group = grouped_df.get_group(key2) 
                output_file = self.construct_output_filename(one_group, group_name)
                text = self.combine(one_group)
                output_file = self.output_dir + key + "/" + output_file
                utils.save_output(text, output_file)
        return

