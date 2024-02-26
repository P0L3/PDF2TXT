from os import listdir

DIR = "./FULL_DATA/MDPI/"
OUTPUT = "mdpi_output.txt"

samples = listdir(DIR)
with open(OUTPUT, 'r') as stream:
    samples_done = stream.readlines()

samples_todo = []

for sample in samples:
    if sample+"\n" in samples_done:
        continue
    else:
        samples_todo.append(sample)

print("Total samples: ", len(samples))
print("Approx done samples: ", len(samples_done))
print("Samples todo: ", len(samples_todo))