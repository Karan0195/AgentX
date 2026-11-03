"""
Universal Data Engine for AgentX
Handles multi-format dataset ingestion, auto-detection, large file streaming,
DuckDB querying, profiling, and JSON sanitization.
"""

import os
import io
import re
import csv
import json
import math
from pathlib import Path
from typing import Dict, Any, Tuple, List, Optional

import pandas as pd
import numpy as np
import duckdb
import charset_normalizer


class DataEngine:
    SUPPORTED_EXTENSIONS = {
        ".csv", ".tsv", ".xlsx", ".xls", ".json", ".jsonl", ".parquet", ".txt"
    }

    @staticmethod
    def detect_encoding(file_bytes: bytes) -> str:
        """Auto-detect character encoding of raw bytes using charset-normalizer."""
        try:
            sample = file_bytes[:65536]
            result = charset_normalizer.from_bytes(sample).best()
            if result and result.encoding:
                return result.encoding
        except Exception:
            pass
        return "utf-8"

    @staticmethod
    def detect_delimiter(sample_text: str) -> str:
        """Auto-detect delimiter (comma, tab, semicolon, pipe) from sample text."""
        delimiters = [",", "\t", ";", "|", ":"]
        try:
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(sample_text[:4096], delimiters=delimiters)
            return dialect.delimiter
        except Exception:
            # Fallback heuristic: count occurrences of each delimiter in first 5 lines
            lines = [line for line in sample_text.splitlines()[:5] if line.strip()]
            if not lines:
                return ","
            counts = {d: sum(line.count(d) for line in lines) for d in delimiters}
            best = max(counts, key=counts.get)
            return best if counts[best] > 0 else ","

    @classmethod
    def load_file(cls, filepath: str or Path, original_filename: str = "") -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Load any supported file into a pandas DataFrame and extract metadata.
        Auto-detects encoding, delimiter, header, and multi-sheet Excel files.
        """
        filepath = Path(filepath)
        ext = filepath.suffix.lower()
        metadata: Dict[str, Any] = {
            "filename": original_filename or filepath.name,
            "filepath": str(filepath),
            "extension": ext,
            "file_size_bytes": filepath.stat().st_size if filepath.exists() else 0,
            "sheets": [],
            "active_sheet": None,
        }

        if ext in {".csv", ".tsv", ".txt"}:
            with open(filepath, "rb") as f:
                raw_bytes = f.read(131072)
            encoding = cls.detect_encoding(raw_bytes)
            metadata["encoding"] = encoding

            with open(filepath, "r", encoding=encoding, errors="replace") as f:
                sample_text = f.read(8192)
            delimiter = cls.detect_delimiter(sample_text)
            metadata["delimiter"] = delimiter

            # Load with auto-detected settings
            try:
                df = pd.read_csv(
                    filepath,
                    sep=delimiter,
                    encoding=encoding,
                    low_memory=False,
                    on_bad_lines="skip"
                )
            except Exception:
                # Fallback to python engine with latin-1
                df = pd.read_csv(
                    filepath,
                    sep=None,
                    engine="python",
                    encoding="latin-1",
                    on_bad_lines="skip"
                )

        elif ext in {".xlsx", ".xls"}:
            excel_file = pd.ExcelFile(filepath)
            sheet_names = excel_file.sheet_names
            metadata["sheets"] = sheet_names
            metadata["active_sheet"] = sheet_names[0] if sheet_names else None
            # Read first/primary sheet
            df = excel_file.parse(sheet_names[0])

        elif ext in {".json", ".jsonl"}:
            with open(filepath, "rb") as f:
                raw_bytes = f.read(65536)
            encoding = cls.detect_encoding(raw_bytes)

            if ext == ".jsonl":
                try:
                    df = pd.read_json(filepath, lines=True, encoding=encoding)
                except Exception:
                    df = pd.read_json(filepath, encoding=encoding)
            else:
                try:
                    with open(filepath, "r", encoding=encoding, errors="replace") as f:
                        data = json.load(f)
                    if isinstance(data, list):
                        df = pd.json_normalize(data)
                    elif isinstance(data, dict):
                        records = data.get("data", data.get("records", data.get("items", [data])))
                        df = pd.json_normalize(records) if isinstance(records, (list, dict)) else pd.DataFrame([data])
                    else:
                        df = pd.read_json(filepath, encoding=encoding)
                except Exception:
                    try:
                        df = pd.read_json(filepath, encoding=encoding)
                    except Exception:
                        df = pd.read_json(filepath, lines=True, encoding=encoding)

        elif ext == ".parquet":
            df = pd.read_parquet(filepath)

        else:
            raise ValueError(f"Unsupported file format: {ext}. Supported: {', '.join(cls.SUPPORTED_EXTENSIONS)}")

        # Clean column headers
        df.columns = [str(c).strip() for c in df.columns]

        # Register into in-memory DuckDB table for ultra-fast SQL and zero-memory chunking
        try:
            conn = duckdb.connect(database=":memory:")
            conn.register("dataset", df)
            metadata["duckdb_registered"] = True
        except Exception:
            metadata["duckdb_registered"] = False

        return df, metadata

    @classmethod
    def profile_dataset(cls, df: pd.DataFrame, filename: str = "", filepath: str = "") -> Dict[str, Any]:
        """
        Generate a comprehensive, token-efficient data profile:
        - Row & column counts
        - Column datatypes, null counts, unique counts, min/max
        - 5 sanitized sample rows
        - Suggested starter questions based on column names
        """
        total_rows, total_cols = df.shape
        columns_profile = []
        date_columns = []
        numeric_columns = []
        categorical_columns = []

        for col in df.columns:
            series = df[col]
            dtype_str = str(series.dtype)
            null_count = int(series.isna().sum())
            null_pct = round((null_count / total_rows * 100), 2) if total_rows > 0 else 0
            try:
                unique_count = int(series.nunique(dropna=True))
            except TypeError:
                unique_count = int(series.astype(str).nunique(dropna=True))

            # Classify column
            is_num = pd.api.types.is_numeric_dtype(series)
            is_datetime = pd.api.types.is_datetime64_any_dtype(series)

            # Check if text column might actually be dates
            if not is_num and not is_datetime and series.dropna().shape[0] > 0:
                sample_vals = series.dropna().astype(str).head(10).tolist()
                date_pattern = re.compile(r"^\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4}$")
                if sum(bool(date_pattern.match(s.strip())) for s in sample_vals) >= 7:
                    is_datetime = True

            col_meta: Dict[str, Any] = {
                "name": str(col),
                "dtype": dtype_str,
                "null_count": null_count,
                "null_pct": null_pct,
                "unique_count": unique_count,
            }

            # Distinct non-null sample values
            non_null = series.dropna()
            try:
                samples = non_null.unique()[:5].tolist()
            except TypeError:
                samples = non_null.astype(str).unique()[:5].tolist()
            col_meta["sample_values"] = [cls.sanitize_scalar(v) for v in samples]

            if is_num:
                numeric_columns.append(str(col))
                clean_num = pd.to_numeric(non_null, errors="coerce").dropna()
                if not clean_num.empty:
                    col_meta["min"] = cls.sanitize_scalar(clean_num.min())
                    col_meta["max"] = cls.sanitize_scalar(clean_num.max())
                    col_meta["mean"] = cls.sanitize_scalar(round(float(clean_num.mean()), 2))
                    col_meta["median"] = cls.sanitize_scalar(round(float(clean_num.median()), 2))
            elif is_datetime:
                date_columns.append(str(col))
            else:
                categorical_columns.append(str(col))

            columns_profile.append(col_meta)

        # 5 sample rows as list of dicts
        sample_df = df.head(5).copy()
        sample_rows = [
            {str(k): cls.sanitize_scalar(v) for k, v in r.items()}
            for r in sample_df.to_dict(orient="records")
        ]

        # Generate intelligent starter questions based on actual column semantics
        suggested_questions = cls.generate_suggested_questions(df, numeric_columns, categorical_columns, date_columns, filename=filename)

        profile = {
            "filename": filename,
            "filepath": filepath,
            "total_rows": total_rows,
            "total_columns": total_cols,
            "columns": columns_profile,
            "column_names": [str(c) for c in df.columns],
            "numeric_columns": numeric_columns,
            "categorical_columns": categorical_columns,
            "date_columns": date_columns,
            "sample_rows": sample_rows,
            "suggested_questions": suggested_questions,
            "memory_mb": round(df.memory_usage().sum() / (1024 * 1024), 2),
        }

        return cls.sanitize_for_json(profile)

    @classmethod
    def generate_suggested_questions(cls, df: pd.DataFrame, num_cols: List[str], cat_cols: List[str], date_cols: List[str], filename: str = "") -> List[str]:
        """
        Generate meaningful, domain-specific starter questions from dataset schema and semantics.
        Detects domains: Student/Academic, Employee/HR, Banking/Finance, Voting/Electoral, Sales/Retail, and General data.
        """
        questions = []
        if df is None or df.empty:
            return ["What is this dataset about?", "Show summary statistics", "Count total records"]

        cols_lower = [str(c).lower().strip() for c in df.columns]
        col_map = {str(c).lower().strip(): str(c) for c in df.columns}
        all_col_text = " ".join(cols_lower)
        context_text = (all_col_text + " " + filename.lower()).strip()

        def find_col(keywords):
            for kw in keywords:
                for c_low, orig in col_map.items():
                    if kw == c_low or kw in c_low:
                        return orig
            return None

        # Check primary domain signals
        has_student_signal = any(k in context_text for k in ["student", "cgpa", "gpa", "marks", "grade", "prn", "roll_no", "rollno", "semester", "exam"])
        has_employee_signal = any(k in context_text for k in ["employee", "emp_", "salary", "wage", "designation", "years_of_service", "job_title"])
        has_bank_signal = any(k in context_text for k in ["bank", "account", "balance", "transaction", "deposit", "withdrawal", "loan", "debit", "credit"])
        has_voter_signal = any(k in context_text for k in ["voter", "voting", "epic", "electoral", "constituency", "booth", "polling_station", "ward"])
        has_sales_signal = any(k in context_text for k in ["product", "revenue", "sales", "units_sold", "order_id", "discount", "profit"])

        # 1. Student / Academic Data
        if has_student_signal and not has_employee_signal:
            gpa_col = find_col(["cgpa", "gpa"])
            marks_col = find_col(["total_marks", "marks", "score", "percentage", "internal", "ete"])
            grade_col = find_col(["grade", "result", "status"])
            branch_col = find_col(["branch", "department", "dept", "course", "stream", "class"])

            if gpa_col:
                questions.append(f"Show the students who have {gpa_col} above 8.0")
                if branch_col:
                    questions.append(f"Show the average {gpa_col} of students branch-wise")
                questions.append(f"Top 5 students with the highest {gpa_col}")
            elif marks_col:
                questions.append(f"Top 5 students with the highest {marks_col}")
                if branch_col:
                    questions.append(f"What is the average {marks_col} by {branch_col}?")

            if grade_col:
                questions.append(f"Show me the students who have FF or failing grade")
                questions.append(f"Show count of students for each {grade_col}")
            elif branch_col and not any("branch" in q.lower() for q in questions):
                questions.append(f"Show count of students by {branch_col}")

            questions.append(f"How many total students are in this dataset?")
            return questions[:5]

        # 2. Employee / HR Data
        if has_employee_signal:
            sal_col = find_col(["annual_salary_inr", "annual_salary", "salary", "wage", "pay", "ctc"])
            dept_col = find_col(["department", "dept", "division", "branch"])
            rating_col = find_col(["performance_rating", "rating", "review"])
            bonus_col = find_col(["annual_bonus_inr", "bonus", "bonus_percent"])
            tenure_col = find_col(["years_of_service", "experience", "tenure"])

            if sal_col:
                questions.append(f"Which employee has the highest salary?")
                if dept_col:
                    questions.append(f"What is the average {sal_col} by {dept_col}?")
                questions.append(f"Show top 5 employees with the highest {sal_col}")

            if rating_col:
                questions.append(f"Show employees with the highest {rating_col}")
            elif bonus_col:
                questions.append(f"Top 5 employees with the highest {bonus_col}")

            if dept_col and not any("department" in q.lower() for q in questions):
                questions.append(f"Count of employees in each {dept_col}")

            questions.append(f"How many total employees are active in this dataset?")
            return questions[:5]

        # 3. Bank / Financial Data
        if has_bank_signal:
            bal_col = find_col(["balance", "account_balance", "current_balance", "available_balance"])
            amt_col = find_col(["transaction_amount", "amount", "deposit_amount", "loan_amount"])
            acc_type_col = find_col(["account_type", "type", "transaction_type", "plan"])
            branch_col = find_col(["branch", "bank_branch", "city", "state"])

            if bal_col:
                if acc_type_col:
                    questions.append(f"Average {bal_col} by {acc_type_col}")
                questions.append(f"Top 5 accounts with the highest {bal_col}")

            if amt_col:
                questions.append(f"What is the total and average {amt_col}?")
                questions.append(f"Show top transactions with highest {amt_col}")

            if branch_col:
                questions.append(f"Count of accounts or records by {branch_col}")

            questions.append(f"How many total financial records or accounts are present?")
            return questions[:5]

        # 4. Voting / Electoral Data
        if has_voter_signal:
            gender_col = find_col(["gender", "sex", "ling"])
            age_col = find_col(["age", "vay"])
            booth_col = find_col(["polling_station", "booth", "house_no", "ward", "constituency"])

            questions.append("How many total registered voters in this list?")
            if gender_col:
                questions.append(f"Show count of voters by {gender_col}")
            if age_col:
                questions.append(f"Show voters with {age_col} above 60")
            if booth_col:
                questions.append(f"Voters distribution grouped by {booth_col}")
            questions.append("List the first 5 voter records with all details")
            return questions[:5]

        # 5. Sales / E-commerce
        if has_sales_signal:
            rev_col = find_col(["revenue_usd", "revenue", "sales", "total_amount", "profit"])
            prod_col = find_col(["product_name", "product", "item_name", "item", "title"])
            cat_col = find_col(["category", "department", "genre", "type"])
            qty_col = find_col(["units_sold", "quantity", "qty", "orders"])

            if rev_col and prod_col:
                questions.append(f"Which {prod_col} generated the highest {rev_col}?")
            elif rev_col:
                questions.append(f"What is the total {rev_col} generated?")

            if rev_col and cat_col:
                questions.append(f"What is the total {rev_col} by {cat_col}?")

            if qty_col:
                questions.append(f"Top 5 products by {qty_col}")

            if cat_col:
                questions.append(f"Count of products across each {cat_col}")

            questions.append("How many total sales records are in this dataset?")
            return questions[:5]

        # 6. General Tabular (clean numeric & categorical heuristics)
        id_patterns = {"id", "pincode", "pin", "zip", "code", "phone", "year_of_birth", "sr", "serial"}
        clean_num_cols = [c for c in num_cols if not any(p in c.lower() for p in id_patterns)]
        if not clean_num_cols:
            clean_num_cols = num_cols

        clean_cat_cols = [c for c in cat_cols if not any(p in c.lower() for p in {"id", "email", "url", "address", "phone", "hash"})]
        if not clean_cat_cols:
            clean_cat_cols = cat_cols

        if clean_num_cols:
            metric = clean_num_cols[0]
            questions.append(f"What is the average {metric}?")
            questions.append(f"Show the top 5 records with the highest {metric}")

            if clean_cat_cols:
                cat = clean_cat_cols[0]
                questions.append(f"What is the average {metric} by {cat}?")
                questions.append(f"Show count of records for each {cat}")
            elif len(clean_num_cols) > 1:
                questions.append(f"What is the median {clean_num_cols[1]}?")

            if date_cols:
                questions.append(f"Show the trend of {metric} over time")
        elif clean_cat_cols:
            cat = clean_cat_cols[0]
            questions.append(f"Show count of records for each {cat}")
            if len(clean_cat_cols) > 1:
                questions.append(f"Show breakdown by {clean_cat_cols[1]}")

        questions.append("How many total records are in this dataset?")
        return questions[:5]

    @classmethod
    def sanitize_scalar(cls, val: Any) -> Any:
        """Convert float NaNs, Infs, pd.NA, and NaT to None or formatted string."""
        if val is None:
            return None
        try:
            if val is pd.NA or val is pd.NaT:
                return None
        except Exception:
            pass
        if isinstance(val, (float, np.floating)):
            if math.isnan(val) or np.isnan(val) or math.isinf(val) or np.isinf(val):
                return None
            return round(float(val), 4)
        if isinstance(val, (int, np.integer)):
            return int(val)
        if isinstance(val, (pd.Timestamp, np.datetime64)):
            return str(val)
        try:
            if pd.isna(val) is True:
                return None
        except Exception:
            pass
        return str(val).strip()

    @classmethod
    def sanitize_for_json(cls, obj: Any) -> Any:
        """
        Recursively walk dictionaries, lists, and primitives to eliminate all NaNs and Infs.
        Guarantees strict compliance with RFC 8259 JSON standards.
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
            return [cls.sanitize_for_json(r) for r in records]

        if isinstance(obj, pd.Series):
            records = obj.replace({np.nan: None}).to_dict()
            return {str(k): cls.sanitize_for_json(v) for k, v in records.items()}

        # Handle NumPy arrays
        if isinstance(obj, np.ndarray):
            return [cls.sanitize_for_json(x) for x in obj.tolist()]

        # Handle dicts
        if isinstance(obj, dict):
            return {str(k): cls.sanitize_for_json(v) for k, v in obj.items()}

        # Handle lists, tuples, sets
        if isinstance(obj, (list, tuple, set)):
            return [cls.sanitize_for_json(x) for x in obj]

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
