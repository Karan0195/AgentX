import sys
sys.path.insert(0, r"C:\Users\karan\Desktop\AgentX")

import math
import json
import numpy as np
import pandas as pd
from typing import Any

def sanitize_for_json(obj: Any) -> Any:
    """
    Recursively sanitize any Python object for 100% RFC 8259 JSON compliance.
    Eliminates all NaNs, Infs, pd.NA, pd.NaT, and converts NumPy types to native Python.
    """
    if obj is None:
        return None

    # Handle pandas NA and NaT
    try:
        if obj is pd.NA or obj is pd.NaT:
            return None
    except Exception:
        pass

    # Handle DataFrames and Series
    if isinstance(obj, pd.DataFrame):
        records = obj.replace({np.nan: None}).to_dict(orient="records")
        return [sanitize_for_json(r) for r in records]

    if isinstance(obj, pd.Series):
        records = obj.replace({np.nan: None}).to_dict()
        return {str(k): sanitize_for_json(v) for k, v in records.items()}

    # Handle NumPy arrays
    if isinstance(obj, np.ndarray):
        return [sanitize_for_json(x) for x in obj.tolist()]

    # Handle dicts
    if isinstance(obj, dict):
        return {str(k): sanitize_for_json(v) for k, v in obj.items()}

    # Handle lists, tuples, sets
    if isinstance(obj, (list, tuple, set)):
        return [sanitize_for_json(x) for x in obj]

    # Handle floats / floating numbers
    if isinstance(obj, (float, np.floating)):
        if math.isnan(obj) or np.isnan(obj) or math.isinf(obj) or np.isinf(obj):
            return None
        return round(float(obj), 4)

    # Handle integers
    if isinstance(obj, (int, np.integer)):
        return int(obj)

    # Handle booleans
    if isinstance(obj, (bool, np.bool_)):
        return bool(obj)

    # General check for pandas / numpy isna
    try:
        if pd.isna(obj) is True:
            return None
    except Exception:
        pass

    return obj

test_cases = [
    float('nan'),
    np.nan,
    pd.NA,
    pd.NaT,
    np.float64('nan'),
    float('inf'),
    float('-inf'),
    {"val": float('nan')},
    {"val": np.nan},
    {"val": pd.NA},
    {"val": pd.NaT},
    {"df": pd.DataFrame({"a": [1.0, np.nan], "b": ["x", pd.NA]})},
    {"series": pd.Series([1.0, np.nan, pd.NA])},
    {"critic": {"confidence_score": float('nan')}},
    {"nested": [{"a": np.nan}, {"b": float('inf')}]},
    {"list_nan": [1, 2, np.nan, 4, pd.NA]},
    {"custom_np_obj": np.array([np.nan])[0]}
]

print("Running sanitize tests:")
all_pass = True
for i, tc in enumerate(test_cases):
    res = sanitize_for_json(tc)
    try:
        s = json.dumps(res, allow_nan=False)
        print(f"[{i}] PASS: {s}")
    except Exception as e:
        print(f"[{i}] FAIL: {e}")
        all_pass = False

if all_pass:
    print("\nALL SANITIZATION TESTS PASSED! Strict RFC 8259 JSON compliance guaranteed!")
