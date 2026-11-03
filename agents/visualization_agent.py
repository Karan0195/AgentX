import matplotlib.pyplot as plt
import os

class VisualizationAgent:
    def __init__(self):
        self.name = "Visualization Agent"

    def get_status(self):
        return "Visualization Agent is ready."

    def recommend_charts(self, data):
        numeric_columns = data.select_dtypes(
            include="number"
        ).columns.tolist()

        categorical_columns = data.select_dtypes(
            exclude="number"
        ).columns.tolist()

        recommendations = []

        for column in numeric_columns:
            recommendations.append({
                "column": column,
                "chart": "Histogram",
                "reason": "To understand the distribution of values."
            })

        for column in categorical_columns:
            recommendations.append({
                "column": column,
                "chart": "Bar Chart",
                "reason": "To compare the frequency of categories."
            })

        return recommendations   

    def generate_chart(self, data, column):
        os.makedirs("charts", exist_ok=True)

        if column not in data.columns:
            return "Column not found."

        plt.figure(figsize=(8, 5))

        if data[column].dtype.kind in "iuf":
            data[column].dropna().plot(
                kind="hist", bins=10
            )
            plt.xlabel(column)
            plt.ylabel("Frequency")

        else:
            data[column].dropna().astype(str).value_counts().plot(
                kind="bar"
            )
            plt.xlabel(column)
            plt.ylabel("Frequency")

        plt.title(f"Distribution of {column}")
        plt.tight_layout()

        file_path = f"charts/{column}_chart.png"
        plt.savefig(file_path)
        plt.close()

        return file_path



    def generate_grouped_chart(
        self, data, category_column, value_column, aggregation="sum"
    ):
        import os
        import pandas as pd
        import matplotlib.pyplot as plt

        os.makedirs("charts", exist_ok=True)

        # Validate columns
        if category_column not in data.columns:
            return f"Column '{category_column}' not found."

        if value_column not in data.columns:
            return f"Column '{value_column}' not found."

        if data.empty:
            return "No data available to plot."

        if not pd.api.types.is_numeric_dtype(data[value_column]):
            return f"Column '{value_column}' must be numeric."

        if aggregation not in {"sum", "mean", "count", "max", "min"}:
            return "Unsupported aggregation."

        # Calculate grouped values
        grouped = (
            data.groupby(category_column, dropna=False)[value_column]
            .agg(aggregation)
            .sort_values(ascending=False)
        )

        if grouped.empty:
            return "No grouped data available to plot."

        # Create a wider chart for long category names
        figure_width = max(10, min(16, len(grouped) * 1.2))
        fig, ax = plt.subplots(figsize=(figure_width, 6))

        bars = ax.bar(
            range(len(grouped)),
            grouped.values,
            edgecolor="black",
            linewidth=0.7,
        )

        # Chart title and axis labels
        ax.set_title(
            f"{aggregation.title()} of {value_column} by {category_column}",
            fontsize=15,
            pad=18,
        )
        ax.set_xlabel(category_column, fontsize=11, labelpad=10)
        ax.set_ylabel(f"{aggregation.title()} {value_column}", fontsize=11)

        # Keep category labels readable
        category_labels = [
            "Missing" if pd.isna(label) else str(label)
            for label in grouped.index
        ]
        ax.set_xticks(range(len(grouped)))
        ax.set_xticklabels(
            category_labels,
            rotation=40,
            ha="right",
            rotation_mode="anchor",
        )

        # Add numerical labels above each bar
        ax.bar_label(
            bars,
            labels=[
                f"{value:,.2f}" if pd.notna(value) else "N/A"
                for value in grouped.values
            ],
            padding=4,
            fontsize=9,
        )

        # Add space above bars so value labels are not clipped
        max_value = grouped.max()
        min_value = min(0, grouped.min())

        
        # Start the Y-axis at zero so bar heights represent values fairly.
        max_value = grouped.max()

        if pd.notna(max_value) and max_value > 0:
            ax.set_ylim(bottom=0, top=max_value * 1.15)
        elif pd.notna(max_value) and max_value == 0:
            ax.set_ylim(bottom=0, top=1)


        ax.grid(axis="y", linestyle="--", alpha=0.3)
        ax.set_axisbelow(True)

        fig.tight_layout()

        # Create safe filename
        safe_category = "".join(
            c if c.isalnum() or c in "-_" else "_"
            for c in str(category_column)
        )
        safe_value = "".join(
            c if c.isalnum() or c in "-_" else "_"
            for c in str(value_column)
        )

        file_path = (
            f"charts/{safe_value}_by_{safe_category}_{aggregation}.png"
        )

        fig.savefig(file_path, dpi=180, bbox_inches="tight")
        plt.close(fig)

        return file_path



if __name__ == "__main__":
    agent = VisualizationAgent()
    print(agent.get_status())