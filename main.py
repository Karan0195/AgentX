import sys
from pathlib import Path

_project_dir = Path(__file__).resolve().parent
_venv_python = _project_dir / '.venv' / 'Scripts' / 'python.exe'
_venv_site = _project_dir / '.venv' / 'Lib' / 'site-packages'

if _venv_site.exists() and str(_venv_site) not in sys.path:
    sys.path.insert(0, str(_venv_site))

if __name__ == '__main__' and _venv_python.exists() and Path(sys.executable).resolve() != _venv_python.resolve():
    import subprocess
    sys.exit(subprocess.call([str(_venv_python)] + sys.argv))

from agents.data_agent import DataAgent
from agents.analyst_agent import AnalystAgent
from agents.visualization_agent import VisualizationAgent

print("AgentX Multi-Agent System")
print("-------------------------")

data_agent = DataAgent()
analyst_agent = AnalystAgent()
visualization_agent = VisualizationAgent()

data = data_agent.load_data("data/students_dataset.csv")

if data is not None:
    print("\nDataset loaded successfully!")

    for column in ["Age", "Salary"]:
        print(f"\n{column} Analysis")
        print("----------------")
        print("Mean:", analyst_agent.calculate_mean(data, column))
        print("Median:", analyst_agent.calculate_median(data, column))
        print("Minimum:", analyst_agent.calculate_min(data, column))
        print("Maximum:", analyst_agent.calculate_max(data, column))
        print("Standard Deviation:", analyst_agent.calculate_std(data, column))

    correlation = analyst_agent.calculate_correlation(
        data, "Age", "Salary"
    )

    interpretation = analyst_agent.interpret_correlation(correlation)

    print("\nCorrelation Analysis")
    print("--------------------")
    print("Age vs Salary:", correlation)
    print("Interpretation:", interpretation)

    print("\nComplete Column Analysis")
    print("------------------------")

    for column in ["Age", "Salary"]:
        result = analyst_agent.analyze_column(data, column)
        print(f"\n{column}:")
        for key, value in result.items():
            print(f"{key}: {value}")

    print("\nCategorical Analysis")
    print("--------------------")

    result = analyst_agent.analyze_categorical(data, "Name")

    for key, value in result.items():
        print(f"{key}: {value}")

    print("\nColumn Type Detection")
    print("---------------------")

    types = analyst_agent.detect_column_types(data)

    print("Numeric columns:", types["numeric_columns"])
    print("Categorical columns:", types["categorical_columns"])



    print("\nAutomatic Dataset Analysis")
    print("--------------------------")

    results = analyst_agent.analyze_dataset(data)

    print("\nNumerical Analysis:")
    for column, result in results["numeric_analysis"].items():
        print(f"\n{column}:")
        for key, value in result.items():
            print(f"{key}: {value}")

    print("\nCategorical Analysis:")
    for column, result in results["categorical_analysis"].items():
        print(f"\n{column}:")
        for key, value in result.items():
            print(f"{key}: {value}")

    print("\nGenerated Insights")
    print("------------------")

    insights = analyst_agent.generate_insights(data)

    for insight in insights:
        print("-", insight)

    print("\nHigh Salary Detection")
    print("---------------------")

    high_values = analyst_agent.find_high_values(data, "Salary")
    print(high_values)

    print("\nLow Salary Detection")
    print("--------------------")

    low_values = analyst_agent.find_low_values(data, "Salary")
    print(low_values)


    print("\nData Completeness")
    print("-----------------")

    for column in data.columns:
        percentage = analyst_agent.calculate_percentage(
            data, column
        )
        print(f"{column}: {percentage:.2f}%")

    print("\nMissing Value Analysis")
    print("----------------------")

    missing = analyst_agent.find_missing_columns(data)

    if missing:
        print(missing)
    else:
        print("No missing values found.")  


    print("\nData Quality Score")
    print("------------------")

    quality = analyst_agent.calculate_data_quality(data)
    print(f"Data Quality: {quality}%")  


    print("\nComplete Analysis Report")
    print("------------------------")

    report = analyst_agent.generate_analysis_report(data)

    print("Dataset Shape:", report["dataset_shape"])
    print("Data Quality:", report["data_quality"])
    print("Insights:")

    for insight in report["insights"]:
        print("-", insight)    

    print("\nUser Request Planning")
    print("---------------------")

    question = "What is the average salary?"
    task = analyst_agent.plan_analysis(question)

    print("User question:", question)
    print("Planned task:", task)   

    print("\nAgentX Task Execution")
    print("---------------------")

    question = "What is the average salary?"
    result = analyst_agent.execute_analysis(data, question)

    print("Question:", question)
    print("Task:", result["task"])
    print("Result:", result["result"])   



    print("\nColumn Extraction Test")
    print("----------------------")

    question = "What is the average Salary?"
    column = analyst_agent.extract_column(data, question)

    print("User question:", question)
    print("Detected column:", column)                      




    print("\nAgentX Question Answering")
    print("-------------------------")

    question = "What is the average Salary?"
    answer = analyst_agent.answer_data_question(data, question)

    print("Question:", question)
    print("Answer:", answer)

    print("\nCategorical Question Test")
    print("-------------------------")

    question = "Show the most frequent Name"
    answer = analyst_agent.answer_data_question(data, question)

    print("Question:", question)
    print("Answer:", answer)

    print("\nQuestion Understanding Test")
    print("---------------------------")

    questions = [
        "What is the avg Salary?",
        "Find the highest Age",
        "What is the smallest Salary?",
        "Show the mode of Name"
    ]

    for question in questions:
        task = analyst_agent.plan_analysis(question)
        print(f"Question: {question}")
        print(f"Detected task: {task}\n")        

    question = "How many rows and columns are in the dataset?"
    answer = analyst_agent.answer_data_question(data, question)

    print("\nDataset Information")
    print("-------------------")
    print(answer)     

    print("\nDataset Information:")
    print(analyst_agent.answer_data_question(
        data, "How many rows and columns are there?"
    ))       

    print("\nWelcome to AgentX!")
    print("You can ask questions about your dataset.")
    print("\nChart Recommendations:")
    charts = visualization_agent.recommend_charts(data)

    for chart in charts:
        print("\nGenerating charts:")

    for column in ["Age", "Salary", "Name"]:
        chart_path = visualization_agent.generate_chart(data, column)
        print(f"{column} chart saved at: {chart_path}")        
        print(
            f"{chart['column']}: {chart['chart']} "
            f"- {chart['reason']}"
        )    
    print("Type 'exit' to stop.")

    while True:
        question = input("\nAsk AgentX: ")

        if question.lower() == "exit":
            print("AgentX: Goodbye!")
            break

        answer = analyst_agent.answer_data_question(data, question)
        formatted_answer = analyst_agent.format_answer(answer)
        print("AgentX:", formatted_answer)