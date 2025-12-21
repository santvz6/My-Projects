import os
import shutil
from datetime import datetime

from config import NUM_LOGS, NUM_PLOTS

def prepare_plot_folder(base_dir, limit=NUM_PLOTS):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    current_run_dir = os.path.join(base_dir, f"run_{timestamp}")
    
    if not os.path.exists(current_run_dir):
        os.makedirs(current_run_dir)

    all_runs = [os.path.join(base_dir, d) for d in os.listdir(base_dir) 
                if os.path.isdir(os.path.join(base_dir, d)) and d.startswith("run_")]
    all_runs.sort(key=os.path.getctime)

    while len(all_runs) >= limit:
        oldest_dir = all_runs.pop(0)
        shutil.rmtree(oldest_dir)


    return current_run_dir

def remove_old_logs(logs_dir, limit=NUM_LOGS):
    logs = sorted(
        [f for f in os.listdir(logs_dir) if f.endswith(".log")],
        key=lambda x: os.path.getmtime(os.path.join(logs_dir, x))
    )

    while len(logs) >= limit:
        oldest_log = logs.pop(0)
        os.remove(os.path.join(logs_dir, oldest_log))
