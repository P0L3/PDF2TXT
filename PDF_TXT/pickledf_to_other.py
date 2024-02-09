import pandas as pd 

file = "/PDF_TXT/REPORTS/ehs_pos"
df = pd.read_pickle("{}.pickle".format(file))

df.to_excel("{}.xlsx".format(file))