import multiprocessing
import subprocess
import multiprocessing as mp
from tqdm import tqdm
from os import listdir

# Directory with files to process
DIR = "./SAMPLE/ENERPOL"
NUMBER_OF_TASKS = multiprocessing.cpu_count() - 2


progress_bar = tqdm(total=NUMBER_OF_TASKS)
samples = listdir(DIR)[:20]

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def work(str_list):
    command = ['python3', 'enerpol_htmlpars.py', "--str-list", str_list]
    subprocess.call(command)

def update_progress_bar(_):
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


