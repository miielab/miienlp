import json
import csv

class Clean_WEAT():
    def __init__(self, clean_csv, clean_out):
        self.clean_csv = clean_csv
        self.clean_out = clean_out
        self.header = ['category',
                      'groups',
                      'decade',
                      'domain',
                      'embedding',
                      'model',
                      'm_assoc',
                      'f_assoc',
                      'abs_bias',
                      'bias',
                      'ewp',
                      'p_value',
                      't_statistic',
                      'n1 - male',
                      'n2 - female']

    def clean_row(self, in_row, writer):
        with open(in_row["file"]) as f:
            data = json.load(f)
            for domain in data.keys():
                for result in data[domain].keys():
                    if data[domain][result]["M_Assoc"] == -1:
                        continue

                    if in_row["corpus"] == "children":
                        decade, group, embedding, model = result.split('_')
                        if group == 'newbery' or group == 'caldecott' or group == 'csking':
                            continue
                    elif in_row["corpus"] == "histwords":
                         decade = result[:4]
                         group = 'histwords'
                         embedding = 'w2v'
                    else:
                        continue

                    m_assoc = data[domain][result]["M_Assoc"]
                    f_assoc = data[domain][result]["F_Assoc"]
                    abs_bias = data[domain][result]["Abs_Bias"]
                    bias = data[domain][result]["Bias"]
                    ewp = data[domain][result]["EWP"]
                    pvalue = data[domain][result]["P_value"]
                    tstat = data[domain][result]["T_statistic"]
                    n1 = data[domain][result]["N1"]
                    n2 = data[domain][result]["N2"]

                    out_row = [in_row["category"],
                               group,
                               decade,
                               domain,
                               embedding,
                               model,
                               m_assoc,
                               f_assoc,
                               abs_bias,
                               bias,
                               ewp,
                               pvalue,
                               tstat,
                               n1,
                               n2]
                    writer.writerow(out_row)

    def clean(self):
        with open(self.clean_csv, mode='r', encoding='utf-8-sig') as csv_file:
            clean_files = csv.DictReader(csv_file)
            with open(self.clean_out, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(self.header)
                for in_row in clean_files:
                    print(in_row)
                    self.clean_row(in_row, writer)
