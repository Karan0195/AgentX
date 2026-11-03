"""
Code Execution Engine for AgentX
Generates Python / Pandas / DuckDB code via LLM, executes in a secure sandbox,
handles self-healing error retries (up to 3 times), and formats outputs into
structured tables and natural-language answers.
"""

import re
import json
import math
import traceback
from typing import Dict, Any, Optional, Tuple, List

import pandas as pd
import numpy as np
import duckdb

from agents.llm_agent import LLMAgent
from utils.data_engine import DataEngine


class CodeExecutionEngine:
    def __init__(self):
        self.llm = LLMAgent()

    def generate_and_execute(
        self,
        df: pd.DataFrame,
        profile: Dict[str, Any],
        query_info: Dict[str, Any],
        history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Main pipeline:
        1. Prompt LLM to generate Python code based on schema profile & query.
        2. Execute code in safe sandbox.
        3. If error occurs, self-heal and retry up to 3 times.
        4. Synthesize plain language answer + structured table/chart.
        """
        history = history or []
        normalized_q = query_info.get("normalized_query", query_info.get("original_query", ""))
        assumptions = query_info.get("stated_assumptions", [])
        language = query_info.get("language", "english")

        # Compact schema summary for LLM prompt
        schema_summary = []
        for col in profile.get("columns", []):
            samples_str = ", ".join(map(str, col.get("sample_values", [])[:3]))
            schema_summary.append(f"- '{col['name']}' ({col['dtype']}): sample values [{samples_str}]")

        sample_rows_preview = json.dumps(profile.get("sample_rows", [])[:3], default=str)

        prompt = f"""
You are the Python/Pandas Code Generator for AgentX, an autonomous data analytics platform.
Given the dataset profile below, write Python code to answer the user's question accurately.

DATASET PROFILE:
Total rows: {profile.get('total_rows')}, Total columns: {profile.get('total_columns')}
Columns:
{chr(10).join(schema_summary)}

Sample Rows (JSON):
{sample_rows_preview}

USER QUESTION:
{normalized_q}

RULES FOR CODE GENERATION:
1. The DataFrame is pre-loaded in memory as variable `df`.
2. Assign your final calculated output to a variable named `result`.
3. `result` can be:
   - A single scalar value (e.g. `result = float(df['salary'].mean())` or `result = int(len(df))`)
   - A Pandas DataFrame (e.g. `result = df[df['salary'] > 50000][['name', 'salary']].head(10)`)
   - A grouped aggregation DataFrame (e.g. `result = df.groupby('department')['salary'].mean().round(2).reset_index()`)
   - A dictionary with key 'chart' if the user explicitly asked for a plot/chart.
4. Do not invent columns. Use exact column names from the schema.
5. If searching text, use case-insensitive matching (`.str.contains('...', case=False, na=False)`).
6. Convert numeric columns with `pd.to_numeric(df[col], errors='coerce')` if they might contain strings.
7. Return ONLY executable Python code inside ```python and ``` code fences. Do not include markdown explanations outside the code block.
"""

        current_prompt = prompt
        attempts = 0
        max_retries = 3
        last_error = None
        executed_code = ""
        raw_result = None

        while attempts < max_retries:
            attempts += 1
            llm_response = self.llm.ask(current_prompt)
            code = self.extract_code_from_markdown(llm_response)
            executed_code = code

            success, output, error_msg = self.run_in_sandbox(df, code)

            if success:
                raw_result = output
                break
            else:
                last_error = error_msg
                # Self-healing retry prompt
                current_prompt = f"""
The Python code you generated threw an error during execution on the dataset.
Please fix the code using the schema below.

DATASET COLUMNS:
{', '.join([c['name'] for c in profile.get('columns', [])])}

FAILED CODE:
```python
{code}
```

ERROR TRACEBACK:
{error_msg}

USER QUESTION:
{normalized_q}

Return ONLY the corrected Python code inside ```python and ``` code fences.
"""

        if raw_result is None and last_error:
            # Fallback to direct heuristic or safe message
            return {
                "answer": f"I was unable to complete the calculation after 3 attempts due to an execution error: {last_error}",
                "stated_assumption": "\n".join(assumptions) if assumptions else None,
                "executed_code": executed_code,
                "success": False
            }

        # Format results into structured tables & natural language
        formatted_answer = self.format_execution_result(
            raw_result=raw_result,
            question=query_info.get("original_query", ""),
            assumptions=assumptions,
            language=language
        )

        return DataEngine.sanitize_for_json(formatted_answer)

    @staticmethod
    def extract_code_from_markdown(text: str) -> str:
        """Extract clean Python code from markdown code fences."""
        match = re.search(r"```(?:python)?\s*(.*?)\s*```", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        # Fallback: remove non-code lines
        lines = [l for l in text.splitlines() if not l.startswith("```")]
        return "\n".join(lines).strip()

    @staticmethod
    def run_in_sandbox(df: pd.DataFrame, code: str) -> Tuple[bool, Any, Optional[str]]:
        """
        Execute code within a safe execution sandbox.
        Variables provided: `df`, `pd`, `np`, `duckdb`, `math`, `re`.
        """
        # Block dangerous modules
        forbidden = ["os", "sys", "subprocess", "shutil", "socket", "__import__", "builtins", "open"]
        for f in forbidden:
            if re.search(r"\b" + re.escape(f) + r"\b", code):
                return False, None, f"Execution security error: use of '{f}' is restricted."

        local_vars = {
            "df": df.copy(),
            "pd": pd,
            "np": np,
            "duckdb": duckdb,
            "math": math,
            "re": re,
            "result": None,
        }

        def safe_import(name, *args, **kwargs):
            allowed = {"pandas", "numpy", "math", "re", "duckdb", "json", "datetime", "scipy", "collections", "statistics"}
            base_module = name.split(".")[0]
            if base_module in allowed:
                return __import__(name, *args, **kwargs)
            raise ImportError(f"Import of '{name}' is restricted in sandbox.")

        safe_builtins = {
            "len": len, "range": range, "list": list, "dict": dict, "set": set,
            "int": int, "float": float, "str": str, "round": round, "sum": sum,
            "min": min, "max": max, "abs": abs, "zip": zip, "enumerate": enumerate,
            "sorted": sorted, "print": print, "bool": bool, "isinstance": isinstance,
            "None": None, "True": True, "False": False,
            "__import__": safe_import,
        }

        try:
            exec(code, {"__builtins__": safe_builtins}, local_vars)
            result = local_vars.get("result")
            if result is None:
                # Check if code printed something or modified df
                return False, None, "Code executed but variable `result` was not assigned."
            return True, result, None
        except Exception as e:
            return False, None, f"{type(e).__name__}: {str(e)}\n{traceback.format_exc(limit=2)}"

    def format_execution_result(
        self,
        raw_result: Any,
        question: str,
        assumptions: List[str],
        language: str = "english"
    ) -> Dict[str, Any]:
        """Format the sandbox output into a structured response with 1-3 sentences + table/chart."""
        assumption_text = f" ({', '.join(assumptions)})" if assumptions else ""

        # 1. DataFrame or Series Output
        if isinstance(raw_result, (pd.DataFrame, pd.Series)):
            if isinstance(raw_result, pd.Series):
                df_res = raw_result.reset_index()
                df_res.columns = ["Category", "Value"]
            else:
                df_res = raw_result

            # Format numbers in the DataFrame for display
            clean_df = df_res.copy().fillna("")
            total_records = len(clean_df)
            limit = min(50, total_records)
            display_df = clean_df.head(limit)

            columns = [str(c) for c in display_df.columns]
            rows = display_df.astype(str).values.tolist()

            table_payload = {
                "type": "table",
                "total_records": total_records,
                "displayed_records": limit,
                "columns": columns,
                "rows": rows,
                "message": f"Matching results{assumption_text}: {total_records} record(s)"
            }

            # Generate natural language summary (1-2 sentences)
            if language == "hinglish":
                summary = f"Aapke prashna ke anusar kul {total_records} records mile hain{assumption_text}. Neeche table me poora data diya gaya hai."
            else:
                summary = f"Found {total_records} matching record(s) based on your question{assumption_text}. Detailed results are presented in the table below."

            return {
                "answer": table_payload,
                "summary": summary,
                "type": "table",
                "raw_result": raw_result,
                "success": True
            }

        # 2. Scalar Number Output
        if isinstance(raw_result, (int, float, np.integer, np.floating)):
            val = float(raw_result)
            if math.isnan(val) or math.isinf(val):
                formatted_val = "N/A (No numeric data)"
            elif "percentage" in question.lower() or "percent" in question.lower() or "%" in question:
                formatted_val = f"{val:.2f}%"
            elif any(w in question.lower() for w in ["salary", "revenue", "price", "cost", "turnover", "pay", "ctc"]):
                # Currency formatting
                currency_symbol = "₹" if any(w in question.lower() for w in ["inr", "rupee", "pune", "delhi", "mumbai", "india", "ctc"]) else "$"
                formatted_val = f"{currency_symbol}{val:,.2f}"
            elif val.is_integer():
                formatted_val = f"{int(val):,}"
            else:
                formatted_val = f"{val:,.2f}"

            if language == "hinglish":
                text_ans = f"Aapka calculated parinaam hai: **{formatted_val}**{assumption_text}."
            else:
                text_ans = f"The calculated result is **{formatted_val}**{assumption_text}."

            return {
                "answer": text_ans,
                "summary": text_ans,
                "raw_value": val,
                "type": "scalar",
                "success": True
            }

        # 3. Chart Dictionary
        if isinstance(raw_result, dict) and raw_result.get("type") == "chart":
            return {
                "answer": raw_result,
                "summary": raw_result.get("message", "Generated chart visualization."),
                "raw_result": raw_result,
                "type": "chart",
                "success": True
            }

        # 4. Fallback string representation
        str_val = str(raw_result).strip()
        return {
            "answer": str_val,
            "summary": str_val,
            "raw_result": raw_result,
            "raw_value": raw_result,
            "type": "text",
            "success": True
        }
