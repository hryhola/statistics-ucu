from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

TASK_DIR = Path.cwd()
if (TASK_DIR / "labs" / "task2").is_dir():
    TASK_DIR = TASK_DIR / "labs" / "task2"
elif TASK_DIR.name == "notebooks":
    TASK_DIR = TASK_DIR.parent
INPUT_DIR = TASK_DIR / "input"
PDF_DIR = TASK_DIR / "pdf"
FIGURES_DIR = PDF_DIR / "figures"
SEED = 42
ALPHA = 0.05
rng = np.random.default_rng(SEED)
sns.set_theme(style="whitegrid")

FIGURES_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR = PDF_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)
plt.rcParams.update({"figure.dpi": 120, "savefig.bbox": "tight"})

pd.set_option("display.float_format", "{:.6g}".format)
