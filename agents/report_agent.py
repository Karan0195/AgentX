"""
ReportAgent: Executive Reporting and Export Agent for AgentX.
Generates comprehensive dataset intelligence reports, executive summaries,
and downloadable HTML / CSV documentation.
"""

import json
import pandas as pd


class ReportAgent:
    def __init__(self):
        self.name = "Report Agent"

    def get_status(self):
        return "Report Agent is ready to generate intelligence reports."

    def generate_dataset_summary(self, data):
        """Generate structured dataset statistics for reporting."""
        total_rows, total_cols = data.shape
        missing_cells = int(data.isnull().sum().sum())
        total_cells = total_rows * total_cols
        data_quality_pct = round(((total_cells - missing_cells) / total_cells * 100), 2) if total_cells else 0.0
        duplicate_rows = int(data.dropna(how="all").duplicated().sum())

        numeric_summary = {}
        for col in data.select_dtypes(include="number").columns:
            series = pd.to_numeric(data[col], errors="coerce").dropna()
            if not series.empty:
                numeric_summary[str(col)] = {
                    "mean": round(float(series.mean()), 2),
                    "median": round(float(series.median()), 2),
                    "std": round(float(series.std()), 2) if len(series) > 1 else 0.0,
                    "min": round(float(series.min()), 2),
                    "max": round(float(series.max()), 2),
                    "valid_count": int(series.count()),
                }

        categorical_summary = {}
        for col in data.select_dtypes(exclude="number").columns:
            series = data[col].dropna().astype(str).str.strip()
            if not series.empty:
                val_counts = series.value_counts().head(5).to_dict()
                modes = series.mode()
                categorical_summary[str(col)] = {
                    "unique_values": int(series.nunique()),
                    "most_frequent": modes.iloc[0] if not modes.empty else "N/A",
                    "top_categories": {str(k): int(v) for k, v in val_counts.items()},
                }

        return {
            "total_rows": total_rows,
            "total_columns": total_cols,
            "data_quality_score": data_quality_pct,
            "missing_cells": missing_cells,
            "duplicate_rows": duplicate_rows,
            "numeric_metrics": numeric_summary,
            "categorical_metrics": categorical_summary,
            "columns": [str(c) for c in data.columns],
        }

    def generate_html_report(self, data, filename="Dataset", history=None):
        """Generate an executive, professional HTML report ready for printing or viewing."""
        summary = self.generate_dataset_summary(data)

        # Build numeric table rows
        num_rows_html = ""
        for col, metrics in summary["numeric_metrics"].items():
            num_rows_html += f"""
            <tr>
                <td><strong>{col}</strong></td>
                <td>{metrics['mean']}</td>
                <td>{metrics['median']}</td>
                <td>{metrics['min']}</td>
                <td>{metrics['max']}</td>
                <td>{metrics['std']}</td>
                <td>{metrics['valid_count']}</td>
            </tr>
            """

        if not num_rows_html:
            num_rows_html = "<tr><td colspan='7'>No numeric columns detected in this dataset.</td></tr>"

        # Build categorical list
        cat_html = ""
        for col, metrics in summary["categorical_metrics"].items():
            top_items = ", ".join([f"{k} ({v})" for k, v in metrics['top_categories'].items()])
            cat_html += f"""
            <div class="cat-card">
                <h4>{col}</h4>
                <p><strong>Unique values:</strong> {metrics['unique_values']} | <strong>Mode:</strong> {metrics['most_frequent']}</p>
                <p class="small">Top distributions: {top_items}</p>
            </div>
            """

        if not cat_html:
            cat_html = "<p>No categorical columns detected.</p>"

        # Build Q&A History section
        history_html = ""
        if history and isinstance(history, list):
            history_rows = ""
            for item in history:
                q = item.get("question", "")
                ans = item.get("answer", "")
                if isinstance(ans, dict) and "message" in ans:
                    ans = ans["message"]
                history_rows += f"""
                <div class="qa-item">
                    <div class="qa-q">Q: {q}</div>
                    <div class="qa-a">A: {ans}</div>
                </div>
                """
            if history_rows:
                history_html = f"""
                <section class="section">
                    <h2>Session Analysis & Questions</h2>
                    {history_rows}
                </section>
                """

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AgentX Executive Report — {filename}</title>
<style>
    body {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        color: #222;
        background: #f8fafc;
        margin: 0;
        padding: 40px 20px;
        line-height: 1.6;
    }}
    .report-container {{
        max-width: 900px;
        margin: 0 auto;
        background: #fff;
        padding: 45px 50px;
        border-radius: 12px;
        box-shadow: 0 4px 25px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
    }}
    .header {{
        border-bottom: 2px solid #8e67ff;
        padding-bottom: 20px;
        margin-bottom: 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .header h1 {{ margin: 0; font-size: 26px; color: #1e1b4b; }}
    .badge {{
        background: #8e67ff;
        color: #fff;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }}
    .stats-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        margin-bottom: 35px;
    }}
    .stat-box {{
        background: #f1f5f9;
        padding: 16px;
        border-radius: 8px;
        text-align: center;
    }}
    .stat-val {{ font-size: 22px; font-weight: 700; color: #4338ca; }}
    .stat-lbl {{ font-size: 11px; color: #64748b; text-transform: uppercase; margin-top: 4px; }}
    .section {{ margin-bottom: 35px; }}
    .section h2 {{ font-size: 18px; border-bottom: 1px solid #cbd5e1; padding-bottom: 8px; color: #1e293b; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 13px; }}
    th, td {{ padding: 10px 12px; border-bottom: 1px solid #e2e8f0; text-align: left; }}
    th {{ background: #f8fafc; color: #475569; font-weight: 600; }}
    .cat-card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px 16px; margin-bottom: 10px; }}
    .cat-card h4 {{ margin: 0 0 5px 0; color: #334155; }}
    .cat-card p {{ margin: 0; font-size: 12px; color: #64748b; }}
    .small {{ font-size: 11px !important; color: #94a3b8; }}
    .qa-item {{ background: #f8fafc; padding: 12px 16px; border-left: 3px solid #8e67ff; margin-bottom: 12px; border-radius: 0 6px 6px 0; }}
    .qa-q {{ font-weight: 600; color: #1e1b4b; font-size: 13px; margin-bottom: 4px; }}
    .qa-a {{ color: #334155; font-size: 13px; white-space: pre-wrap; }}
    .footer {{ margin-top: 40px; text-align: center; font-size: 11px; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 20px; }}
    @media print {{
        body {{ background: #fff; padding: 0; }}
        .report-container {{ box-shadow: none; border: none; padding: 20px; }}
    }}
</style>
</head>
<body>
<div class="report-container">
    <div class="header">
        <div>
            <h1>AgentX Executive Intelligence Report</h1>
            <p style="margin:4px 0 0; color:#64748b; font-size:13px;">File: {filename}</p>
        </div>
        <div class="badge">AGENTX CERTIFIED</div>
    </div>

    <div class="stats-grid">
        <div class="stat-box">
            <div class="stat-val">{summary['total_rows']:,}</div>
            <div class="stat-lbl">Total Records</div>
        </div>
        <div class="stat-box">
            <div class="stat-val">{summary['total_columns']}</div>
            <div class="stat-lbl">Total Attributes</div>
        </div>
        <div class="stat-box">
            <div class="stat-val">{summary['data_quality_score']}%</div>
            <div class="stat-lbl">Data Health Index</div>
        </div>
        <div class="stat-box">
            <div class="stat-val">{summary['duplicate_rows']}</div>
            <div class="stat-lbl">Duplicate Rows</div>
        </div>
    </div>

    <section class="section">
        <h2>Numeric Column Statistics</h2>
        <table>
            <thead>
                <tr>
                    <th>Column</th>
                    <th>Mean</th>
                    <th>Median</th>
                    <th>Min</th>
                    <th>Max</th>
                    <th>Std Dev</th>
                    <th>Count</th>
                </tr>
            </thead>
            <tbody>
                {num_rows_html}
            </tbody>
        </table>
    </section>

    <section class="section">
        <h2>Categorical Overview</h2>
        {cat_html}
    </section>

    {history_html}

    <div class="footer">
        Generated by AgentX Autonomous Multi-Agent AI System · Final-Year B.Tech AI & Data Science
    </div>
</div>
</body>
</html>
"""
        return html_content


if __name__ == "__main__":
    agent = ReportAgent()
    print(agent.get_status())
