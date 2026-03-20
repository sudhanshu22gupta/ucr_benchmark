---
name: autoresearch
description: Optimizes a metric autonomously by iteratively training and evaluating models.
---

Run the training script.
After training, an evaluation metric will be printed. Your goal is to optimize it. Do not touch or change the data loading or evaluation code.

Check with user, which metric to optimize, if multiple metrics are tracked.

## Setup

To set up a new experiment, work with the user to:

1. **Agree on a run tag**: propose a tag based on today's date (e.g. `mar5`). The branch `autoresearch/<tag>` must not already exist — this is a fresh run.
2. **Create the branch**: `git checkout -b autoresearch/<tag>` from current master.
4. **Initialize results.tsv**: Create `results.tsv` with just the header row. The baseline will be recorded after the first run.
5. **Confirm and go**: Confirm setup looks good.

Once you get confirmation, kick off the experimentation.


**What you CAN do:**
- Modify the model training. Everything is fair game: model architecture, optimizer, hyperparameters, training loop, batch size, model size, etc.

**What you CANNOT do:**
- Install new packages or add dependencies. You can only use what's already in `pyproject.toml`.
- Change the data loading or evaluation code. The metric must be computed the same way every time, so do not modify how the validation metric is calculated. You can only change how the model is trained, not how it's evaluated.

**Simplicity criterion**: All else being equal, simpler is better. A small improvement that adds ugly complexity is not worth it. Conversely, removing something and getting equal or better results is a great outcome — that's a simplification win. When evaluating whether to keep a change, weigh the complexity cost against the improvement magnitude. A 0.001 improvement that adds 20 lines of hacky code? Probably not worth it. A 0.001 improvement from deleting code? Definitely keep. An improvement of ~0 but much simpler code? Keep.

**The first run**: Your very first run should always be to establish the baseline, so you will run the training script as is.

## Logging results

When an experiment is done, log it to `results.tsv` (tab-separated, NOT comma-separated — commas break in descriptions).

The TSV has a header row and 4 columns:

```
commit	metric	status	description
```

1. git commit hash (short, 7 chars)
2. metric achieved (e.g. 1.234567) — use 0.000000 for crashes
3. status: `keep`, `discard`, or `crash`
4. short text description of what this experiment tried

## The experiment loop

The experiment runs on a dedicated branch (e.g. `autoresearch/mar5` or `autoresearch/mar5-gpu0`).

LOOP FOREVER:

1. Look at the git state: the current branch/commit we're on
2. Tune the training script with an experimental idea by directly hacking the code.
3. git commit
4. Run the experiment. (redirect everything — do NOT use tee or let output flood your context)
5. Read out the results.
6. If the grep output is empty, the run crashed. Run `tail -n 50 run.log` to read the Python stack trace and attempt a fix. If you can't get things to work after more than a few attempts, give up.
7. Record the results in the tsv (NOTE: do not commit the results.tsv file, leave it untracked by git)
8. If the metric improved, you "advance" the branch, keeping the git commit
9. If the metric is equal or worse, you git reset back to where you started