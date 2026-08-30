# AI Use Disclosure

**Raghav Iyengar (DA24B020)** · AIOps Module 1

I used Claude (Anthropic) during this assignment. This file records what it was
used for and what was my own work. All code was run, all results were produced,
and all analysis was written on my own machines.

---

## Question 2 — MLflow experiment comparison

1. **Structuring the epoch loop.** I asked how to get per-epoch `train_loss` and
   `val_accuracy` out of scikit-learn's `MLPClassifier`, since a single `.fit()`
   call only exposes a final value. The `warm_start=True` with `max_iter=1`
   pattern came from that conversation. I wrote the sweep itself and chose the
   hyperparameter grid.

2. **Catching a dataset error.** I had initially used `load_digits` while
   tagging the runs as MNIST. This was pointed out on review, and I switched to
   `fetch_openml("mnist_784")` and re-ran all seven experiments. The analysis in
   the write-up is my own, written from my own run results.

---

## Question 3 — DVC data versioning and rollback

1. **AWS and IAM setup.** I had not used AWS before. I used AI assistance to
   work out the account structure — root account lockdown, a separate admin
   user, a bucket-scoped IAM policy, and per-partner access keys rather than a
   shared credential. I created every resource myself in the console.

2. **Debugging a `.gitignore` conflict.** `dvc add` was failing with
   `bad DVC file name ... is git-ignored`, because a `data/` entry left over
   from an earlier step was also hiding the `.dvc` pointer that must be
   committed. I diagnosed this with `git check-ignore -v` after being pointed at
   that command. The versioning steps and the rollback were run by me.

---

## Question 4 — Reproducibility capstone

1. **Scaffolding the training and helper scripts.** `train.py`,
   `prepare_data.py`, `promote.py` and `log_repro_note.py` were drafted with AI
   assistance and then edited by me — in particular the skops serialisation
   fallback, which I added after hitting an `UntrustedTypesFoundException` on
   `MLPClassifier`. The protocol itself (commit order, what to hand over, what
   not to communicate) follows the assignment brief.

2. **Diagnosing the reproduction failures.** When Partner B's environment build
   failed and MLflow artifacts could not be written, I used AI assistance to
   read the tracebacks and narrow the causes — the `pip freeze` over-pinning,
   the Python 3.13 vs 3.14 difference, and the artifact root pointing at a local
   path. The findings are written up in my own words in the README and the
   report.

---

## General

- **Debugging and environment setup.** VirtualBox networking (NAT vs bridged),
  port binding, venv and dependency issues, and MLflow server configuration.
- **LaTeX formatting.** The write-up template and its one-page layout. The
  content of the answers is mine.
- **Not used for:** running any experiment, producing any result, or writing the
  Q1 answer. The Q1 categories were identified from the Lecture 1 slides and the
  mitigation is written in my own words.
