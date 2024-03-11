import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("triples_full.csv", nrows=1000000)

# def to_lower


t2rr = [] # Triples to relation ratio
maxi = 0
for i in (10**p for p in range(1, 8)):
    if i < len(df):
        t2rr.append((i, len(pd.unique(df["Relation"].sample(i).apply(lambda x: x.lower() if isinstance(x, str) else x)))))
    else:
        i = len(df)
        maxi = i
        t2rr.append((i, len(pd.unique(df["Relation"].sample(i).apply(lambda x: x.lower() if isinstance(x, str) else x)))))
        break


# plt.title("Number of unique relations vs number of triples")
# plt.xlabel("Number of Triples")
# plt.ylabel("Number of Unique Relations")

# plt.plot([i[0] for i in t2rr], [i[1] for i in t2rr], marker='o')
# plt.ylim([0, maxi])
# plt.xlim([0, maxi])

# plt.show()
    

plt.title("Number of unique relations vs number of triples")
plt.xlabel("X Axis Label")
plt.ylabel("Y Axis Label") 
plt.plot(range(len(t2rr)), [i[0] for i in t2rr])
plt.plot(range(len(t2rr)), [i[1] for i in t2rr])
plt.tick_params(axis='both', which='major', labelbottom=False)
plt.show()
    
# Extract x and y data for bar plot
# x = [i[0] for i in t2rr]
# y1 = [i[0] for i in t2rr]
# y2 = [i[1] for i in t2rr]

# # Width of each bar
# bar_width = 0.35

# # Set the positions of the bars on the x-axis
# r1 = np.arange(len(x))
# r2 = [x + bar_width for x in r1]

# plt.figure(figsize=(10, 6))
# plt.bar(r1, y1, color='skyblue', width=bar_width, edgecolor='grey', label='Number of Triples')
# plt.bar(r2, y2, color='orange', width=bar_width, edgecolor='grey', label='Number of Unique Relations')

# # Add xticks on the middle of the group bars
# plt.xlabel('Number of Triples', fontweight='bold')
# plt.ylabel('Count', fontweight='bold')
# plt.xticks([r + bar_width/2 for r in range(len(x))], x)

# # Create legend & Show graphic
# plt.legend()
# plt.title('Number of unique relations vs number of triples')
# plt.show()
