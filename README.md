# AIOps — Module 1 Assignment

**Raghav Iyengar (DA24B020)** · Partner for Q4: **Dhanush (DA24B019)**

Single submission repository for Module 1. Q1–Q3 live here; Q4 was done in a
separate shared repository (linked below) so that both partners could commit to
the same history.

---

## Where each answer is

| Question | Marks | Deliverable | Location |
|---|---|---|---|
| **Q1** — Technical debt diagnosis | 10 | Category identification + mitigation | §1 of the write-up PDF |
| **Q2** — MLflow experiment comparison | 15 | | |
| ⤷ comparison screenshot | 4 | run comparison + per-run detail | [`Q2/mlflow_logs.png`](Q2/mlflow_logs.png), [`Q2/run_details.png`](Q2/run_details.png), [`Q2/params_metrics.png`](Q2/params_metrics.png) |
| ⤷ written analysis | 7 | 150–250 words | §2 of the write-up PDF · curves: [`Q2/train_loss.png`](Q2/train_loss.png), [`Q2/val_accuracy.png`](Q2/val_accuracy.png) |
| ⤷ logging code | 4 | `log_param` / `log_metric` calls | [`Q2/Question2_NB.ipynb`](Q2/Question2_NB.ipynb), `train_and_log` cell · also quoted in §2 of the PDF |
| **Q3** — DVC versioning & rollback | 10 | | |
| ⤷ init + push v1 | 2 | tag `v1`, 1800 rows | [`q3/Q3.txt`](q3/Q3.txt) |
| ⤷ update to v2 | 3 | tag `v2`, 2800 rows | [`q3/Q3.txt`](q3/Q3.txt) |
| ⤷ rollback proof | 5 | row count + md5 | [`q3/Q3.txt`](q3/Q3.txt) PART 3 · [`q3/evidence/rollback.txt`](q3/evidence/rollback.txt) |
| **Q4** — Reproducibility capstone | 15 | Full drill with partner | [`q4/Q4.txt`](q4/Q4.txt) + screenshots below · **shared repo** ↓ |
| ⤷ Partner A: train, track, register | 6 | run detail, artifacts, registry | [`q4/A_run_details.png`](q4/A_run_details.png), [`q4/A_run_artifacts.png`](q4/A_run_artifacts.png), [`q4/Model_details.png`](q4/Model_details.png) |
| ⤷ Partner B: reproduction | 6 | run detail | [`q4/B_run_details.png`](q4/B_run_details.png) |
| ⤷ reproduction note | 3 | `repro_note` verdict | [`q4/B_comparison_log.png`](q4/B_comparison_log.png) |
| **Write-up** | — | One-page PDF | `writeup/aiops_m1_writeup.pdf` |
| **AI use disclosure** | — | | [`ai_use.md`](ai_use.md) |

### Q4 shared repository

**https://github.com/DA24B020/aiops-m1-da24b019-da24b020**

Commits are prefixed `[A]` (Raghav) and `[B]` (Dhanush) so each partner's
contribution is attributable from the history alone:

```bash
git log --pretty=format:'%h %an %s'
```

Key values from the drill:

| | |
|---|---|
| Commit reproduced | `ac32533` |
| Partner A run | `1bfc37a0`, seed 42, `git_dirty=false`, `final_val_accuracy = 1.0000` |
| Partner B run | `47ff794f`, `final_val_accuracy = 1.0000` |
| Verdict | MATCH, \|Δ\| = 0.0000 against a tolerance of ±0.005 declared in advance |
| Registered model | `m1-capstone-model` v3, stage **Staging** |

---

## Repository layout

```
.
├── README.md
├── ai_use.md
├── requirements.txt
├── .dvc/config                  DVC remote config (no credentials)
├── Q2/
│   ├── Question2_NB.ipynb       MLP on MNIST, 7 tracked runs
│   ├── mlflow_logs.png          run comparison
│   ├── run_details.png
│   ├── params_metrics.png
│   ├── train_loss.png
│   └── val_accuracy.png
├── q3/
│   ├── Q3.txt                   full annotated terminal transcript
│   ├── evidence/rollback.txt    rollback transcript
│   ├── filelist.csv.dvc         DVC pointer (data itself is in S3)
│   └── scripts/make_filelist.py builds the versioned CSV
├── q4/
│   ├── Q4.txt                   full drill transcript, both partners
│   ├── A_run_details.png        params, seed, git_commit, git_dirty
│   ├── A_run_artifacts.png      logged model artifact
│   ├── Model_details.png        registry, v3 in Staging
│   ├── B_run_details.png        Partner B's reproduction run
│   └── B_comparison_log.png     repro_note verdict
└── writeup/
    └── aiops_m1_writeup.pdf
```

Git tags `v1` and `v2` mark the two dataset versions used in Q3.

---

## Setup

