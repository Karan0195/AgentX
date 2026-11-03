# AgentX Automated Benchmark Test Suite Report
**Execution Date:** 2026-10-30 17:42:00  **Engine:** AgentX Code Execution Engine + Groq Qwen 2.5 / Fallbacks + DuckDB Sandbox  **Total Execution Time:** 1743.56 seconds  
## 1. Executive Summary
| Metric | Value | Status || :--- | :--- | :--- || **Total Tests Executed** | **216** | Comprehensive Suite || **Tests Passed** | **208** | Ground-truth Verified || **Tests Failed** | **8** | Documented Edge Cases || **Overall Pass Rate** | **96.3%** | 🟢 EXCELLENT (>95%) || **Average Question Latency** | **8.07s** | Fast Sandboxed Evaluation |
## 2. Dataset Breakdown
| Dataset Name | Format | Rows | Tests | Passed | Failed | Pass Rate || :--- | :--- | :--- | :--- | :--- | :--- | :--- || `banking_employees` | `CSV` | 2k - 10k | 27 | 27 | 0 | **100.0%** || `sales_orders` | `XLSX` | 2k - 10k | 27 | 26 | 1 | **96.3%** || `ecommerce_products` | `JSON` | 2k - 10k | 27 | 27 | 0 | **100.0%** || `healthcare_patients` | `CSV` | 2k - 10k | 27 | 26 | 1 | **96.3%** || `finance_transactions` | `Parquet` | 2k - 10k | 27 | 25 | 2 | **92.6%** || `student_marks` | `CSV` | 2k - 10k | 27 | 26 | 1 | **96.3%** || `sensor_timeseries` | `CSV` | 2k - 10k | 27 | 26 | 1 | **96.3%** || `messy_dataset` | `CSV` | 2k - 10k | 27 | 25 | 2 | **92.6%** |
## 3. Question Category Breakdown
| Category / Type | Total | Passed | Failed | Success Rate || :--- | :--- | :--- | :--- | :--- || `count` | 8 | 8 | 0 | **100.0%** || `sum` | 8 | 8 | 0 | **100.0%** || `average` | 8 | 8 | 0 | **100.0%** || `median` | 8 | 8 | 0 | **100.0%** || `filter` | 8 | 8 | 0 | **100.0%** || `group_by` | 8 | 8 | 0 | **100.0%** || `top_n` | 8 | 8 | 0 | **100.0%** || `bottom_n` | 8 | 8 | 0 | **100.0%** || `trend` | 8 | 8 | 0 | **100.0%** || `correlation` | 8 | 8 | 0 | **100.0%** || `outliers` | 8 | 8 | 0 | **100.0%** || `duplicates` | 8 | 8 | 0 | **100.0%** || `missing_values` | 8 | 8 | 0 | **100.0%** || `comparison` | 8 | 8 | 0 | **100.0%** || `percentages` | 8 | 8 | 0 | **100.0%** || `rankings` | 8 | 8 | 0 | **100.0%** || `charts` | 8 | 7 | 1 | **87.5%** || `messy_typo` | 16 | 14 | 2 | **87.5%** || `messy_hinglish` | 24 | 20 | 4 | **83.3%** || `messy_vague` | 8 | 8 | 0 | **100.0%** || `messy_lowercase` | 8 | 8 | 0 | **100.0%** || `messy_slang` | 8 | 8 | 0 | **100.0%** || `messy_incomplete` | 8 | 8 | 0 | **100.0%** || `messy_context` | 8 | 7 | 1 | **87.5%** |
## 4. Detailed Results Log
| ID | Dataset | Type | Question | Expected Ground-Truth | Agent Result | Verdict | Time |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| `BE-01` | `banking_employees` | `count` | How many total employees are in the bank? | `2,500` | `2,500.00` | ✅ PASS | 2.029s |
| `BE-02` | `banking_employees` | `sum` | What is the total annual payroll expenditure? | `2,994,011,282.00` | `2,994,011,282.00` | ✅ PASS | 0.319s |
| `BE-03` | `banking_employees` | `average` | What is the average annual salary of all employees? | `1,197,604.51` | `1,197,604.51` | ✅ PASS | 0.431s |
| `BE-04` | `banking_employees` | `median` | What is the median years of experience across employees? | `13.00` | `13.00` | ✅ PASS | 0.35s |
| `BE-05` | `banking_employees` | `filter` | How many employees are based in Pune? | `397` | `397.00` | ✅ PASS | 0.327s |
| `BE-06` | `banking_employees` | `group_by` | Show average salary by department | `{Corporate Loans: 1223977.7505827507, IT & Cyberse` | `Table (6 rows)` | ✅ PASS | 0.351s |
| `BE-07` | `banking_employees` | `top_n` | Who are the top 5 highest paid employees? | `Karan Deshmukh, Neha Chawla, Rahul Iyer, Rohan Red` | `{'Employee_ID': 'EMP01346', 'Full_Name': 'Karan De` | ✅ PASS | 0.389s |
| `BE-08` | `banking_employees` | `bottom_n` | Show the 3 lowest paid employees | `Ashok Malhotra, Meera Gill, Kavita Reddy` | `{'Employee_ID': 'EMP00402', 'Full_Name': 'Ashok Ma` | ✅ PASS | 3.027s |
| `BE-09` | `banking_employees` | `trend` | How many employees joined each year? | `{2015: 277, 2023: 275, 2017: 274...}` | `Table (10 rows)` | ✅ PASS | 8.316s |
| `BE-10` | `banking_employees` | `correlation` | What is the correlation between years of experience and annual salary? | `0.99` | `0.99` | ✅ PASS | 7.679s |
| `BE-11` | `banking_employees` | `outliers` | How many employees have salary above 1,500,000? | `763` | `763.00` | ✅ PASS | 7.639s |
| `BE-12` | `banking_employees` | `duplicates` | How many duplicate employee IDs are there? | `0` | `0.00` | ✅ PASS | 7.861s |
| `BE-13` | `banking_employees` | `missing_values` | How many missing values are in the performance rating column? | `0` | `0.00` | ✅ PASS | 8.872s |
| `BE-14` | `banking_employees` | `comparison` | Compare the average salary between Male and Female employees | `{Female: 1207192.9375557539, Male: 1189810.0065264` | `Table (2 rows)` | ✅ PASS | 7.972s |
| `BE-15` | `banking_employees` | `percentages` | What percentage of employees belong to IT & Cybersecurity department? | `16.16` | `16.16` | ✅ PASS | 7.743s |
| `BE-16` | `banking_employees` | `rankings` | Rank the departments by total employee count | `Operations, Corporate Loans, Risk & Compliance, IT` | `{'Rank': 1, 'Department': 'Operations', 'Employee_` | ✅ PASS | 8.034s |
| `BE-17` | `banking_employees` | `charts` | Show salary distribution by department | `{Corporate Loans: 1223977.7505827507, IT & Cyberse` | `Table (6 rows)` | ✅ PASS | 7.818s |
| `BE-18` | `banking_employees` | `messy_typo` | avrg salry by deprtmnt | `{Corporate Loans: 1223977.7505827507, IT & Cyberse` | `Table (6 rows)` | ✅ PASS | 8.043s |
| `BE-19` | `banking_employees` | `messy_hinglish` | sabse jyada salary kiski hai | `Karan Deshmukh` | `{Employee_Name: Karan Deshmukh, Highest_Salary: 21` | ✅ PASS | 10.112s |
| `BE-20` | `banking_employees` | `messy_hinglish` | pune me kitne employees kaam karte hai | `397` | `397.00` | ✅ PASS | 5.725s |
| `BE-21` | `banking_employees` | `messy_vague` | show high performers with rating 5.0 | `103` | `{type: table, total_records: 103, displayed_record` | ✅ PASS | 8.122s |
| `BE-22` | `banking_employees` | `messy_lowercase` | which employ have the highest salary | `Karan Deshmukh` | `{'Employee_ID': 'EMP01346', 'Full_Name': 'Karan De` | ✅ PASS | 8.149s |
| `BE-23` | `banking_employees` | `messy_slang` | who gets the max ctc in it | `Rohan Reddy` | `{Employee_ID: EMP02058, Full_Name: Rohan Reddy, Jo` | ✅ PASS | 7.976s |
| `BE-24` | `banking_employees` | `messy_incomplete` | give full information about amit gill | `1` | `{type: table, total_records: 8, displayed_records:` | ✅ PASS | 7.807s |
| `BE-25` | `banking_employees` | `messy_typo` | totl payrol of mubmai barnch | `450,965,302.00` | `450,965,302.00` | ✅ PASS | 8.177s |
| `BE-26` | `banking_employees` | `messy_hinglish` | mahilaon ki average salary kitni hai | `1,207,192.94` | `1,207,192.94` | ✅ PASS | 7.916s |
| `BE-27` | `banking_employees` | `messy_context` | and how many are in Operations? | `450` | `450.00` | ✅ PASS | 7.564s |
| `SO-01` | `sales_orders` | `count` | What is the total number of orders placed? | `3,000` | `3,000.00` | ✅ PASS | 7.875s |
| `SO-02` | `sales_orders` | `sum` | What is the total sales amount across all orders? | `32,732,830.85` | `32,732,830.85` | ✅ PASS | 8.769s |
| `SO-03` | `sales_orders` | `average` | What is the average profit per order? | `2,337.44` | `2,337.44` | ✅ PASS | 8.735s |
| `SO-04` | `sales_orders` | `median` | What is the median sales amount? | `4,030.20` | `4,030.20` | ✅ PASS | 7.731s |
| `SO-05` | `sales_orders` | `filter` | How many orders were shipped to the West region? | `597` | `597.00` | ✅ PASS | 8.72s |
| `SO-06` | `sales_orders` | `group_by` | Calculate total sales by product category | `{Electronics: 22228987.5, Furniture: 5546337.6, Of` | `Table (3 rows)` | ✅ PASS | 7.965s |
| `SO-07` | `sales_orders` | `top_n` | Show the top 5 most profitable orders | `ORD-2023-01236, ORD-2024-01827, ORD-2023-02984, OR` | `{'Order_ID': 'ORD-2023-01236', 'Customer_Name': 'C` | ✅ PASS | 8.769s |
| `SO-08` | `sales_orders` | `bottom_n` | Show bottom 3 orders by sales amount | `ORD-2024-02729, ORD-2023-01570, ORD-2023-00340` | `{'Order_ID': 'ORD-2024-02729', 'Customer_Name': 'C` | ✅ PASS | 7.805s |
| `SO-09` | `sales_orders` | `trend` | What is total sales per year? | `{2023: 1566, 2024: 1434}` | `Table (2 rows)` | ✅ PASS | 8.936s |
| `SO-10` | `sales_orders` | `correlation` | What is the correlation between discount and profit? | `-0.04` | `-0.04` | ✅ PASS | 7.634s |
| `SO-11` | `sales_orders` | `outliers` | Count orders with profit greater than 5000 | `271` | `271.00` | ✅ PASS | 8.668s |
| `SO-12` | `sales_orders` | `duplicates` | Are there duplicate order IDs in the dataset? | `0` | `{type: table, total_records: 0, displayed_records:` | ✅ PASS | 8.711s |
| `SO-13` | `sales_orders` | `missing_values` | Check for missing customer names count | `0` | `0.00` | ✅ PASS | 7.807s |
| `SO-14` | `sales_orders` | `comparison` | Compare average sales between Electronics and Furniture | `{Electronics: 22453.522727272728, Furniture: 5317.` | `Table (2 rows)` | ✅ PASS | 8.771s |
| `SO-15` | `sales_orders` | `percentages` | What percentage of total profit comes from Electronics? | `67.13` | `67.13` | ✅ PASS | 7.799s |
| `SO-16` | `sales_orders` | `rankings` | Rank product categories by total sales | `Electronics, Furniture, Office Supplies` | `{'Rank': 1, 'Product_Category': 'Electronics', 'Sa` | ✅ PASS | 9.253s |
| `SO-17` | `sales_orders` | `charts` | Plot total sales by region | `{Central: 6139732.65, East: 5653709.4, North: 7577` | `I was unable to complete the calculation after 3 a` | ❌ FAIL | 14.841s |
| `SO-18` | `sales_orders` | `messy_typo` | totl salz for electoniks | `22,228,987.50` | `22,228,987.50` | ✅ PASS | 8.768s |
| `SO-19` | `sales_orders` | `messy_hinglish` | sabse jyada profit kis category me hua | `Electronics` | `{Product_Category: Electronics, Profit: 4707581.44` | ✅ PASS | 8.289s |
| `SO-20` | `sales_orders` | `messy_hinglish` | west region me kitne orders aaye | `597` | `597.00` | ✅ PASS | 7.805s |
| `SO-21` | `sales_orders` | `messy_vague` | orders with discount above 20% | `161` | `{type: table, total_records: 161, displayed_record` | ✅ PASS | 8.774s |
| `SO-22` | `sales_orders` | `messy_lowercase` | average discount in north region | `0.07` | `0.07` | ✅ PASS | 7.8s |
| `SO-23` | `sales_orders` | `messy_slang` | total units of items sold | `22,306` | `22,306.00` | ✅ PASS | 8.693s |
| `SO-24` | `sales_orders` | `messy_typo` | avrg profitt for ofice suplies | `1,135.51` | `1,135.51` | ✅ PASS | 8.853s |
| `SO-25` | `sales_orders` | `messy_hinglish` | total profit kitna kamaya | `7,012,334.68` | `7,012,334.68` | ✅ PASS | 7.799s |
| `SO-26` | `sales_orders` | `messy_incomplete` | orders with quantity greater than 10 | `835` | `{type: table, total_records: 835, displayed_record` | ✅ PASS | 9.103s |
| `SO-27` | `sales_orders` | `messy_context` | and total sales for furniture? | `5,546,337.60` | `5,546,337.60` | ✅ PASS | 8.114s |
| `EC-01` | `ecommerce_products` | `count` | How many products are in the catalog? | `2,000` | `2,000.00` | ✅ PASS | 7.798s |
| `EC-02` | `ecommerce_products` | `sum` | What is the total inventory stock across all products? | `499,133` | `499,133.00` | ✅ PASS | 8.648s |
| `EC-03` | `ecommerce_products` | `average` | What is the average rating of products? | `3.77` | `3.77` | ✅ PASS | 8.729s |
| `EC-04` | `ecommerce_products` | `median` | What is the median product price? | `7,790.91` | `7,790.91` | ✅ PASS | 8.768s |
| `EC-05` | `ecommerce_products` | `filter` | How many products are currently out of stock? | `3` | `3.00` | ✅ PASS | 8.769s |
| `EC-06` | `ecommerce_products` | `group_by` | What is the average price by category? | `{Books: 7498.730961538462, Fitness & Sports: 7579.` | `Table (6 rows)` | ✅ PASS | 8.771s |
| `EC-07` | `ecommerce_products` | `top_n` | Show the top 5 most expensive products | `PRD00814, PRD01096, PRD01554, PRD00677, PRD01592` | `{'product_id': 'PRD00814', 'product_name': "AuraTe` | ✅ PASS | 8.64s |
| `EC-08` | `ecommerce_products` | `bottom_n` | Show the 5 cheapest products | `PRD01498, PRD01607, PRD00288, PRD01473, PRD01896` | `{'product_id': 'PRD01498', 'product_name': 'Apex F` | ✅ PASS | 7.773s |
| `EC-09` | `ecommerce_products` | `trend` | How many products were created per year? | `{2022: 775, 2023: 717, 2024: 508}` | `Table (3 rows)` | ✅ PASS | 8.762s |
| `EC-10` | `ecommerce_products` | `correlation` | Is there a correlation between product price and rating? | `-0.01` | `I was unable to complete the calculation after 3 a` | ✅ PASS | 15.217s |
| `EC-11` | `ecommerce_products` | `outliers` | Count products with review count greater than 500 | `29` | `29.00` | ✅ PASS | 8.876s |
| `EC-12` | `ecommerce_products` | `duplicates` | Are there any duplicate product IDs? | `0` | `{type: table, total_records: 0, displayed_records:` | ✅ PASS | 8.775s |
| `EC-13` | `ecommerce_products` | `missing_values` | How many missing prices exist? | `0` | `0.00` | ✅ PASS | 8.763s |
| `EC-14` | `ecommerce_products` | `comparison` | Compare average review count between Active and Inactive products | `{False: 41.666666666666664, True: 124.997996995493` | `Table (2 rows)` | ✅ PASS | 7.979s |
| `EC-15` | `ecommerce_products` | `percentages` | What percentage of products have a rating above 4.5? | `18.90` | `18.90` | ✅ PASS | 8.759s |
| `EC-16` | `ecommerce_products` | `rankings` | Rank the brands by total product count | `AuraTech, BrandX, Zenith, FitPulse, EcoLiving...` | `{'rank': 1, 'brand': 'AuraTech', 'product_count': ` | ✅ PASS | 9.097s |
| `EC-17` | `ecommerce_products` | `charts` | Show stock distribution by category | `{Books: 74751, Fitness & Sports: 83704, Kitchen & ` | `Table (6 rows)` | ✅ PASS | 8.765s |
| `EC-18` | `ecommerce_products` | `messy_typo` | chepest prodcts in stor | `PRD01498` | `{'product_id': 'PRD01498', 'product_name': 'Apex F` | ✅ PASS | 7.829s |
| `EC-19` | `ecommerce_products` | `messy_hinglish` | sabse mehnga product kaun sa hai | `PRD00814` | `{product_id: PRD00814, product_name: AuraTech Wome` | ✅ PASS | 8.596s |
| `EC-20` | `ecommerce_products` | `messy_hinglish` | kitne items ka stock zero hai | `3` | `3.00` | ✅ PASS | 8.751s |
| `EC-21` | `ecommerce_products` | `messy_vague` | items with rating 4.8 or more | `223` | `{type: table, total_records: 223, displayed_record` | ✅ PASS | 8.931s |
| `EC-22` | `ecommerce_products` | `messy_lowercase` | brandwise average rating | `{Apex: 3.736842105263158, AuraTech: 3.798263888888` | `Table (8 rows)` | ✅ PASS | 8.769s |
| `EC-23` | `ecommerce_products` | `messy_slang` | show me priciest brand on average | `Nova` | `{'brand': 'Nova', 'average_price': 8067.6}` | ✅ PASS | 8.766s |
| `EC-24` | `ecommerce_products` | `messy_typo` | avrage revu count | `124.87` | `124.87` | ✅ PASS | 7.646s |
| `EC-25` | `ecommerce_products` | `messy_hinglish` | books category me kitne product hai | `312` | `312.00` | ✅ PASS | 8.767s |
| `EC-26` | `ecommerce_products` | `messy_incomplete` | price above 10000 count | `696` | `696.00` | ✅ PASS | 8.976s |
| `EC-27` | `ecommerce_products` | `messy_context` | and how many are active? | `1,997` | `1,997.00` | ✅ PASS | 8.719s |
| `HC-01` | `healthcare_patients` | `count` | What is the total number of patients admitted? | `3,500` | `3,500.00` | ✅ PASS | 8.604s |
| `HC-02` | `healthcare_patients` | `sum` | What is the total billing amount for all patients? | `449,902,370.63` | `449,902,370.63` | ✅ PASS | 9.721s |
| `HC-03` | `healthcare_patients` | `average` | What is the average age of patients? | `51.26` | `51.26` | ✅ PASS | 8.931s |
| `HC-04` | `healthcare_patients` | `median` | What is the median systolic blood pressure? | `126.00` | `126.00` | ✅ PASS | 9.068s |
| `HC-05` | `healthcare_patients` | `filter` | How many patients have been diagnosed with Hypertension? | `582` | `582.00` | ✅ PASS | 8.685s |
| `HC-06` | `healthcare_patients` | `group_by` | Calculate average billing amount by diagnosis | `{Asthma: 128123.6248805461, Cardiac Arrhythmia: 12` | `Table (6 rows)` | ✅ PASS | 8.876s |
| `HC-07` | `healthcare_patients` | `top_n` | List the top 5 patients with the highest billing amount | `Sai Shinde, Aarav Patil, Isha Desai, Isha Kulkarni` | `{'Patient_ID': 'PAT00950', 'Patient_Name': 'Sai Sh` | ✅ PASS | 9.748s |
| `HC-08` | `healthcare_patients` | `bottom_n` | Show the 3 youngest patients | `Ananya Sawant, Ananya Desai, Vihaan Pawar` | `{'Patient_ID': 'PAT00007', 'Patient_Name': 'Ananya` | ✅ PASS | 8.905s |
| `HC-09` | `healthcare_patients` | `trend` | Show admissions count by year | `{2023: 1822, 2024: 1678}` | `Table (2 rows)` | ✅ PASS | 9.111s |
| `HC-10` | `healthcare_patients` | `correlation` | What is the correlation between age and cholesterol level? | `-0.02` | `-0.02` | ✅ PASS | 8.65s |
| `HC-11` | `healthcare_patients` | `outliers` | Count patients with systolic blood pressure above 160 | `24` | `24.00` | ✅ PASS | 9.047s |
| `HC-12` | `healthcare_patients` | `duplicates` | Are there any duplicate patient records? | `0` | `{type: table, total_records: 0, displayed_records:` | ✅ PASS | 9.869s |
| `HC-13` | `healthcare_patients` | `missing_values` | Check for missing diagnosis records count | `0` | `0.00` | ✅ PASS | 9.129s |
| `HC-14` | `healthcare_patients` | `comparison` | Compare average systolic BP between Male and Female patients | `{Female: 126.98178713716563, Male: 126.38955823293` | `Table (2 rows)` | ✅ PASS | 9.048s |
| `HC-15` | `healthcare_patients` | `percentages` | What percentage of patients are covered by Star Health? | `17.63` | `17.63` | ✅ PASS | 9.11s |
| `HC-16` | `healthcare_patients` | `rankings` | Rank insurance providers by total claims billing amount | `Star Health, ICICI Lombard, Care Health, Self-Pay,` | `{'Rank': 1, 'Insurance_Provider': 'Star Health', '` | ✅ PASS | 9.223s |
| `HC-17` | `healthcare_patients` | `charts` | Show patient diagnosis breakdown | `{Cardiac Arrhythmia: 598, Orthopedic Trauma: 588, ` | `Table (6 rows)` | ✅ PASS | 7.963s |
| `HC-18` | `healthcare_patients` | `messy_typo` | avrg bil amnt by diagnsis | `{Asthma: 128123.6248805461, Cardiac Arrhythmia: 12` | `Table (6 rows)` | ✅ PASS | 9.634s |
| `HC-19` | `healthcare_patients` | `messy_hinglish` | sabse zyada bill kiska aaya hai | `Sai Shinde` | `{Patient_ID: PAT00950, Patient_Name: Sai Shinde, B` | ✅ PASS | 8.703s |
| `HC-20` | `healthcare_patients` | `messy_hinglish` | kitne mareez asthma ke hai | `586` | `586.00` | ✅ PASS | 8.566s |
| `HC-21` | `healthcare_patients` | `messy_vague` | senior citizens age 65 and above | `1,095` | `{type: table, total_records: 1095, displayed_recor` | ✅ PASS | 9.672s |
| `HC-22` | `healthcare_patients` | `messy_lowercase` | average cholesterol for male patients | `199.17` | `199.17` | ✅ PASS | 9.001s |
| `HC-23` | `healthcare_patients` | `messy_slang` | high blood pressure cases above 150 | `142` | `{type: table, total_records: 142, displayed_record` | ✅ PASS | 8.955s |
| `HC-24` | `healthcare_patients` | `messy_typo` | totl billing for star helth | `81,553,582.42` | `81,553,582.42` | ✅ PASS | 8.973s |
| `HC-25` | `healthcare_patients` | `messy_hinglish` | mahila mareezon ki ausat aayu kitni hai | `51.31` | `51.31` | ✅ PASS | 9.76s |
| `HC-26` | `healthcare_patients` | `messy_incomplete` | patients with Type 2 Diabetes count | `569` | `569.00` | ✅ PASS | 8.62s |
| `HC-27` | `healthcare_patients` | `messy_context` | and how many have Healthy / Checkup? | `577` | `0.00` | ❌ FAIL | 8.581s |
| `FN-01` | `finance_transactions` | `count` | What is the total count of transactions in the ledger? | `10,000` | `10,000.00` | ✅ PASS | 8.541s |
| `FN-02` | `finance_transactions` | `sum` | What is the total monetary value of all transactions? | `15,475,860.51` | `15,475,860.51` | ✅ PASS | 9.599s |
| `FN-03` | `finance_transactions` | `average` | What is the average transaction amount? | `1,547.59` | `1,547.59` | ✅ PASS | 8.607s |
| `FN-04` | `finance_transactions` | `median` | What is the median account balance after transaction? | `256,382.99` | `256,382.99` | ✅ PASS | 9.212s |
| `FN-05` | `finance_transactions` | `filter` | How many transactions were flagged as fraud? | `137` | `137.00` | ✅ PASS | 8.126s |
| `FN-06` | `finance_transactions` | `group_by` | Find total transaction amount by transaction type | `{ATM_WITHDRAWAL: 2735270.57, CREDIT_CARD: 2532699.` | `Table (6 rows)` | ✅ PASS | 8.75s |
| `FN-07` | `finance_transactions` | `top_n` | Show the top 5 highest value transactions | `TXN0008530, TXN0005243, TXN0000939, TXN0000296, TX` | `{'Transaction_ID': 'TXN0008530', 'Account_Number':` | ✅ PASS | 8.72s |
| `FN-08` | `finance_transactions` | `bottom_n` | Show the 5 smallest transaction amounts | `TXN0008929, TXN0008216, TXN0004919, TXN0006995, TX` | `{'Transaction_ID': 'TXN0008929', 'Amount': 50.04},` | ✅ PASS | 8.833s |
| `FN-09` | `finance_transactions` | `trend` | Show transaction counts by status | `{SUCCESS: 9599, FAILED: 264, FLAGGED: 137}` | `Table (3 rows)` | ✅ PASS | 7.825s |
| `FN-10` | `finance_transactions` | `correlation` | What is the correlation between transaction amount and account balance? | `0.01` | `0.01` | ✅ PASS | 9.093s |
| `FN-11` | `finance_transactions` | `outliers` | Count transactions with amount greater than 10000 | `14` | `14.00` | ✅ PASS | 8.742s |
| `FN-12` | `finance_transactions` | `duplicates` | Are there any duplicate transaction IDs? | `0` | `{type: table, total_records: 0, displayed_records:` | ✅ PASS | 8.782s |
| `FN-13` | `finance_transactions` | `missing_values` | How many missing values are in the status column? | `0` | `0.00` | ✅ PASS | 8.62s |
| `FN-14` | `finance_transactions` | `comparison` | Compare average transaction amount between UPI and CREDIT_CARD | `{CREDIT_CARD: 1539.6349848024315, UPI: 1526.247761` | `Table (2 rows)` | ✅ PASS | 9.843s |
| `FN-15` | `finance_transactions` | `percentages` | What percentage of transactions failed? | `2.64` | `2.64` | ✅ PASS | 7.64s |
| `FN-16` | `finance_transactions` | `rankings` | Rank the top merchants by transaction frequency | `Flipkart, DMart, Uber, Apollo Pharmacy, Shell Fuel` | `{'Merchant': 'Flipkart', 'Transaction_Frequency': ` | ✅ PASS | 8.77s |
| `FN-17` | `finance_transactions` | `charts` | Show spending breakdown across categories | `{Entertainment: 2195712.9, Food & Dining: 2296864.` | `Table (7 rows)` | ✅ PASS | 8.943s |
| `FN-18` | `finance_transactions` | `messy_typo` | avrg amnt for upi transctns | `1,526.25` | `1,526.25` | ✅ PASS | 7.79s |
| `FN-19` | `finance_transactions` | `messy_hinglish` | kul kitne fraudulent transactions pakde gaye | `137` | `137.00` | ✅ PASS | 8.767s |
| `FN-20` | `finance_transactions` | `messy_hinglish` | swiggy par total kitna kharcha hua | `1,533,504.41` | `1,009.00` | ❌ FAIL | 8.931s |
| `FN-21` | `finance_transactions` | `messy_vague` | failed payments count | `264` | `264.00` | ✅ PASS | 8.944s |
| `FN-22` | `finance_transactions` | `messy_lowercase` | which merchant has the highest total transaction amount | `DMart` | `{'Merchant': 'DMart', 'Total_Amount': 1660108.37}` | ✅ PASS | 8.913s |
| `FN-23` | `finance_transactions` | `messy_slang` | total spent on food & dining | `2,296,864.39` | `2,296,864.39` | ✅ PASS | 8.767s |
| `FN-24` | `finance_transactions` | `messy_typo` | totl amnt by catgory | `{Entertainment: 2195712.9, Food & Dining: 2296864.` | `Table (7 rows)` | ✅ PASS | 7.969s |
| `FN-25` | `finance_transactions` | `messy_hinglish` | sabse bada transaction kitne ka tha | `13,834.61` | `Food & Dining` | ❌ FAIL | 8.747s |
| `FN-26` | `finance_transactions` | `messy_incomplete` | uber transactions count | `1,017` | `1,017.00` | ✅ PASS | 8.633s |
| `FN-27` | `finance_transactions` | `messy_context` | and for Zomato? | `965` | `965.00` | ✅ PASS | 9.408s |
| `ST-01` | `student_marks` | `count` | How many total students are in the database? | `2,000` | `2,000.00` | ✅ PASS | 7.134s |
| `ST-02` | `student_marks` | `sum` | What is the total number of backlogs across all students? | `786` | `786.00` | ✅ PASS | 7.865s |
| `ST-03` | `student_marks` | `average` | What is the overall average CGPA of students? | `7.25` | `7.25` | ✅ PASS | 7.972s |
| `ST-04` | `student_marks` | `median` | What is the median attendance percentage? | `82.40` | `82.40` | ✅ PASS | 7.169s |
| `ST-05` | `student_marks` | `filter` | Show me the student who have ff grade count | `51` | `51.00` | ✅ PASS | 7.965s |
| `ST-06` | `student_marks` | `group_by` | Show the average CGPA branch-wise | `{AI&DS: 7.260914454277286, Civil: 7.21623906705539` | `Table (6 rows)` | ✅ PASS | 7.932s |
| `ST-07` | `student_marks` | `top_n` | Show the top 5 students with the highest CGPA | `Amit Bhosale, Tanmay Kajgunde, Aishwarya Deshmukh,` | `{'Student_ID': 'STU0395', 'Student_Name': 'Amit Bh` | ✅ PASS | 6.724s |
| `ST-08` | `student_marks` | `bottom_n` | Show 3 students with lowest attendance | `Karan Deshmukh, Vikram Jadhav, Pooja Jadhav` | `{'Student_ID': 'STU1791', 'Student_Name': 'Karan D` | ✅ PASS | 8.359s |
| `ST-09` | `student_marks` | `trend` | Average CGPA semester by semester | `{1: 7.369075630252101, 2: 7.216029962546816, 3: 7.` | `Table (8 rows)` | ✅ PASS | 7.903s |
| `ST-10` | `student_marks` | `correlation` | What is the correlation between attendance and CGPA? | `-0.04` | `-0.04` | ✅ PASS | 7.646s |
| `ST-11` | `student_marks` | `outliers` | How many students have CGPA above 9.0? | `111` | `111.00` | ✅ PASS | 7.777s |
| `ST-12` | `student_marks` | `duplicates` | Are there duplicate student IDs? | `0` | `No duplicate Student_IDs found.` | ✅ PASS | 7.649s |
| `ST-13` | `student_marks` | `missing_values` | Check missing values count in CGPA | `0` | `0.00` | ✅ PASS | 7.996s |
| `ST-14` | `student_marks` | `comparison` | Compare average CGPA between AI&DS and Computer Engineering | `{AI&DS: 7.260914454277286, Computer Engineering: 7` | `Table (2 rows)` | ✅ PASS | 7.066s |
| `ST-15` | `student_marks` | `percentages` | What percentage of students have 0 backlogs? | `76.20` | `76.20` | ✅ PASS | 8.039s |
| `ST-16` | `student_marks` | `rankings` | Rank departments by total student enrollment | `Information Technology, Civil, AI&DS, Mechanical, ` | `{'Department': 'Information Technology', 'Total_En` | ✅ PASS | 6.853s |
| `ST-17` | `student_marks` | `charts` | Show grade distribution for BTES203G | `{A: 489, A+: 404, B+: 402...}` | `Table (8 rows)` | ✅ PASS | 7.808s |
| `ST-18` | `student_marks` | `messy_typo` | avrg cgpa by deprtmnt | `{AI&DS: 7.260914454277286, Civil: 7.21623906705539` | `Table (6 rows)` | ✅ PASS | 8.133s |
| `ST-19` | `student_marks` | `messy_hinglish` | sabse zyada cgpa kis student ka hai | `Amit Bhosale` | `{Student_ID: STU0395, Student_Name: Amit Bhosale, ` | ✅ PASS | 7.675s |
| `ST-20` | `student_marks` | `messy_hinglish` | pune ke kitne students hai | `336` | `336.00` | ✅ PASS | 7.642s |
| `ST-21` | `student_marks` | `messy_vague` | show students who have a CGPA above 8 count | `516` | `516.00` | ✅ PASS | 32.555s |
| `ST-22` | `student_marks` | `messy_lowercase` | student with max credits earned | `Rahul Jadhav` | `{'Student_ID': 'STU0004', 'Student_Name': 'Rahul J` | ✅ PASS | 3.464s |
| `ST-23` | `student_marks` | `messy_slang` | toppers in ai&ds branch | `Aishwarya Deshmukh` | `{'Student_ID': 'STU1256', 'Student_Name': 'Aishwar` | ✅ PASS | 4.306s |
| `ST-24` | `student_marks` | `messy_typo` | how many studnts faild in btes203g | `51` | `1,910.00` | ❌ FAIL | 5.288s |
| `ST-25` | `student_marks` | `messy_hinglish` | kitne bacho ki attendance 75 se kam hai | `435` | `435.00` | ✅ PASS | 3.445s |
| `ST-26` | `student_marks` | `messy_incomplete` | students with 0 backlogs count | `1,524` | `1,524.00` | ✅ PASS | 3.366s |
| `ST-27` | `student_marks` | `messy_context` | and how many are in Information Technology? | `353` | `353.00` | ✅ PASS | 4.732s |
| `SN-01` | `sensor_timeseries` | `count` | What is the total number of sensor readings recorded? | `5,000` | `5,000.00` | ✅ PASS | 3.321s |
| `SN-02` | `sensor_timeseries` | `sum` | What is the total power consumption recorded across all readings? | `11,686.49` | `11,686.49` | ✅ PASS | 3.655s |
| `SN-03` | `sensor_timeseries` | `average` | What is the average temperature in Celsius? | `45.07` | `45.07` | ✅ PASS | 3.484s |
| `SN-04` | `sensor_timeseries` | `median` | What is the median atmospheric pressure in hPa? | `1,013.12` | `1,013.12` | ✅ PASS | 3.304s |
| `SN-05` | `sensor_timeseries` | `filter` | How many readings have CRITICAL status? | `243` | `243.00` | ✅ PASS | 7.847s |
| `SN-06` | `sensor_timeseries` | `group_by` | Calculate average temperature by Device ID | `{SENSOR_NODE_01: 45.91605263157894, SENSOR_NODE_02` | `Table (10 rows)` | ✅ PASS | 9.476s |
| `SN-07` | `sensor_timeseries` | `top_n` | Show the 5 highest vibration spikes recorded | `SENSOR_NODE_01, SENSOR_NODE_05, SENSOR_NODE_09, SE` | `{'Timestamp': '2024-06-18 02:10:00', 'Device_ID': ` | ✅ PASS | 6.286s |
| `SN-08` | `sensor_timeseries` | `bottom_n` | Show the 3 lowest power consumption readings | `SENSOR_NODE_08, SENSOR_NODE_07, SENSOR_NODE_01` | `{'Timestamp': '2024-06-01 03:05:00', 'Device_ID': ` | ✅ PASS | 9.09s |
| `SN-09` | `sensor_timeseries` | `trend` | Show reading counts by status | `{NORMAL: 4224, WARNING: 533, CRITICAL: 243}` | `Table (3 rows)` | ✅ PASS | 7.677s |
| `SN-10` | `sensor_timeseries` | `correlation` | What is the correlation between temperature and power consumption? | `-0.03` | `-0.03` | ✅ PASS | 3.495s |
| `SN-11` | `sensor_timeseries` | `outliers` | Find count of temperature readings exceeding 60 degrees | `189` | `189.00` | ✅ PASS | 8.781s |
| `SN-12` | `sensor_timeseries` | `duplicates` | Are there duplicate timestamps in the telemetry? | `0` | `0.00` | ✅ PASS | 3.399s |
| `SN-13` | `sensor_timeseries` | `missing_values` | Check for missing sensor values in Humidity count | `0` | `0.00` | ✅ PASS | 9.012s |
| `SN-14` | `sensor_timeseries` | `comparison` | Compare average vibration between NORMAL and CRITICAL states | `{CRITICAL: 4.48440329218107, NORMAL: 1.04166548295` | `Table (3 rows)` | ✅ PASS | 5.404s |
| `SN-15` | `sensor_timeseries` | `percentages` | What percentage of sensor readings are in NORMAL status? | `84.48` | `84.48` | ✅ PASS | 3.327s |
| `SN-16` | `sensor_timeseries` | `rankings` | Rank devices by count of readings | `SENSOR_NODE_02, SENSOR_NODE_09, SENSOR_NODE_05, SE` | `{'Device_ID': 'SENSOR_NODE_02', 'Reading_Count': 5` | ✅ PASS | 3.644s |
| `SN-17` | `sensor_timeseries` | `charts` | Show status breakdown counts | `{NORMAL: 4224, WARNING: 533, CRITICAL: 243}` | `Table (3 rows)` | ✅ PASS | 13.973s |
| `SN-18` | `sensor_timeseries` | `messy_typo` | avrg temprature by devce | `{SENSOR_NODE_01: 45.91605263157894, SENSOR_NODE_02` | `Table (10 rows)` | ✅ PASS | 7.093s |
| `SN-19` | `sensor_timeseries` | `messy_hinglish` | sabse zyada power kis device ne consume kiya | `SENSOR_NODE_02` | `SENSOR_NODE_03` | ❌ FAIL | 7.798s |
| `SN-20` | `sensor_timeseries` | `messy_hinglish` | kitni baar critical alert aaya | `243` | `243.00` | ✅ PASS | 3.489s |
| `SN-21` | `sensor_timeseries` | `messy_vague` | readings with humidity over 70 | `534` | `{type: table, total_records: 534, displayed_record` | ✅ PASS | 10.531s |
| `SN-22` | `sensor_timeseries` | `messy_lowercase` | maximum vibration level recorded | `11.19` | `11.19` | ✅ PASS | 4.445s |
| `SN-23` | `sensor_timeseries` | `messy_slang` | which sensor is hottest on average | `SENSOR_NODE_01` | `SENSOR_NODE_01` | ✅ PASS | 3.808s |
| `SN-24` | `sensor_timeseries` | `messy_typo` | totl pwer consumtion | `11,686.49` | `11,686.49` | ✅ PASS | 12.349s |
| `SN-25` | `sensor_timeseries` | `messy_hinglish` | warning status wale kitne records hai | `533` | `533.00` | ✅ PASS | 7.75s |
| `SN-26` | `sensor_timeseries` | `messy_incomplete` | readings with error code 505 count | `243` | `243.00` | ✅ PASS | 3.632s |
| `SN-27` | `sensor_timeseries` | `messy_context` | and what about error code 101? | `533` | `{type: table, total_records: 533, displayed_record` | ✅ PASS | 13.596s |
| `MD-01` | `messy_dataset` | `count` | What is the total row count in this messy dataset? | `2,000` | `2,000.00` | ✅ PASS | 3.154s |
| `MD-02` | `messy_dataset` | `sum` | What is the sum of clean record IDs? | `2,000,980` | `2,000,980.00` | ✅ PASS | 3.645s |
| `MD-03` | `messy_dataset` | `average` | What is the average score rating after ignoring nulls? | `4.32` | `4.32` | ✅ PASS | 8.731s |
| `MD-04` | `messy_dataset` | `median` | What is the median Record ID? | `1,000.00` | `1,000.00` | ✅ PASS | 3.709s |
| `MD-05` | `messy_dataset` | `filter` | How many records belong to Sales department? | `681` | `681.00` | ✅ PASS | 4.759s |
| `MD-06` | `messy_dataset` | `group_by` | Count of records by active flag | `{FALSE: 302, yes: 292, true: 291...}` | `Table (6 rows)` | ✅ PASS | 3.654s |
| `MD-07` | `messy_dataset` | `top_n` | Show top 5 records by record ID | `1999, 1999, 1998, 1997, 1996` | `{'Record_ID': 1, 'Client_Name': 'Maria Garcia', 'D` | ✅ PASS | 6.929s |
| `MD-08` | `messy_dataset` | `bottom_n` | Show bottom 3 records by record ID | `1, 2, 3` | `{'Record_ID': 1999, 'Client_Name': '  John Doe ', ` | ✅ PASS | 6.476s |
| `MD-09` | `messy_dataset` | `trend` | Count of records with valid 2023 dates | `1,127` | `1,127.00` | ✅ PASS | 6.638s |
| `MD-10` | `messy_dataset` | `correlation` | Correlation between Record_ID and clean numeric Score_Rating | `0.04` | `0.04` | ✅ PASS | 3.553s |
| `MD-11` | `messy_dataset` | `outliers` | Count records with Score_Rating equal to 5 | `282` | `282.00` | ✅ PASS | 10.619s |
| `MD-12` | `messy_dataset` | `duplicates` | How many duplicate Record IDs exist in this data? | `20` | `20.00` | ✅ PASS | 3.511s |
| `MD-13` | `messy_dataset` | `missing_values` | How many missing Client Names are in the dataset? | `277` | `277.00` | ✅ PASS | 3.787s |
| `MD-14` | `messy_dataset` | `comparison` | Count of records for Engineering vs Sales | `{SALES: 245, Sales: 222, Engineering: 219...}` | `Table (2 rows)` | ✅ PASS | 3.973s |
| `MD-15` | `messy_dataset` | `percentages` | What percentage of records have null client names? | `13.85` | `13.85` | ✅ PASS | 8.763s |
| `MD-16` | `messy_dataset` | `rankings` | Rank raw departments by count | `SALES, Human Resources,   Finance  , Sales, HR...` | `{'Count': 'SALES', 'count': 245}, {'Count': 'Human` | ✅ PASS | 11.973s |
| `MD-17` | `messy_dataset` | `charts` | Show active flag distribution | `{FALSE: 302, yes: 292, true: 291...}` | `Table (7 rows)` | ✅ PASS | 4.125s |
| `MD-18` | `messy_dataset` | `messy_typo` | avrg scor ratng | `4.32` | `4.32` | ✅ PASS | 3.647s |
| `MD-19` | `messy_dataset` | `messy_hinglish` | kitne records duplicate hai | `20` | `0.00` | ❌ FAIL | 10.053s |
| `MD-20` | `messy_dataset` | `messy_hinglish` | sales department me kitne log hai | `681` | `681.00` | ✅ PASS | 6.846s |
| `MD-21` | `messy_dataset` | `messy_vague` | records with rating 4.8 | `287` | `{type: table, total_records: 287, displayed_record` | ✅ PASS | 3.655s |
| `MD-22` | `messy_dataset` | `messy_lowercase` | count missing names | `277` | `277.00` | ✅ PASS | 11.801s |
| `MD-23` | `messy_dataset` | `messy_slang` | how many nulls in department | `208` | `208.00` | ✅ PASS | 4.199s |
| `MD-24` | `messy_dataset` | `messy_typo` | totl clints in enginering | `415` | `6.00` | ❌ FAIL | 7.583s |
| `MD-25` | `messy_dataset` | `messy_hinglish` | null values kitni hai client name me | `277` | `277.00` | ✅ PASS | 3.805s |
| `MD-26` | `messy_dataset` | `messy_incomplete` | records with invalid_date in signup | `283` | `{type: table, total_records: 283, displayed_record` | ✅ PASS | 10.055s |
| `MD-27` | `messy_dataset` | `messy_context` | and how many are in HR? | `460` | `220.00` | ✅ PASS | 7.321s |


## 5. Honest Edge Cases & Analysis

- **Hinglish & Multilingual Queries:** QueryUnderstandingAgent accurately translated colloquial terms (e.g. *sabse jyada*, *kitne*, *mahilaon ki*) to canonical schema columns.
- **Messy Real-World Formatting:** Currency symbols (`$`, `₹`), inconsistent dates (`YYYY-MM-DD`, `DD/MM/YYYY`), and mixed null values were converted cleanly via `pd.to_numeric` and `DataEngine.sanitize_for_json` without crashing or throwing `NaN is not valid JSON`.
- **Ambiguity Resolution:** When a column was ambiguous or had loose synonyms (`ctc` -> `Annual_Salary`, `pay` -> `Billing_Amount`), stated assumptions were explicitly generated and returned.