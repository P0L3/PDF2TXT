import pandas as pd
from tqdm import tqdm

df = pd.read_csv("triples_full.csv", nrows=10000000)

print("Number of triples: ", len(df))
# print(df.keys())

# Lower everything
df["Relation"] = df["Relation"].apply(lambda x: x.lower() if isinstance(x, str) else x)
df["Head"] = df["Head"].apply(lambda x: x.lower() if isinstance(x, str) else x)
df["Tail"] = df["Tail"].apply(lambda x: x.lower() if isinstance(x, str) else x)

def fix_order(row):
    """
    Function to compare 'Head' and 'Tail' values and replace them if they are alphabetically in the wrong order.
    
    Parameters:
        row (pandas.Series): A row from a DataFrame containing 'Head' and 'Tail' columns.
        
    Returns:
        pandas.Series: The row with 'Head' and 'Tail' values possibly swapped if needed.
    """
    head = row['Head']
    tail = row['Tail']
    
    # Check if 'Head' comes after 'Tail' alphabetically
    if str(head) > str(tail):
        # Swap 'Head' and 'Tail'
        row['Head'], row['Tail'] = str(tail), str(head)
    
    return row
tqdm.pandas()

consistent_order_df = df.progress_apply(fix_order, axis=1)

# print(df[["Head", "Relation", "Tail"]])
# print(consistent_order_df[["Head", "Relation", "Tail"]])

unique_triples = consistent_order_df.drop_duplicates(subset=['Head', 'Relation', 'Tail'])

print(len(df))
print(len(consistent_order_df))
print(len(unique_triples))