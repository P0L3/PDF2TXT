import pandas as pd
from matplotlib import pyplot as plt


file = "unnamed.pickle"
df_ner = pd.read_pickle(file)

# # Assuming df is your DataFrame
# # Grouping by 'Tag' and counting occurrences of 'Entity'
# grouped = df_ner.groupby('Tag')['Entity'].count().reset_index()

# # Sorting by the count of occurrences
# sorted_grouped = grouped.sort_values(by='Entity', ascending=False)

# print(sorted_grouped)

grouped = df_ner.groupby(['Tag', 'Entity']).size().reset_index(name='Entity Count')

# Sorting by the count of occurrences
sorted_grouped = grouped.sort_values(by=['Tag', 'Entity Count'], ascending=[True, False])

print(sorted_grouped)

# for tag, data in sorted_grouped.groupby('Tag'):
#     plt.figure(figsize=(10, 6))
#     plt.barh(data['Entity'].head(20), data['Entity Count'].head(20))
#     plt.xlabel('Entity Count')
#     plt.ylabel('Entity')
#     plt.title(f'Top 20 Entities for Tag: {tag}')
#     plt.gca().invert_yaxis()  # Invert y-axis to have the highest count on top
#     plt.show()

def list_to_string(string_in_list):
    return " ".join(string_in_list)

df_ner["String_Title"] = df_ner['Title'].apply(list_to_string)

# Assuming df is your DataFrame
num_unique_titles = df_ner['String_Title'].nunique()
print("Number of unique titles:", num_unique_titles)