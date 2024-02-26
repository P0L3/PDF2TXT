import multiprocessing
import subprocess
import multiprocessing as mp
from tqdm import tqdm
from os import listdir

# Directory with files to process
DIR = "./SAMPLE/ENERPOL"
SCRIPT = "enerpol_htmlpars.py"
NUMBER_OF_TASKS = multiprocessing.cpu_count() - 2
print(f"Working in parallel on {NUMBER_OF_TASKS} threads.")

progress_bar = tqdm(total=NUMBER_OF_TASKS)
samples = listdir(DIR)[:20]

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
n_samples = list(split(samples, NUMBER_OF_TASKS))

if __name__ == '__main__':
    pool = mp.Pool(NUMBER_OF_TASKS)

    for n_s in n_samples:
        str_list = ",".join(n_s)
        # print(str_list)
        pool.apply_async(work, (str_list,), callback=update_progress_bar)

    pool.close()
    pool.join()


