"""Download the course dataset (raw job postings + skills) into data/raw/.

Students: run this ONCE, from your repo root (the folder with pyproject.toml):

    mkdir -p scripts
    curl -sL -o scripts/download_data.py https://raw.githubusercontent.com/lukebarousse/dbt_Analytics_Engineering_Course/main/project_1/scripts/download_data.py
    python scripts/download_data.py

Run it FROM THE REPO ROOT, not from inside scripts/ — files land in data/raw/
relative to wherever you run it (~85MB total). Re-running skips files you
already have. If `python` isn't found, your environment isn't activated;
`uv run scripts/download_data.py` always works.
"""

# import urllib.request
# from pathlib import Path

# REPO = "lukebarousse/dbt_Analytics_Engineering_Course"
# TAG = "dataset-v1"
# BASE = f"https://github.com/{REPO}/releases/download/{TAG}"

# MONTHS = [
#     "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12",
#     "2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06",
# ]
# FILES = [f"raw_job_postings_{m}.parquet" for m in MONTHS] + ["raw_job_skills.parquet"]

# DATA_DIR = Path.cwd() / "data" / "raw"   # relative to where you RUN it

# if __name__ == "__main__":
#     DATA_DIR.mkdir(parents=True, exist_ok=True)
#     for name in FILES:
#         dest = DATA_DIR / name
#         if dest.exists():
#             print(f"  already have {name}")
#             continue
#         print(f"  downloading {name} ...")
#         urllib.request.urlretrieve(f"{BASE}/{name}", dest)
#     print(f"Done. {len(FILES)} files in {DATA_DIR}")

import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = "lukebarousse/dbt_Analytics_Engineering_Course"
TAG = "dataset-v1"
BASE = f"https://github.com/{REPO}/releases/download/{TAG}"

MONTHS = [
    "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12",
    "2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06",
]
FILES = [f"raw_job_postings_{m}.parquet" for m in MONTHS] + ["raw_job_skills.parquet"]

DATA_DIR = Path.cwd() / "data" / "raw"


def download(url: str, dest: Path, retries: int = 5) -> None:
    tmp = dest.with_suffix(dest.suffix + ".part")
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=120) as r, open(tmp, "wb") as f:
                while chunk := r.read(1024 * 1024):
                    f.write(chunk)
            tmp.rename(dest)  # file only gets its real name when complete
            return
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            print(f"  attempt {attempt}/{retries} failed: {e}")
            tmp.unlink(missing_ok=True)
            if attempt == retries:
                raise
            time.sleep(2 ** attempt)  # 2s, 4s, 8s, 16s


if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        dest = DATA_DIR / name
        if dest.exists():
            print(f"  already have {name}")
            continue
        print(f"  downloading {name} ...")
        download(f"{BASE}/{name}", dest)
    print(f"Done. {len(FILES)} files in {DATA_DIR}")
