import multiprocessing
import subprocess
import multiprocessing as mp
from tqdm import tqdm
from os import listdir

# Directory with files to process
DIR = "./FULL_DATA/GCB"
SCRIPT = "gcb_htmlpars.py"
NUMBER_OF_TASKS = multiprocessing.cpu_count() - round(0.25 * multiprocessing.cpu_count())
BATCH_SIZE = NUMBER_OF_TASKS * 15  # You can adjust this based on your requirements
CHECKPOINT = ""


print(f"Working in parallel on {NUMBER_OF_TASKS} threads.")
print(f"Batch size: {BATCH_SIZE}")

progress_bar = tqdm(total=NUMBER_OF_TASKS)
samples = listdir(DIR)

if len(CHECKPOINT) > 10:
    samples = listdir(DIR)
    with open(CHECKPOINT, 'r') as stream:
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

    samples = samples_todo

def split_into_batches(lst, batch_size):
    """
    Split a list into batches of a specified size.

    Args:
    lst (list): The list to split.
    batch_size (int): The size of each batch.

    Returns:
    list: A list of batches, where each batch is a sublist of the original list.
    """
    return [lst[i:i+batch_size] for i in range(0, len(lst), batch_size)]

def split(a, n):
    """
    Split a list into n parts as evenly as possible.

    Args:
    a (list): The list to split.
    n (int): The number of parts to split the list into.

    Returns:
    generator: A generator yielding the split parts of the list.
    """
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def work(str_list):
    """
    Perform some work using subprocess.

    This function constructs a command and calls it using subprocess.

    Args:
    str_list (str): A string representing a list of items.

    Returns:
    None
    """
    command = ['python3', SCRIPT, "--str-list", str_list]
    subprocess.call(command)

def update_progress_bar(_):
    """
    Update a progress bar.

    Args:
    _ (any): Placeholder argument.

    Returns:
    None
    """
    progress_bar.update()

# Divide samples equally
    

# Split the samples list into batches
sample_batches = split_into_batches(samples, BATCH_SIZE)

# Now you can iterate over each batch and process them separately
for batch in tqdm(sample_batches):
    # Process each batch here
    n_samples = list(split(batch, NUMBER_OF_TASKS))

    if __name__ == '__main__':
        pool = mp.Pool(NUMBER_OF_TASKS)

        for n_s in n_samples:
            str_list = "ž".join(n_s)
            # print(str_list)
            pool.apply_async(work, (str_list,), callback=update_progress_bar)

        pool.close()
        pool.join()


