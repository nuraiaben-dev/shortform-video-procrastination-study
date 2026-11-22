"""Shared helpers used by the analysis and the aggregation benchmark."""

import numpy as np
import pandas as pd


def add_late_tasks(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Add the day-level late-task count L_day.

    The diary records, for every day, how many tasks were planned and how
    many were completed on time. A task that is not completed by its
    deadline is late (submitted late) or missed (not submitted), and the
    protocol counts both as late tasks:

        L_day = max(tasks_planned - tasks_completed, 0)

    Returns a copy; the input frame is not modified.
    """
    col = cfg["columns"]
    out = df.copy()
    unfinished = out[col["tasks_due"]] - out[col["tasks_completed"]]
    out[col["late_tasks"]] = unfinished.clip(lower=0)
    return out
