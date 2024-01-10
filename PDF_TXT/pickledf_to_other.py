import pandas as pd 

file = "test_enerpol"
df = pd.read_pickle("{}.pickle".format(file))

df.to_excel("{}.xlsx".format(file))