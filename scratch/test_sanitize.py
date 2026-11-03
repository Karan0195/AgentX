import sys
from pathlib import Path
sys.path.insert(0, r"C:\Users\karan\Desktop\AgentX")

import math
import numpy as np
import pandas as pd
from utils.data_engine import DataEngine

print("Testing sanitize_for_json:")
test_cases = [
    float('nan'),
    np.nan,
    pd.NA,
    np.float64('nan'),
    {"val": float('nan')},
    {"val": np.nan},
    {"val": pd.NA},
    {"df": pd.DataFrame({"a": [1, np.nan], "b": ["x", None]})},
    {"series": pd.Series([1.0, np.nan])},
    {"critic": {"confidence_score": float('nan')}},
    {"nested": [{"a": np.nan}, {"b": float('inf')}]},
    {"str_nan": "NaN"},
    {"list_nan": [1, 2, np.nan, 4]},
    {"custom_np_obj": np.array([np.nan])[0]}
]

for i, tc in enumerate(test_cases):
    res = DataEngine.sanitize_for_json(tc)
    import json
    try:
        s = json.dumps(res, allow_nan=False)
        print(f"[{i}] PASS: {s}")
    except ValueError as e:
        print(f"[{i}] FAIL with allow_nan=False: {e} -> res was: {res}")
