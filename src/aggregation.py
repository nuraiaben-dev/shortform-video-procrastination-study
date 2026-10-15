import pandas as pd


def derive_participant_level_proposed(df, cfg):
    """Aggregate diary data with one groupby operation."""
    col = cfg["columns"]

    # Use the same filtering rule as the baseline.
    data = df.copy()
    data = data[data[col["viewing_minutes"]] >= 0]

    result = (
        data.groupby(col["id"])
        .agg(
            valid_days=(col["viewing_minutes"], "size"),
            sum_viewing=(col["viewing_minutes"], "sum"),
            sum_study=(col["study_time_viewing"], "sum"),
            sum_bedtime=(col["bedtime_viewing"], "sum"),
            P=(col["tuckman_score"], "first"),
            L=(col["late_tasks"], "sum"),
            A=(col["tasks_due"], "sum"),
        )
        .reset_index()
    )

    result["X"] = result["sum_viewing"] / result["valid_days"]
    result["S"] = result["sum_study"] / result["valid_days"]
    result["B"] = result["sum_bedtime"] / result["valid_days"]

    return result
