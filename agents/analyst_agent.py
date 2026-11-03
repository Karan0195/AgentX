import json
import re
import pandas as pd
from agents.llm_agent import LLMAgent
class AnalystAgent:
    def generate_data_quality_report(self, data):
        """Check dataset quality without modifying the original data."""
        if data is None:
            return "No dataset is available for quality checking."
        total_rows = len(data)
        total_columns = len(data.columns)
        # Completely blank rows.
        blank_rows = int(data.isna().all(axis=1).sum())
        # Rows containing at least one non-missing value.
        non_empty_rows = total_rows - blank_rows
        # Duplicate rows, excluding completely blank rows.
        non_empty_data = data.dropna(how="all")
        duplicate_rows = int(
            non_empty_data.duplicated().sum()
        )
        # Missing values by column.
        missing_values = data.isna().sum()
        missing_values = missing_values[missing_values > 0]
        # Identify columns that look like record identifiers.
        id_columns = [
            col for col in data.columns
            if (
                str(col).strip().casefold() == "id"
                or str(col).strip().casefold().endswith("_id")
                or str(col).strip().casefold().endswith(" id")
            )
        ]
        id_issues = []
        for col in id_columns:
            values = non_empty_data[col].astype("string").str.strip()
            valid_values = values[values.notna() & values.ne("")]
            duplicate_ids = int(valid_values.duplicated().sum())
            missing_ids = int(
                (values.isna() | values.eq("")).sum()
            )
            if duplicate_ids or missing_ids:
                id_issues.append(
                    f"- {col}: {duplicate_ids} duplicate ID entries, "
                    f"{missing_ids} missing ID entries"
                )
        # Check numeric-looking columns only.
        # Ordinary text columns should not be flagged as errors.
        numeric_issues = []
        numeric_keywords = (
            "age", "percentage", "percent", "cgpa",
            "salary", "revenue", "price", "amount",
            "count", "quantity", "units", "year",
            "semester", "score", "marks", "package",
            "attendance", "backlogs", "internships",
            "projects", "hours", "weight", "height"
        )
        for col in data.columns:
            column_name = str(col).strip().casefold()
            # Skip identifiers because they may contain text.
            if (
                column_name == "id"
                or column_name.endswith("_id")
                or column_name.endswith(" id")
            ):
                continue
            # Check columns whose names suggest numeric values.
            if not any(
                keyword in column_name
                for keyword in numeric_keywords
            ):
                continue
            values = data[col].dropna().astype("string").str.strip()
            values = values[values.ne("")]
            if values.empty:
                continue
            converted = pd.to_numeric(values, errors="coerce")
            invalid_count = int(converted.isna().sum())
            if invalid_count:
                numeric_issues.append(
                    f"- {col}: {invalid_count} values "
                    "are not numeric"
                )
        lines = [
            "DATA QUALITY REPORT",
            "=" * 40,
            f"Total rows: {total_rows}",
            f"Total columns: {total_columns}",
            f"Completely blank rows: {blank_rows}",
            f"Non-empty rows: {non_empty_rows}",
            f"Duplicate non-empty rows: {duplicate_rows}",
            "",
            "MISSING VALUES",
        ]
        if missing_values.empty:
            lines.append("No missing values detected.")
        else:
            for col, count in missing_values.items():
                lines.append(f"- {col}: {int(count)}")
        lines.append("")
        lines.append("POTENTIAL ID ISSUES")
        if id_issues:
            lines.extend(id_issues)
        else:
            lines.append(
                "No issues detected in recognized ID columns."
            )
        lines.append("")
        lines.append("POTENTIAL NON-NUMERIC VALUES")
        if numeric_issues:
            lines.extend(numeric_issues)
        else:
            lines.append(
                "No invalid numeric values detected "
                "in columns identified as numeric."
            )
        lines.append("")
        lines.append(
            "Note: These checks flag potential issues. "
            "They do not modify or delete dataset records."
        )
        return "\n".join(lines)
    def __init__(self):
        self.name = "Analyst Agent"
        self.llm_agent = LLMAgent()
    def get_status(self):
        return "Analyst Agent is ready."
    # ---------------- BASIC STATISTICS ----------------
    def calculate_mean(self, data, column):
        return data[column].mean()
    def calculate_min(self, data, column):
        return data[column].min()
    def calculate_max(self, data, column):
        return data[column].max()
    def calculate_median(self, data, column):
        return data[column].median()
    def calculate_std(self, data, column):
        return data[column].std()
    def calculate_correlation(self, data, column1, column2):
        return data[column1].corr(data[column2])
    def interpret_correlation(self, correlation):
        if correlation > 0.7:
            return "Strong positive correlation"
        elif correlation > 0.3:
            return "Moderate positive correlation"
        elif correlation < -0.7:
            return "Strong negative correlation"
        elif correlation < -0.3:
            return "Moderate negative correlation"
        return "Weak or no correlation"
    def analyze_column(self, data, column):
        return {
            "column": column,
            "mean": self.calculate_mean(data, column),
            "median": self.calculate_median(data, column),
            "minimum": self.calculate_min(data, column),
            "maximum": self.calculate_max(data, column),
            "standard_deviation": self.calculate_std(data, column),
        }
    def analyze_categorical(self, data, column):
        modes = data[column].mode()
        return {
            "unique_values": int(data[column].nunique()),
            "most_frequent": (
                modes.iloc[0] if not modes.empty else None
            ),
            "value_counts": data[column].value_counts().to_dict(),
        }
    def detect_column_types(self, data):
        numeric = list(data.select_dtypes(include="number").columns)
        categorical = list(
            data.select_dtypes(
                include=["object", "category", "string", "bool"]
            ).columns
        )
        return {
            "numeric_columns": numeric,
            "categorical_columns": categorical,
        }
    def analyze_dataset(self, data):
        column_types = self.detect_column_types(data)
        results = {
            "numeric_analysis": {},
            "categorical_analysis": {},
        }
        for column in column_types["numeric_columns"]:
            results["numeric_analysis"][column] = (
                self.analyze_column(data, column)
            )
        for column in column_types["categorical_columns"]:
            results["categorical_analysis"][column] = (
                self.analyze_categorical(data, column)
            )
        return results
    def generate_insights(self, data):
        insights = []
        for column in data.select_dtypes(include="number").columns:
            series = data[column].dropna()
            if series.empty:
                continue
            insights.append(
                f"{column}: Average is {series.mean():.2f}, "
                f"minimum is {series.min()}, "
                f"maximum is {series.max()}."
            )
        return insights
    def find_high_values(self, data, column):
        return data[data[column] > data[column].mean()][[column]]
    def find_low_values(self, data, column):
        return data[data[column] < data[column].mean()][[column]]
    def calculate_percentage(self, data, column):
        if len(data) == 0:
            return 0
        return (data[column].count() / len(data)) * 100
    def find_missing_columns(self, data):
        missing = data.isnull().sum()
        return missing[missing > 0].to_dict()
    def calculate_data_quality(self, data):
        if data.size == 0:
            return 0
        missing_cells = data.isnull().sum().sum()
        quality = ((data.size - missing_cells) / data.size) * 100
        return round(quality, 2)
    def generate_analysis_report(self, data):
        return {
            "dataset_shape": data.shape,
            "column_types": self.detect_column_types(data),
            "statistics": self.analyze_dataset(data),
            "insights": self.generate_insights(data),
            "data_quality": self.calculate_data_quality(data),
            "missing_values": self.find_missing_columns(data),
        }
    # ---------------- QUESTION HELPERS ----------------
    
    def extract_column(self, data, user_question):
        import re

        question = AnalystAgent.normalize_text(user_question)

        # Match complete column names, not partial words.
        normalized_columns = {
            AnalystAgent.normalize_text(str(column)): column
            for column in data.columns
        }

        # Support common alternative names for dataset columns.
        aliases = {
            "average attendance": "attendance percentage",
            "attendance": "attendance percentage",
            "package": "package lpa",
            "salary package": "package lpa",
            "grade point average": "cgpa",
            "c g p a": "cgpa",
        }

        for alias, target in aliases.items():
            if re.search(r"\b" + re.escape(alias) + r"\b", question):
                question = re.sub(
                    r"\b" + re.escape(alias) + r"\b",
                    target,
                    question,
                )

        # Match the longest column name first.
        for normalized_name in sorted(
            normalized_columns,
            key=len,
            reverse=True,
        ):
            if not normalized_name:
                continue

            pattern = r"\b" + re.escape(normalized_name) + r"\b"

            if re.search(pattern, question):
                return normalized_columns[normalized_name]

        return None

    @staticmethod
    def normalize_text(value):
        return re.sub(
            r"[^a-z0-9]+", " ", str(value).lower()
        ).strip()
    def find_matching_category(self, values, question):
        normalized_question = AnalystAgent.normalize_text(question)
        question_tokens = set(normalized_question.split())
        for value in sorted(
            values,
            key=lambda item: len(str(item)),
            reverse=True,
        ):
            normalized_value = AnalystAgent.normalize_text(value)
            if not normalized_value:
                continue
            if re.search(
                r"\b" + re.escape(normalized_value) + r"\b",
                normalized_question,
            ):
                return value
            tokens = normalized_value.split()
            meaningful_tokens = [
                token for token in tokens
                if token not in {
                    "engineering", "branch", "and", "the"
                }
                and len(token) > 2
            ]
            if meaningful_tokens and all(
                token in question_tokens for token in meaningful_tokens
            ):
                return value
        return None
    def answer_branch_question(self, data, question):
        if "branch" not in data.columns:
            return "The dataset does not contain a branch column."
        question_lower = question.lower()
        asks_for_all_branches = any(
            phrase in question_lower
            for phrase in [
                "each branch",
                "every branch",
                "all branches",
                "by branch",
                "branch wise",
                "branch-wise",
            ]
        )
        count_keywords = [
            "how many",
            "number of",
            "total students",
            "count students",
            "count of students",
            "student count",
        ]
        asks_for_count = any(
            phrase in question_lower for phrase in count_keywords
        )
        if asks_for_all_branches and asks_for_count:
            counts = (
                data["branch"]
                .dropna()
                .astype(str)
                .str.strip()
                .value_counts()
            )
            if counts.empty:
                return "No branch values were found in the dataset."
            counts_df = counts.reset_index()
            counts_df.columns = ["Branch", "Student Count"]
            return json.dumps({
                "type": "table",
                "columns": list(counts_df.columns),
                "rows": counts_df.fillna("").astype(str).values.tolist(),
                "total_records": len(counts_df),
                "displayed_records": len(counts_df),
                "message": f"Student count by branch (Total: {int(counts.sum())}):"
            }, ensure_ascii=False)
        if asks_for_count:
            branch_values = (
                data["branch"].dropna().astype(str).str.strip().unique()
            )
            matched_branch = self.find_matching_category(
                branch_values, question
            )
            if matched_branch is not None:
                count = int(
                    data["branch"]
                    .astype("string")
                    .str.strip()
                    .eq(str(matched_branch))
                    .sum()
                )
                return (
                    f"Number of students in {matched_branch}: {count}"
                )
        if asks_for_all_branches and "cgpa" in question_lower:
            if "cgpa" not in data.columns:
                return "The dataset does not contain a CGPA column."
            result = data.groupby("branch")["cgpa"].mean().round(2).reset_index()
            result.columns = ["Branch", "Average CGPA"]
            return json.dumps({
                "type": "table",
                "columns": list(result.columns),
                "rows": result.fillna("").astype(str).values.tolist(),
                "total_records": len(result),
                "displayed_records": len(result),
                "message": "Average CGPA by Branch:"
            }, ensure_ascii=False)
        return None
    def find_ranked_person(self, data, column, highest=True):
        """Find the person(s) with the highest or lowest value in a numeric column."""
        name_candidates = [
            col for col in data.columns
            if self.normalize_text(col) in {
                "name",
                "student",
                "student name",
                "full name",
                "person name",
                "candidate name",
            }
        ]

        if not name_candidates:
            return (
                "I couldn't find a name column. Available columns: "
                + ", ".join(map(str, data.columns))
            )

        name_column = name_candidates[0]
        values = pd.to_numeric(data[column], errors="coerce")

        valid_mask = (
            values.notna()
            & data[name_column].notna()
            & data[name_column].astype(str).str.strip().ne("")
        )

        valid_values = values[valid_mask]

        if valid_values.empty:
            return f"No valid numeric values found in {column}."

        target_value = valid_values.max() if highest else valid_values.min()
        matching_rows = data.loc[valid_mask & values.eq(target_value)]

        rank_label = "highest" if highest else "lowest"
        people = [
            f"{str(row[name_column]).strip()} "
            f"({column}: {target_value:.2f})"
            for _, row in matching_rows.iterrows()
        ]

        return (
            f"Person(s) with the {rank_label} "
            f"{column}: " + ", ".join(people)
        )

    def find_entity_record(self, data, user_question):
        """Find and display details of a specific person or record in the dataset."""
        question_lower = user_question.lower().strip()
        lookup_triggers = [
            "find", "search for", "search", "details of", "details for",
            "details about", "tell me about", "who is", "information about",
            "info about", "information on", "info on", "profile of",
            "look up", "lookup", "record for", "records for", "show me", "get me"
        ]

        has_trigger = any(
            re.search(r"\b" + re.escape(t) + r"\b", question_lower)
            for t in lookup_triggers
        )
        if not has_trigger:
            return None

        # Do not mistake ranking or aggregation queries for entity lookup
        if any(w in question_lower for w in ["highest", "lowest", "top", "bottom", "average", "mean", "median", "sum", "correlation"]):
            return None

        query = question_lower
        for trigger in sorted(lookup_triggers, key=len, reverse=True):
            query = re.sub(r"\b" + re.escape(trigger) + r"\b", " ", query)

        stopwords = {
            "student", "person", "record", "records", "the", "a", "an",
            "data", "row", "entry", "candidate", "voter", "employee", "customer",
            "please", "can", "you", "about", "for", "in", "of", "with", "id"
        }
        tokens = [
            t for t in re.findall(r"[a-z0-9_-]+", query)
            if t not in stopwords and len(t) > 1
        ]
        if not tokens:
            return None

        search_target = " ".join(tokens)

        search_cols = []
        for col in data.columns:
            col_str = str(col).lower()
            if "id" in col_str or data[col].dtype == "object" or pd.api.types.is_string_dtype(data[col]):
                search_cols.append(col)

        if not search_cols:
            search_cols = list(data.columns)

        matched_indices = []
        for col in search_cols:
            series = data[col].astype(str).str.strip()
            exact_mask = series.str.lower() == search_target
            if exact_mask.any():
                matched_indices.extend(data[exact_mask].index.tolist())
                continue
            sub_mask = series.str.lower().str.contains(
                re.escape(search_target), na=False, regex=True
            )
            if sub_mask.any():
                matched_indices.extend(data[sub_mask].index.tolist())

        if not matched_indices and len(tokens) > 1:
            for token in tokens:
                for col in search_cols:
                    mask = data[col].astype(str).str.lower().str.contains(
                        r"\b" + re.escape(token) + r"\b", na=False, regex=True
                    )
                    if mask.any():
                        matched_indices.extend(data[mask].index.tolist())

        matched_indices = list(dict.fromkeys(matched_indices))
        if not matched_indices:
            return f"No matching record found for '{search_target}' in the dataset."

        matched_data = data.loc[matched_indices]

        disp_limit = min(50, len(matched_data))
        return {
            "type": "table",
            "columns": [str(c) for c in matched_data.columns],
            "rows": matched_data.head(disp_limit).fillna("").astype(str).values.tolist(),
            "total_records": len(matched_data),
            "displayed_records": disp_limit,
            "message": f"Found {len(matched_data)} matching record(s) for '{search_target}':"
        }

    def answer_top_bottom_ranking(self, data, user_question):
        """Handle Top-N and Bottom-N ranking questions (e.g. 'Show top 5 students by CGPA')."""
        question_lower = user_question.lower().strip()
        ranking_match = re.search(
            r"\b(top|bottom|highest|lowest|best|worst)\s*(\d+)?\b",
            question_lower
        )
        if not ranking_match:
            return None

        if any(p in question_lower for p in ["who is", "who has", "who got", "whose", "which student"]):
            return None

        direction = ranking_match.group(1)
        count_str = ranking_match.group(2)
        n = int(count_str) if count_str else 5
        n = max(1, min(n, 50))

        requested_column = self.extract_column(data, user_question)
        if not requested_column:
            return None

        numeric_series = pd.to_numeric(data[requested_column], errors="coerce")
        if numeric_series.dropna().empty:
            return None

        is_ascending = direction in {"bottom", "lowest", "worst"}
        sorted_df = data.assign(_sort_col=numeric_series).sort_values(
            by="_sort_col", ascending=is_ascending, na_position="last"
        ).drop(columns=["_sort_col"])

        result = sorted_df.head(n)
        label = "Lowest" if is_ascending else "Top"
        return {
            "type": "table",
            "columns": [str(c) for c in result.columns],
            "rows": result.fillna("").astype(str).values.tolist(),
            "total_rows": len(result),
            "message": f"Showing {label} {len(result)} records sorted by {requested_column}."
        }

    # ---------------- ANALYSIS PLANNING ----------------
    def plan_analysis(self, user_question):
        question = user_question.lower().strip()
        if question in ["hi", "hello", "hey"]:
            return "greeting"
        if any(word in question for word in ["average", "mean", "avg"]):
            return "calculate_mean"
        if "median" in question:
            return "calculate_median"
        if any(
            word in question
            for word in ["maximum", "highest", "largest", "max"]
        ):
            return "calculate_max"
        if any(
            word in question
            for word in ["minimum", "lowest", "smallest", "min"]
        ):
            return "calculate_min"
        if any(
            word in question
            for word in ["correlation", "relationship", "related"]
        ):
            return "calculate_correlation"
        if any(
            word in question
            for word in ["summary", "analyze", "analysis"]
        ):
            return "analyze_dataset"
        if any(
            word in question
            for word in ["most frequent", "most common", "mode"]
        ):
            return "analyze_categorical"
        if any(
            word in question
            for word in [
                "how many rows",
                "number of rows",
                "row count",
                "how many columns",
                "number of columns",
                "column count",
                "dataset shape",
                "dataset size",
            ]
        ):
            return "dataset_info"
        return "general_question"
    def execute_analysis(self, data, user_question):
        task = self.plan_analysis(user_question)
        if task == "calculate_mean":
            result = data.mean(numeric_only=True).to_dict()
        elif task == "calculate_median":
            result = data.median(numeric_only=True).to_dict()
        elif task == "calculate_max":
            result = data.max(numeric_only=True).to_dict()
        elif task == "calculate_min":
            result = data.min(numeric_only=True).to_dict()
        elif task == "calculate_correlation":
            result = data.corr(numeric_only=True).to_dict()
        elif task == "analyze_dataset":
            result = self.generate_analysis_report(data)
        else:
            result = "This request is not supported yet."
        return {"task": task, "result": result}
    # ---------------- FILTER HELPERS ----------------
    def apply_filters(self, data, filter_conditions):
        """Apply validated filter conditions without changing the original data."""
        filtered_data = data.copy()
        valid_operators = {
            "eq", "ne", "gt", "gte", "lt", "lte", "contains", "in"
        }
        for condition in filter_conditions:
            if not isinstance(condition, dict):
                continue
            filter_column = condition.get("column")
            operator = condition.get("operator")
            value = condition.get("value")
            if filter_column not in filtered_data.columns:
                continue
            if operator not in valid_operators or value is None:
                continue
            series = filtered_data[filter_column]
            try:
                if operator in {"eq", "ne"}:
                    normalized = (
                        series.astype("string")
                        .str.strip()
                        .str.casefold()
                    )
                    target = str(value).strip().casefold()
                    if operator == "eq":
                        mask = normalized == target
                    else:
                        mask = normalized != target
                elif operator in {"gt", "gte", "lt", "lte"}:
                    numeric_series = pd.to_numeric(
                        series, errors="coerce"
                    )
                    numeric_value = float(value)
                    if operator == "gt":
                        mask = numeric_series > numeric_value
                    elif operator == "gte":
                        mask = numeric_series >= numeric_value
                    elif operator == "lt":
                        mask = numeric_series < numeric_value
                    else:
                        mask = numeric_series <= numeric_value
                elif operator == "contains":
                    mask = series.astype("string").str.contains(
                        str(value),
                        case=False,
                        na=False,
                        regex=False,
                    )
                else:  # operator == "in"
                    if not isinstance(value, list):
                        continue
                    allowed_values = {
                        str(item).strip().casefold()
                        for item in value
                    }
                    mask = (
                        series.astype("string")
                        .str.strip()
                        .str.casefold()
                        .isin(allowed_values)
                    )
                filtered_data = filtered_data.loc[
                    mask.fillna(False)
                ]
            except (TypeError, ValueError):
                raise ValueError(
                    f"Could not apply the filter to column "
                    f"'{filter_column}'. Check the condition."
                )
        return filtered_data
    # ---------------- MAIN QUESTION ANSWERING ----------------
    def answer_data_question(self, data, user_question):
        import re
        question_lower = user_question.lower().strip()
        # 1. Show the first N rows of the dataset.
        first_rows_match = re.search(
            r"\b(?:show|display|give|get|list)\s+"
            r"(?:me\s+)?(?:the\s+)?"
            r"(?:first|top)\s+(\d+)\s+rows?\b",
            question_lower
        )
        if first_rows_match:
            n = int(first_rows_match.group(1))
            n = max(1, min(n, 100))
            result = data.head(n)
            return {
                "type": "table",
                "columns": result.columns.tolist(),
                "rows": result.fillna("").astype(str).values.tolist(),
                "total_rows": len(result),
                "message": f"Showing the first {len(result)} rows."
            }
        # Also support requests such as "show first rows"
        # when the user does not specify a number.
        if (
            "first rows" in question_lower
            or "top rows" in question_lower
            or "show all rows" in question_lower
        ):
            result = data.head(5)
            return {
                "type": "table",
                "columns": result.columns.tolist(),
                "rows": result.fillna("").astype(str).values.tolist(),
                "total_rows": len(result),
                "message": f"Showing {len(result)} rows."
            }
        # 1B. Top-N and Bottom-N Rankings (e.g., "top 5 students by CGPA").
        top_n_result = self.answer_top_bottom_ranking(data, user_question)
        if top_n_result is not None:
            return top_n_result

        # 1C. Specific Person or Entity Record Lookup (e.g., "Find Diya Patel", "Details of Aarav").
        entity_result = self.find_entity_record(data, user_question)
        if entity_result is not None:
            return entity_result

        # 2. Count rows, non-empty records, and students safely.
        total_count_phrases = [
            "how many rows are in this dataset",
            "how many rows are in the dataset",
            "how many records are in this dataset",
            "how many records are in the dataset",
            "how many entries are in this dataset",
            "how many items are in this dataset",
            "total number of rows",
            "number of rows",
            "how many rows",
            "row count",
            "total records",
            "total orders",
            "total number of records",
            "total number of orders",
            "how many orders are in this dataset",
            "how many orders are in the dataset",
            "dataset size",
        ]
        is_student_count_question = any(
            phrase in question_lower
            for phrase in [
                "how many students are in this dataset",
                "how many students are in the dataset",
                "total number of students",
                "number of students in the dataset",
                "student count",
            ]
        )
        non_empty_data = data.dropna(how="all")
        if is_student_count_question:
            # Prefer a recognized student ID column.
            id_candidates = [
                col for col in data.columns
                if str(col).strip().casefold()
                in {"student_id", "student id", "studentid"}
            ]
            if id_candidates:
                id_column = id_candidates[0]
                student_ids = (
                    non_empty_data[id_column]
                    .astype("string")
                    .str.strip()
                )
                valid_ids = student_ids[
                    student_ids.notna() & student_ids.ne("")
                ]
                unique_students = int(valid_ids.nunique())
                missing_ids = int(
                    (student_ids.isna() | student_ids.eq("")).sum()
                )
                return (
                    f"Unique students identified by {id_column}: "
                    f"{unique_students}. "
                    f"Non-empty records: {len(non_empty_data)}. "
                    f"Records with missing student IDs: {missing_ids}."
                )
            return (
                f"The dataset contains {len(non_empty_data)} "
                "non-empty records, excluding completely blank rows. "
                "I cannot reliably determine the number of unique "
                "students because no recognized student ID column "
                "was found. Duplicate names may belong to different "
                "students."
            )
        if any(
            phrase in question_lower
            for phrase in total_count_phrases
        ):
            return f"Total number of rows: {len(data)}"
        # 2. Handle branch questions.
        if "branch" in data.columns and "branch" in question_lower:
            branch_answer = self.answer_branch_question(
                data, user_question
            )
            if branch_answer is not None:
                return branch_answer
        # 3. Count placed students.
        if any(
            phrase in question_lower
            for phrase in [
                "how many students are placed",
                "number of placed students",
                "count of placed students",
            ]
        ):
            if "placement_status" not in data.columns:
                return (
                    "The dataset does not contain a "
                    "placement_status column."
                )
            placed_count = (
                data["placement_status"]
                .astype("string")
                .str.strip()
                .str.lower()
                .eq("placed")
                .sum()
            )
            return f"Number of placed students: {int(placed_count)}"
        # 4. Count values above a numeric threshold.
        threshold_match = re.search(
            r"(?:more than|greater than|over)\s+(\d+(?:\.\d+)?)"
            r".*?(?:units sold|units|quantity)",
            question_lower,
        )
        if (
            threshold_match
            and "units_sold" in data.columns
            and any(
                word in question_lower
                for word in ["how many", "count", "number of"]
            )
        ):
            threshold = float(threshold_match.group(1))
            units = pd.to_numeric(data["units_sold"], errors="coerce")
            count = int((units > threshold).sum())
            return (
                f"Number of orders with more than "
                f"{threshold:g} units sold: {count}"
            )
        # 5. Dynamically count records matching a category value.
        count_keywords = [
            "how many",
            "number of",
            "count of",
            "count the",
            "total number of",
        ]
        is_count_question = any(
            keyword in question_lower for keyword in count_keywords
        )
        is_group_question = any(
            phrase in question_lower
            for phrase in [
                "each region", "every region", "all regions",
                "by region", "each category", "every category",
                "all categories", "by category", "each branch",
                "every branch", "all branches", "by branch",
            ]
        )
        is_dataset_total_question = any(
            phrase in question_lower
            for phrase in [
                "in this dataset",
                "in the dataset",
                "in this file",
                "in the file",
                "overall",
            ]
        )
        if (
            is_count_question
            and not is_group_question
            and not is_dataset_total_question
        ):
            categorical_columns = list(
                data.select_dtypes(
                    include=["object", "category", "string", "bool"]
                ).columns
            )
            categorical_columns.sort(
                key=lambda col: (
                    self.normalize_text(str(col))
                    not in self.normalize_text(question_lower),
                    -len(str(col)),
                )
            )
            normalized_question = self.normalize_text(question_lower)
            matched_value = None
            matched_column = None
            for col in categorical_columns:
                values = data[col].dropna().unique()
                for value in sorted(
                    values,
                    key=lambda item: len(str(item)),
                    reverse=True,
                ):
                    normalized_value = self.normalize_text(value)
                    if not normalized_value:
                        continue
                    pattern = r"\b" + re.escape(normalized_value) + r"\b"
                    if re.search(pattern, normalized_question):
                        matched_value = value
                        matched_column = col
                        break
                if matched_column is not None:
                    break
            if matched_column is not None:
                normalized_values = (
                    data[matched_column]
                    .astype("string")
                    .str.strip()
                    .str.casefold()
                )
                count = int(
                    normalized_values.eq(
                        str(matched_value).strip().casefold()
                    ).sum()
                )
                return (
                    f"Number of records where {matched_column} "
                    f"is {matched_value}: {count}"
                )
        
        # 5B. Dynamically count records matching a numeric condition.
            threshold_match = re.search(
                r"\b(greater than or equal to|less than or equal to|"
                r"at least|at most|greater than|more than|higher than|"
                r"less than|lower than|above|below|over|under|"
                r"equal to|equals?|greater than or equal|"
                r"less than or equal)\s+(-?\d+(?:\.\d+)?)",
                question_lower,
            )

            asks_count = any(
                phrase in question_lower
                for phrase in [
                    "how many",
                    "count",
                    "number of",
                    "total students",
                    "total records",
                    "total orders",
                ]
            )

            if asks_count and threshold_match:
                condition_text = threshold_match.group(1)
                threshold = float(threshold_match.group(2))

                # Match a real column name from the uploaded dataset.
                normalized_question = self.normalize_text(question_lower)
                matched_column = None

                columns_by_length = sorted(
                    data.columns,
                    key=lambda col: len(self.normalize_text(col)),
                    reverse=True,
                )

                for candidate in columns_by_length:
                    normalized_column = self.normalize_text(candidate)

                    if not normalized_column:
                        continue

                    if (
                        f" {normalized_column} "
                        in f" {normalized_question} "
                    ):
                        values = pd.to_numeric(
                            data[candidate], errors="coerce"
                        )

                        if values.notna().any():
                            matched_column = candidate
                            break

                if matched_column is not None:
                    if "at least" in condition_text or (
                        "greater than or equal" in condition_text
                    ):
                        operator = ">="
                    elif "at most" in condition_text or (
                        "less than or equal" in condition_text
                    ):
                        operator = "<="
                    elif any(
                        phrase in condition_text
                        for phrase in [
                            "less than", "lower than", "below", "under"
                        ]
                    ):
                        operator = "<"
                    elif any(
                        phrase in condition_text
                        for phrase in ["equal to", "equals", "equal"]
                    ):
                        operator = "=="
                    else:
                        operator = ">"

                    values = pd.to_numeric(
                        data[matched_column], errors="coerce"
                    )

                    comparisons = {
                        ">": values > threshold,
                        "<": values < threshold,
                        ">=": values >= threshold,
                        "<=": values <= threshold,
                        "==": values == threshold,
                    }

                    count = int(comparisons[operator].sum())

                    subject = (
                        "students"
                        if "student" in question_lower
                        else "records"
                    )

                    return (
                        f"Number of {subject} with "
                        f"{matched_column} {operator} {threshold:g}: {count}"
                    )

                # Avoid sending an unsupported numeric count to the LLM.
                return (
                    "I couldn't identify a numeric column in your question. "
                    "Available columns: "
                    + ", ".join(map(str, data.columns))
                )

         # Detect questions asking for the student with the highest or lowest marks.
        asks_for_person = any(
            phrase in question_lower
            for phrase in [
                "which student", "who is the", "who has", "who got",
                "who scored", "whose", "student name", "name of the student",
                "name of student", "give me the name", "highest marks student",
                "lowest marks student", "highest scoring student",
                "lowest scoring student",
            ]
        )
        asks_highest = any(
            phrase in question_lower
            for phrase in [
                "highest", "maximum", "max marks", "top marks",
                "highest marks", "highest score", "highest scoring",
                "highest hsc", "highest ssc", "most marks",
            ]
        )
        asks_lowest = any(
            phrase in question_lower
            for phrase in [
                "lowest", "minimum", "min marks", "lowest marks",
                "lowest score", "lowest scoring", "least marks",
            ]
        )        

        # 5C. Handle common numeric calculations without requiring the LLM.
        requested_column = self.extract_column(data, user_question)
        aggregation = None
        if any(word in question_lower for word in ["average", "mean", "avg"]):
            aggregation = "mean"
        elif any(word in question_lower for word in ["highest", "maximum", "largest", "max"]):
            aggregation = "max"
        elif any(word in question_lower for word in ["lowest", "minimum", "smallest", "min"]):
            aggregation = "min"
        elif "median" in question_lower:
            aggregation = "median"
        elif any(word in question_lower for word in ["total", "sum"]):
            aggregation = "sum"


        # Handle highest/lowest questions that ask for a person's name.
        if (
            asks_for_person
            and (asks_highest or asks_lowest)
            and requested_column is not None
        ):
            return self.find_ranked_person(
                data, requested_column, highest=asks_highest
            )

        if aggregation and requested_column is not None:
            numeric_values = pd.to_numeric(
                data[requested_column], errors="coerce"
            ).dropna()
            if not numeric_values.empty:
                operations = {
                    "mean": numeric_values.mean,
                    "max": numeric_values.max,
                    "min": numeric_values.min,
                    "median": numeric_values.median,
                    "sum": numeric_values.sum,
                }
                result = operations[aggregation]()
                return f"{aggregation.title()} of {requested_column}: {result:,.2f}"
            return f"No valid numeric values were found in {requested_column}."
        if aggregation and requested_column is None:
            agg_match = re.search(
                r"\b(?:average|mean|avg|highest|maximum|max|lowest|minimum|min|median|total|sum)\s+(?:of\s+)?(?:the\s+)?([a-zA-Z0-9_\s]+)",
                question_lower
            )
            if agg_match:
                candidate_word = re.sub(r"[?.,!]", "", agg_match.group(1)).strip()
                if candidate_word and candidate_word not in {"rows", "records", "values", "number", "dataset", "each", "all"}:
                    return (
                        f"I couldn't find the column '{candidate_word}' in your question. "
                        f"Available columns: {', '.join(map(str, data.columns))}"
                    )

        # 6. Ask the LLM to interpret the question.
        try:
            plan = self.llm_agent.interpret_question(
                user_question, data
            )
        except Exception as exc:
            return f"Could not understand the question: {exc}"
        operation = plan.get("operation", "general_question")
        column = plan.get("column")
        second_column = plan.get("second_column")
        group_column = plan.get("group_column")
        # Validate column names returned by the LLM.
        if column not in data.columns:
            column = None
        if second_column not in data.columns:
            second_column = None
        if group_column not in data.columns:
            group_column = None
        # 7. Apply filters.
        try:
            data = self.apply_filters(
                data, plan.get("filter_conditions", [])
            )
        except ValueError as exc:
            return str(exc)
        # 8. General questions.
        if operation == "general_question":
            return self.llm_agent.ask(
                "You are AgentX, a helpful assistant. "
                "The user's dataset has these columns: "
                + ", ".join(map(str, data.columns))
                + ". Answer general questions clearly. "
                "Do not invent dataset statistics. Question: "
                + user_question
            )
        if operation == "clarification_needed":
            return plan.get("clarification") or (
                "Please clarify your question and mention "
                "the column or analysis you want."
            )
        # 9. Dataset information.
        if operation == "dataset_info":
            return (
                f"The dataset contains {data.shape[0]} rows "
                f"and {data.shape[1]} columns. "
                f"Columns: {', '.join(map(str, data.columns))}"
            )
        # 10. Dataset summary.
        if operation == "summary":
            if data.empty:
                return "The dataset has no records to summarize."
            rows, columns = data.shape
            parts = [
                f"Dataset contains {rows:,} records and {columns} columns."
            ]
            metrics = {
                "cgpa": "Average CGPA",
                "ssc_percentage": "Average SSC percentage",
                "hsc_percentage": "Average HSC percentage",
                "attendance_percentage": "Average attendance",
            }
            for col, label in metrics.items():
                if col in data.columns:
                    values = pd.to_numeric(
                        data[col], errors="coerce"
                    ).dropna()
                    if not values.empty:
                        value = values.mean()
                        suffix = "%" if "percentage" in col else ""
                        parts.append(f"{label} is {value:.2f}{suffix}.")
            if "placement_status" in data.columns:
                placement = (
                    data["placement_status"]
                    .dropna()
                    .astype(str)
                    .str.strip()
                    .value_counts()
                )
                if not placement.empty:
                    parts.append("Placement results:")
                    for status, count in placement.items():
                        parts.append(f"{status}: {count}")
            if "branch" in data.columns:
                branches = data["branch"].dropna().value_counts()
                if not branches.empty:
                    parts.append(
                        f"Largest branch is {branches.index[0]} "
                        f"with {branches.iloc[0]} records."
                    )
            missing_count = int(data.isna().sum().sum())
            if missing_count:
                parts.append(f"Total missing values: {missing_count}.")
            else:
                parts.append("No missing values were detected.")
            return "\n".join(parts)
        # 11. Missing values.
        if operation == "missing_values":
            if column:
                return (
                    f"Missing values in {column}: "
                    f"{int(data[column].isna().sum())}"
                )
            missing = data.isna().sum()
            missing = missing[missing > 0]
            return (
                "Missing values by column: "
                + (
                    str(missing.to_dict())
                    if not missing.empty
                    else "No missing values found."
                )
            )
        # 12. Correlation.
        if operation == "correlation":
            if not column or not second_column:
                return (
                    "Please specify two columns to calculate "
                    "their correlation."
                )
            if not (
                pd.api.types.is_numeric_dtype(data[column])
                and pd.api.types.is_numeric_dtype(data[second_column])
            ):
                return "Correlation requires two numeric columns."
            value = data[column].corr(data[second_column])
            if pd.isna(value):
                return (
                    "Correlation could not be calculated "
                    "for these columns."
                )
            return (
                f"Correlation between {column} and {second_column}: "
                f"{value:.4f}"
            )
        # 13. Group a numeric column by a category.
        if operation == "group_by":
            if not column or not group_column:
                return (
                    "Please specify the numeric column and "
                    "the category to group by."
                )
            if column not in data.columns:
                return f"Column '{column}' was not found."
            if group_column not in data.columns:
                return f"Column '{group_column}' was not found."
            if not pd.api.types.is_numeric_dtype(data[column]):
                return f"{column} must be numeric for this analysis."
            if data.empty:
                return "No rows match the requested conditions."
            question_lower = user_question.lower()
            # Select the requested aggregation.
            if any(word in question_lower for word in [
                "total", "sum", "combined", "overall"
            ]):
                aggregation = "sum"
                label = "Total"
            elif any(word in question_lower for word in [
                "average", "mean", "avg"
            ]):
                aggregation = "mean"
                label = "Average"
            elif "count" in question_lower or "number of" in question_lower:
                aggregation = "count"
                label = "Count"
            elif any(word in question_lower for word in [
                "maximum", "highest", "largest"
            ]):
                aggregation = "max"
                label = "Maximum"
            elif any(word in question_lower for word in [
                "minimum", "lowest", "smallest"
            ]):
                aggregation = "min"
                label = "Minimum"
            else:
                # Preserve the existing default behavior.
                aggregation = "mean"
                label = "Average"
            grouped = (
                data.groupby(group_column)[column]
                .agg(aggregation)
                .sort_values(ascending=False)
                .round(2)
            )
            grouped_df = grouped.reset_index()
            grouped_df.columns = [str(group_column), f"{label} {column}"]
            result = {
                "type": "table",
                "total_records": int(len(grouped_df)),
                "displayed_records": int(len(grouped_df)),
                "columns": [str(col) for col in grouped_df.columns],
                "rows": grouped_df.fillna("").astype(str).values.tolist(),
                "message": f"{label} {column} by {group_column}:"
            }
            return json.dumps(result, ensure_ascii=False, default=str)
        # 14. Display filtered rows in a structured format.
        if operation == "filter":
            if data.empty:
                return "No rows match the requested filter conditions."
            max_rows = 50
            displayed_data = data.head(max_rows).copy()
            # Convert missing values to empty strings.
            displayed_data = displayed_data.astype(object).where(
                displayed_data.notna(), ""
            )
            # Return structured JSON for accurate HTML table rendering.
            result = {
                "type": "table",
                "total_records": int(len(data)),
                "displayed_records": int(len(displayed_data)),
                "columns": [str(col) for col in displayed_data.columns],
                "rows": displayed_data.values.tolist(),
            }
            return json.dumps(result, ensure_ascii=False, default=str)
        # 15. Validate the requested column.
        if not column:
            return (
                "I couldn't identify the column confidently. "
                "Please mention one of these columns: "
                + ", ".join(map(str, data.columns))
            )
        # 16. Student ranking questions (post-LLM fallback).
        if asks_for_person and (asks_highest or asks_lowest) and column:
            return self.find_ranked_person(
                data, column, highest=asks_highest
            )

        # Existing numerical calculations.
        if operation in {"mean", "median", "min", "max", "sum", "std"}:
            if not column:
                return (
                    "I couldn't identify the column confidently. "
                    "Please mention one of these columns: "
                    + ", ".join(map(str, data.columns))
                )
            if not pd.api.types.is_numeric_dtype(data[column]):
                return f"{column} is not a numeric column."
            series = pd.to_numeric(
                data[column], errors="coerce"
            ).dropna()
            if series.empty:
                return f"No valid numeric values exist in {column}."
            functions = {
                "mean": series.mean,
                "median": series.median,
                "min": series.min,
                "max": series.max,
                "sum": series.sum,
                "std": series.std,
            }
            result = functions[operation]()
            if operation == "sum" and column == "revenue":
                formatted_result = f"₹{result:,.2f}"
                if any(
                    phrase in question_lower
                    for phrase in [
                        "west region", "region west", "in west"
                    ]
                ):
                    return (
                        f"Total revenue for the West region is "
                        f"{formatted_result}."
                    )
                return f"Total revenue is {formatted_result}."
            return (
                f"{operation.title()} of {column}: "
                f"{result:,.2f}"
            )
        # 17. Count rows or non-missing values.
        if operation == "count":
            if column:
                return (
                    f"Non-missing values in {column}: "
                    f"{int(data[column].count())}"
                )
            return f"Total number of matching rows: {len(data)}"
        # 18. Count unique values.
        if operation == "unique":
            return (
                f"Unique values in {column}: "
                f"{int(data[column].nunique())}"
            )
        # 19. Most frequent value.
        if operation == "mode":
            modes = data[column].mode()
            if modes.empty:
                return f"No mode could be determined for {column}."
            return (
                f"Most frequent value in {column}: {modes.iloc[0]}"
            )
        # 20. Frequency of each value.
        if operation == "value_counts":
            vc = data[column].value_counts(dropna=False).reset_index()
            vc.columns = [str(column), "Count"]
            result = {
                "type": "table",
                "total_records": int(len(vc)),
                "displayed_records": int(len(vc)),
                "columns": [str(c) for c in vc.columns],
                "rows": vc.fillna("Missing").astype(str).values.tolist(),
                "message": f"Value counts for {column}:"
            }
            return json.dumps(result, ensure_ascii=False, default=str)
        return (
            f"The operation '{operation}' is not implemented yet."
        )
    # ---------------- ANSWER FORMATTING ----------------
    def format_answer(self, answer):
        if not isinstance(answer, dict):
            return str(answer)
        task = answer.get("task")
        column = answer.get("column")
        result = answer.get("result")
        if task == "calculate_mean":
            return f"The average {column} is {result}."
        if task == "calculate_median":
            return f"The median of {column} is {result}."
        if task == "calculate_min":
            return f"The minimum {column} is {result}."
        if task == "calculate_max":
            return f"The maximum {column} is {result}."
        if task == "dataset_info":
            return (
                f"The dataset has {answer['rows']} rows "
                f"and {answer['columns']} columns. "
                f"Column names: {', '.join(answer['column_names'])}."
            )
        if task == "analyze_categorical":
            return (
                f"The most frequent value in {column} is "
                f"{result['most_frequent']}."
            )
        return str(answer)
if __name__ == "__main__":
    agent = AnalystAgent()
    print(agent.get_status())