```bash
git clone https://github.com/DA24B020/aiops-as1.git
cd aiops-as1

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start a tracking server before running the Q2 notebook:

```bash
mlflow server --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlruns \
  --host 0.0.0.0 --port 5000 \
  --allowed-hosts "*" --cors-allowed-origins "*"
```

Then open `Q2/Question2_NB.ipynb` and run all cells. The first cell downloads
MNIST from OpenML (cached afterwards); the sweep takes roughly 15 minutes.

### Reproducing Q3

```bash
dvc pull                              # requires access to the S3 remote — see below
dvc checkout
wc -l q3/filelist.csv                 # 2801 at v2

git checkout v1 && dvc checkout
wc -l q3/filelist.csv                 # 1801 at v1
git checkout main && dvc checkout
```

Without S3 access the CSV can be regenerated from scratch, since the source
data is public:

```bash
dvc get https://github.com/iterative/dataset-registry tutorials/versioning/data.zip
unzip -q data.zip && rm -f data.zip
python q3/scripts/make_filelist.py --root data --out q3/filelist.csv   # 1801 lines

dvc get https://github.com/iterative/dataset-registry tutorials/versioning/new-labels.zip
unzip -q new-labels.zip && rm -f new-labels.zip
python q3/scripts/make_filelist.py --root data --out q3/filelist.csv   # 2801 lines
```

---

## DVC remote (S3)

```
s3://aiops-da24b019-da24b020/q3/dvcstore     region ap-south-1
```

The bucket is private. `.dvc/config` holds only the URL and region — credentials
are read from `~/.aws/credentials` and never committed. Access is granted per
user through an IAM policy scoped to this one bucket:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    { "Effect": "Allow",
      "Action": ["s3:ListBucket", "s3:GetBucketLocation"],
      "Resource": "arn:aws:s3:::aiops-da24b019-da24b020" },
    { "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
      "Resource": "arn:aws:s3:::aiops-da24b019-da24b020/*" }
  ]
}
```

Each partner has their own IAM user and access key rather than a shared
credential, so access can be revoked individually. Evaluators needing `dvc pull`
can request a key; otherwise use the regeneration commands above.

---

## Notes on replication

Three things surfaced during the assignment that are worth recording, because
each one is a place where the reproducibility protocol did **not** hold.

### 1. `pip freeze` produced an unsatisfiable requirements file

`requirements.txt` was generated with `pip freeze`, which pins every transitive
dependency at its locally installed version. On Partner B's machine the install
failed outright:

```
ERROR: Cannot install aiobotocore==3.9.0 and botocore==1.43.83 because these
package versions have conflicting dependencies.
    aiobotocore 3.9.0 depends on botocore<1.43.57 and >=1.43.3
```

The pinned set resolved on the machine that generated it and nowhere else.
Partner B therefore trained with whatever packages his environment already had.
The metric still matched, but the environment was not actually reproduced — the
match reflects a fixed-seed MLP on a small dataset being robust, not a
successful environment rebuild. A hand-maintained direct-dependency list, or a
proper lockfile, would have avoided this.

### 2. A requirements file cannot pin the interpreter

Partner A ran Python 3.13, Partner B ran 3.14. Nothing in `requirements.txt`
constrains the interpreter version, so this difference passed unnoticed until it
appeared in a traceback. `environment.yml` pins `python=`, but the venv route
bypasses it entirely. Pinning the interpreter belongs alongside pinning the
packages.

### 3. Infrastructure configuration travelled with neither the code nor the data

The MLflow server was initially started with `--default-artifact-root ./mlruns`,
a path local to Partner A's machine. Partner B's runs logged their metrics fine
and then failed when writing artifacts:

```
PermissionError: [Errno 13] Permission denied: '/home/raghav-iyengar'
```

Two further points came out of fixing it. An experiment's artifact location is
fixed **when the experiment is created**, so changing the server's default did
nothing for the existing experiment and a new one (`m1-capstone-v2`) had to be
made. And once artifacts moved to S3, `boto3` turned out to be a required
dependency that had never appeared in `requirements.txt`, because it was not
needed under the previous local-artifact configuration.

The general lesson: the protocol pinned code, data, environment and seed, but
the *server configuration* was a fourth input that no artifact in the repository
captured.

### Smaller issues

- The dataset path given in the lecture deck (`tutorial/ver/`) no longer exists;
  the registry has been reorganised to `tutorials/versioning/`. A small live
  example of the unstable-data-dependency problem from Lecture 1.
- `make_filelist.py` sorts rows by relative path before writing. Without this,
  `os.walk` ordering varies by filesystem and identical data would produce a
  different md5 on a different machine, showing a phantom diff in DVC.
- Q3 v2 contains 2800 image rows / 2801 lines including the header. The brief
  states 2801; `new-labels.zip` contributes 1000 images to the existing 1800,
  verified with `find data -type f | wc -l`.
