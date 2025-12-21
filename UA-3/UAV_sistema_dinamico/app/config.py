import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOGS_DIR = os.path.join(BASE_DIR, "logs")
RES_DIR = os.path.join(BASE_DIR, "res")
PLOT_DIR = os.path.join(RES_DIR, "plots")

NUM_LOGS = 5
NUM_PLOTS = 5