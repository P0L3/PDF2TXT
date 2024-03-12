import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("triples_full.csv", nrows=10000000)

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

print("Growth of unique relations (verbs): ", t2rr)

plt.title("Number of unique relations vs number of triples")
plt.xlabel("X Axis Label")
plt.ylabel("Y Axis Label") 
plt.plot(range(len(t2rr)), [i[0] for i in t2rr])
plt.plot(range(len(t2rr)), [i[1] for i in t2rr])
plt.tick_params(axis='both', which='major', labelbottom=False)
plt.show()
    
