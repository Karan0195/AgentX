import json
import re
import time

from groq import Groq
from config import GROQ_API_KEY


class LLMAgent:
    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError(
                "Groq API key missing. Check your .env file."
            )

        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = "qwen/qwen3.8-27b"
        self.fallback_models = [
            "qwen/qwen3.8-27b",
            "openai/gpt-oss-20b",
            "openai/gpt-oss-120b",
        ]

    def ask(self, question):
        last_error = None

        for model_name in self.fallback_models:
            try:
                response = self.client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are AgentX, a professional AI data and document analyst. "
                                "Answer clearly, completely, and accurately using provided context. "
                                "Never invent facts or dataset results."
                            ),
                        },
                        {"role": "user", "content": question},
                    ],
                    temperature=0.2,
                    max_tokens=2500,
                )

                msg = response.choices[0].message
                content = (msg.content or "").strip()
                if not content and hasattr(msg, "reasoning") and msg.reasoning:
                    content = msg.reasoning.strip()

                if content:
                    return content
            except Exception as exc:
                last_error = exc
                if "429" in str(exc) or "rate" in str(exc).lower():
                    time.sleep(2.5)
                continue

        if last_error:
            raise last_error

        return (
            "I apologize, but I was unable to generate a response for this query. "
            "Please try rephrasing or asking again."
        )

    def interpret_question(self, question, data):
        columns = [
            {
                "name": str(column),
                "type": str(data[column].dtype),
                "sample_values": [
                    str(value)
                    for value in data[column].dropna().unique()[:5]
                ],
            }
            for column in data.columns
        ]

        prompt = f"""
You are the question-understanding component of AgentX.

Interpret the user's question about the provided dataset.
Do not calculate results. Python will execute calculations.

DATASET:
{json.dumps(columns, ensure_ascii=False)}

USER QUESTION:
{question}

Choose exactly one operation:
mean, median, min, max, sum, count, unique, mode, std,
missing_values, dataset_info, value_counts, correlation,
group_by, filter, summary, general_question,
clarification_needed.

Return one JSON object with these fields:
{{
  "operation": "count",
  "column": null,
  "second_column": null,
  "group_column": null,
  "filter_conditions": [],
  "clarification": null
}}

Each filter condition must have this structure:
{{
  "column": "region",
  "operator": "eq",
  "value": "West"
}}

Allowed filter operators:
eq, ne, gt, gte, lt, lte, contains, in.

INTERPRETATION RULES:

1. Use only exact column names provided in the dataset.
2. Never invent column names, category values, or substitute unrelated columns (e.g. never substitute age if the user asks for package, salary, or attendance).
3. "How many records/orders/students are in this dataset?"
   means operation=count with column=null and no filters.
4. "How many orders are from the West region?"
   means operation=count and a filter condition matching the
   appropriate categorical column to the value West.
5. "How many orders are in each region?"
   means operation=value_counts and column should be the
   region column.
6. "What is the total revenue?"
   means operation=sum and column should be the revenue column.
7. "What is the average revenue?"
   means operation=mean and column should be the revenue column.
8. For "greater than", "less than", "at least", or "at most",
   use gt, lt, gte, or lte respectively.
9. If a question has multiple conditions, return each condition
   separately in filter_conditions.
10. For correlation, identify both numeric columns.
11. For group-by calculations, identify the numeric column and
    group_column. Use the operation group_by.
12. For missing-value questions, use missing_values.
13. For general conversation unrelated to the dataset, use
    general_question.
14. If the question asks about a column or concept not present in the dataset, or if the meaning cannot be identified confidently,
    use clarification_needed and explain what is unclear.
15. Use an empty filter_conditions list when no filtering is
    requested.
16. Return only valid JSON. Do not include Markdown fences.
"""

        response = None
        last_error = None

        for model_name in self.fallback_models:
            try:
                response = self.client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Interpret dataset questions accurately. "
                                "Return a single valid JSON object only."
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0,
                    response_format={"type": "json_object"},
                    max_tokens=1000,
                )
                if response and response.choices and response.choices[0].message.content:
                    break
            except Exception as exc:
                last_error = exc
                if "429" in str(exc) or "rate" in str(exc).lower():
                    time.sleep(2.5)
                continue

        if not response or not response.choices or not response.choices[0].message.content:
            if last_error:
                raise last_error
            raise ValueError("Groq returned an invalid or empty question interpretation.")

        text = response.choices[0].message.content.strip()

        # Handle a response enclosed in Markdown code fences.
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)

        try:
            result = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Groq returned an invalid question interpretation."
            ) from exc

        allowed_operations = {
            "mean",
            "median",
            "min",
            "max",
            "sum",
            "count",
            "unique",
            "mode",
            "std",
            "missing_values",
            "dataset_info",
            "value_counts",
            "correlation",
            "group_by",
            "filter",
            "summary",
            "general_question",
            "clarification_needed",
        }

        operation = result.get("operation")
        if operation not in allowed_operations:
            raise ValueError(
                "Groq returned an unsupported operation."
            )

        # Validate column names against the uploaded dataset.
        valid_columns = {str(column): column for column in data.columns}

        for key in ("column", "second_column", "group_column"):
            value = result.get(key)

            if value is not None:
                if value in valid_columns:
                    result[key] = valid_columns[value]
                else:
                    result[key] = None

        # Validate filter conditions before returning them.
        conditions = result.get("filter_conditions", [])

        if not isinstance(conditions, list):
            conditions = []

        valid_operators = {
            "eq", "ne", "gt", "gte", "lt", "lte",
            "contains", "in",
        }

        validated_conditions = []

        for condition in conditions:
            if not isinstance(condition, dict):
                continue

            column = condition.get("column")
            operator = condition.get("operator")
            value = condition.get("value")

            if column not in valid_columns:
                continue

            if operator not in valid_operators:
                continue

            if value is None:
                continue

            validated_conditions.append({
                "column": valid_columns[column],
                "operator": operator,
                "value": value,
            })

        result["filter_conditions"] = validated_conditions

        if operation == "clarification_needed":
            result["clarification"] = (
                result.get("clarification")
                or "Please clarify the question."
            )

        return result
