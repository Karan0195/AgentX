
import pandas as pd

# Load the same dataset used by AgentX.
file_path = "data/students_dataset.csv"
df = pd.read_csv(file_path)

print("=" * 55)
print("AGENTX DATA ANALYSIS VERIFICATION")
print("=" * 55)

# 1. Total rows and columns
print("\n1. Dataset size")
print("Rows:", len(df))
print("Columns:", len(df.columns))

# 2. Average CGPA
if "cgpa" in df.columns:
    cgpa = pd.to_numeric(df["cgpa"], errors="coerce")
    print("\n2. Average CGPA")
    print("Average:", round(cgpa.mean(), 4))
    print("Valid CGPA values:", int(cgpa.notna().sum()))

# 3. CGPA greater than 8
if "cgpa" in df.columns:
    cgpa = pd.to_numeric(df["cgpa"], errors="coerce")
    print("\n3. Students with CGPA greater than 8")
    print("Count:", int((cgpa > 8).sum()))

# 4. Student with highest CGPA
if "cgpa" in df.columns:
    cgpa = pd.to_numeric(df["cgpa"], errors="coerce")
    max_cgpa = cgpa.max()
    highest = df.loc[cgpa == max_cgpa]

    print("\n4. Highest CGPA")
    print("Highest CGPA:", max_cgpa)

    name_column = next(
        (
            col for col in df.columns
            if str(col).strip().casefold()
            in {"name", "student_name", "student name", "full_name"}
        ),
        None,
    )

    if name_column:
        print("Student name(s):")
        print(highest[[name_column, "cgpa"]].to_string(index=False))
    else:
        print("Student name column not found.")

# 5. Placement counts
if "placement_status" in df.columns:
    placement = df["placement_status"].astype("string").str.strip()

    print("\n5. Placement status counts")
    print(placement.value_counts(dropna=False).to_string())

    placed_count = int(
        placement.str.casefold().eq("placed").sum()
    )
    print("Students marked Placed:", placed_count)

# 6. Attendance below 60%
if "attendance_percentage" in df.columns:
    attendance = pd.to_numeric(
        df["attendance_percentage"], errors="coerce"
    )

    filtered = df.loc[attendance < 60].copy()

    print("\n6. Attendance below 60%")
    print("Matching records:", len(filtered))

    columns_to_show = [
        col for col in [
            "student_id",
            "name",
            "attendance_percentage",
        ]
        if col in filtered.columns
    ]

    print(filtered[columns_to_show].to_string(index=False))

print("\n" + "=" * 55)
print("VERIFICATION COMPLETE")
print("=" * 55)
