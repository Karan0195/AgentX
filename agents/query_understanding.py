"""
Query Understanding Agent for AgentX
Handles typo correction, business synonym mapping, Hinglish/multilingual detection,
conversational context resolution, and assumption stating.
"""

import re
from typing import Dict, Any, List, Optional, Tuple


class QueryUnderstandingAgent:
    COMMON_TYPOS = {
        "avrg": "average",
        "avg": "average",
        "mean": "average",
        "salry": "salary",
        "salery": "salary",
        "slary": "salary",
        "employ": "employee",
        "emp": "employee",
        "empid": "employee_id",
        "deprtmnt": "department",
        "depatment": "department",
        "dept": "department",
        "hiest": "highest",
        "catgory": "category",
        "studnts": "students",
        "faild": "fail",
        "fail": "grade FF",
        "failed": "grade FF",
        "temprature": "temperature",
        "devce": "device",
        "pwer": "power",
        "consumtion": "consumption",
        "scor": "score",
        "ratng": "rating",
        "enginering": "engineering",
        "clints": "clients",
        "employ": "employee",
        "higest": "highest",
        "maximum": "highest",
        "max": "highest",
        "lawest": "lowest",
        "min": "lowest",
        "totl": "total",
        "stdnt": "student",
        "perfomance": "performance",
        "attndance": "attendance",
        "cgpa": "cgpa",
        "gpa": "cgpa",
        "pct": "percentage",
        "prcnt": "percentage",
    }

    HINGLISH_MAPPINGS = {
        "sabse jyada": "highest",
        "sabse zyada": "highest",
        "sabse adhik": "highest",
        "sabse bada": "highest amount",
        "sabse mehnga": "most expensive highest price",
        "sabse kam": "lowest",
        "kitne": "count",
        "kitna": "count",
        "kitni": "count",
        "kul": "total",
        "kharcha": "total spent amount sum",
        "kharch": "total spent amount sum",
        "ausat": "average",
        "aayu": "age",
        "mareez": "patient",
        "mareezon": "patients",
        "bacho": "students",
        "batao": "show",
        "dikhao": "show",
        "kiska": "who has",
        "kiske": "who has",
        "kaun": "who",
        "kis": "which",
        "mahilaon": "women female",
        "mahila": "female",
        "auraton": "women female",
        "ladkiyan": "female",
        "purush": "male",
        "ladke": "male",
        "pichle saal": "last year",
        "is saal": "this year",
        "ab sirf": "now only",
        "aur": "and",
    }

    SYNONYM_CLUSTERS = {
        "salary": ["salary", "pay", "ctc", "wages", "income", "compensation", "annual_salary", "package", "stipend", "base_salary", "remuneration"],
        "department": ["department", "dept", "division", "team", "domain", "business_unit", "branch"],
        "date_of_joining": ["date_of_joining", "doj", "joined", "hire_date", "start_date", "hired_on", "joining_date"],
        "employee_id": ["employee_id", "emp_id", "id", "staff_id", "emp_no", "employee_number", "roll_no", "prn"],
        "name": ["name", "employee_name", "student_name", "full_name", "first_name", "customer_name", "patient_name"],
        "city": ["city", "location", "place", "region", "branch_location", "town", "state"],
        "performance": ["performance", "rating", "score", "performance_rating", "review", "evaluation"],
        "age": ["age", "years_old", "dob", "birth_date"],
        "experience": ["experience", "years_experience", "exp", "tenure", "service_years"],
        "status": ["status", "active", "employment_status", "job_status", "result"],
        "revenue": ["revenue", "sales", "total_sales", "turnover", "total_revenue", "order_value", "amount"],
        "marks": ["marks", "score", "total_marks", "grade", "cgpa", "percentage"],
    }

    @classmethod
    def understand_query(cls, raw_question: str, available_columns: List[str], history: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Main query understanding pass.
        Returns:
            - normalized_query: cleaned and expanded question
            - matched_columns: mapped real dataset columns
            - stated_assumptions: 1-line note if ambiguous
            - language: 'english' | 'hinglish' | 'hindi'
            - is_follow_up: boolean flag indicating contextual continuity
        """
        history = history or []
        original = raw_question.strip()
        q_lower = original.lower()

        # 1. Detect language / Hinglish
        is_hinglish = any(re.search(r"\b" + re.escape(h) + r"\b", q_lower) for h in cls.HINGLISH_MAPPINGS.keys())
        detected_language = "hinglish" if is_hinglish else "english"

        # 2. Fix typos and translate Hinglish terms into query keywords
        cleaned_words = []
        for word in re.findall(r"\b[\w'-]+\b", q_lower):
            word_clean = cls.COMMON_TYPOS.get(word, word)
            cleaned_words.append(word_clean)

        normalized_phrase = " ".join(cleaned_words)
        for h_phrase, eng_trans in cls.HINGLISH_MAPPINGS.items():
            normalized_phrase = re.sub(r"\b" + re.escape(h_phrase) + r"\b", eng_trans, normalized_phrase)

        # 3. Context & Follow-Up Resolution
        is_follow_up = False
        resolved_context_query = normalized_phrase

        if history:
            last_turn = history[-1]
            last_q = last_turn.get("question", "")
            last_ans = str(last_turn.get("answer", ""))

            # Check for elliptical follow-ups ("and for women?", "now show only Pune", "what about last year?")
            elliptical_triggers = [
                "and for", "what about", "how about", "now show", "only for",
                "in pune", "for women", "for men", "lowest?", "highest?", "compare"
            ]
            if any(t in normalized_phrase for t in elliptical_triggers) or len(normalized_phrase.split()) <= 4:
                is_follow_up = True
                resolved_context_query = f"{normalized_phrase} [Context: previous query was '{last_q}']"

        # 4. Fuzzy Column Matching
        matched_columns, assumptions = cls.match_columns_to_dataset(normalized_phrase, available_columns)

        return {
            "original_query": original,
            "normalized_query": resolved_context_query,
            "cleaned_query": normalized_phrase,
            "matched_columns": matched_columns,
            "stated_assumptions": assumptions,
            "language": detected_language,
            "is_follow_up": is_follow_up,
        }

    @classmethod
    def match_columns_to_dataset(cls, query: str, available_columns: List[str]) -> Tuple[Dict[str, str], List[str]]:
        """
        Fuzzy match terms in query to actual columns in dataset.
        Returns:
            - mapped_columns: {concept: dataset_column_name}
            - assumptions: list of 1-line assumptions made
        """
        q_lower = query.lower()
        matched = {}
        assumptions = []
        normalized_cols = {cls.normalize_identifier(c): c for c in available_columns}

        # Direct name match
        for norm_col, raw_col in normalized_cols.items():
            if re.search(r"\b" + re.escape(norm_col) + r"\b", q_lower):
                matched[raw_col] = raw_col

        # Synonym cluster match
        for concept, synonyms in cls.SYNONYM_CLUSTERS.items():
            has_concept = any(re.search(r"\b" + re.escape(syn) + r"\b", q_lower) for syn in synonyms)
            if has_concept:
                # Find matching column in dataset
                candidate_cols = []
                for raw_col in available_columns:
                    col_norm = cls.normalize_identifier(raw_col)
                    if any(syn in col_norm for syn in synonyms):
                        candidate_cols.append(raw_col)

                if candidate_cols:
                    # Pick best match
                    chosen = candidate_cols[0]
                    matched[concept] = chosen
                    if len(candidate_cols) > 1:
                        assumptions.append(f"Assuming '{chosen}' for {concept}.")

        return matched, assumptions

    @staticmethod
    def normalize_identifier(text: str) -> str:
        """Normalize column name: remove special chars, lowercase."""
        return re.sub(r"[^a-zA-Z0-9]", "", text).lower()
