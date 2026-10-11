# 🏢 PugArch Technology — Day 3 Facility Intelligence & Data Analytics

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Array%20Computing-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557C?style=for-the-badge)
![Seaborn](https://img.shields.io/badge/Seaborn-Statistical%20Plots-4C72B0?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Render](https://img.shields.io/badge/Deployment-Render-46E3B7?style=for-the-badge&logo=render&logoColor=black)

</p>

<p align="center">
<strong>Data Quality • Exploratory Data Analysis • Statistical Intelligence • Visualization • Interactive Analytics</strong>
</p>

---

## 🌐 Project Dashboard

> After deployment, place the Render URL here.

**Live Dashboard:** `[https://your-render-url.onrender.com/](https://pugarch-day3-facility-intelligence.onrender.com/)`

**Source Code:** `https://github.com/<your-username>/<your-repository>`

---

# 1. Executive Summary

This project is the **Day 3 practical assignment** for the **PugArch Technology 10-Day Intern Technical Training & Domain Assessment Program**, under the **Data & AI/ML** track.

The project demonstrates an end-to-end data analytics workflow using a deliberately imperfect facility inspection dataset.

The pipeline starts with **raw, dirty operational data**, performs automated data-quality inspection and cleaning, applies statistical analysis, generates publication-quality visualizations, and finally exposes the cleaned data and analytical insights through an interactive **Streamlit dashboard**.

The project is designed to demonstrate practical understanding of:

- NumPy array and numerical operations
- Pandas DataFrame manipulation
- Data quality engineering
- Missing-value treatment
- Duplicate detection
- Invalid-value correction
- IQR-based outlier handling
- Group-wise statistical analysis
- Correlation analysis
- Business/operational insight generation
- Static visualization
- Interactive visualization
- Dashboard development
- Data pipeline modularization
- Cloud deployment

---

# 2. Business Problem

Facility operations teams need reliable information to understand:

- Which locations have poor cleanliness?
- Where are odor-related complaints concentrated?
- Does water availability affect hygiene outcomes?
- Which locations experience the highest visitor pressure?
- Which facilities represent the highest operational risk?
- Are there suspicious or invalid observations in the inspection data?

Raw operational data is rarely perfect.

It can contain:

- Missing values
- Duplicate records
- Invalid numerical values
- Extreme observations
- Inconsistent data types
- Incomplete categorical information

Therefore, this project treats **data quality as a first-class stage of the analytical pipeline**.

---

# 3. Project Objective

The primary objective is to build a reusable facility-data intelligence pipeline that:

```text
Raw Data
   ↓
Data Quality Inspection
   ↓
Data Cleaning
   ↓
Outlier Treatment
   ↓
Clean Dataset
   ↓
Statistical Analysis
   ↓
Operational Insights
   ↓
Static Visualizations
   ↓
Interactive Dashboard
   ↓
Deployment
```

---

# 4. Dataset

The project uses a generated facility inspection dataset containing at least 150 base records and intentionally injected data-quality issues.

## Dataset Fields

| Field | Description |
|---|---|
| `facility_id` | Unique facility identifier |
| `location` | Facility location |
| `cleanliness_score` | Cleanliness rating from 1–10 |
| `odor_score` | Odor severity from 1–5 |
| `waste_level` | Low / Medium / High / Critical |
| `water_availability` | Yes / No |
| `footfall` | Approximate daily visitors |
| `complaints` | Registered complaints |
| `inspection_date` | Inspection date |

## Location Categories

The dataset strictly uses:

- North Wing
- South Wing
- East Concourse
- West Terminal
- Central Hub

## Waste Categories

- Low
- Medium
- High
- Critical

---

# 5. Intentional Data Quality Issues

The raw dataset intentionally contains controlled data-quality problems so that the cleaning pipeline can be demonstrated realistically.

### Duplicate Records

5 duplicate rows are intentionally injected.

### Missing Values

Approximately 8% missing values are introduced into:

- `cleanliness_score`
- `odor_score`
- `water_availability`

### Invalid Values

3 negative complaint values are intentionally introduced.

### Statistical Outliers

At least 4 extreme `footfall` values are injected, including values far outside the normal operational range.

This allows the project to demonstrate real-world data-quality handling rather than analyzing an artificially perfect dataset.

---

# 6. Data Cleaning Pipeline

The cleaning pipeline is implemented in:

```text
data-cleaning/clean_data.py
```

## Cleaning Steps

### Step 1 — Load Raw Data

The pipeline reads:

```text
dataset/raw_facility_data.csv
```

using Pandas.

---

### Step 2 — Inspect Data

The pipeline reports:

- Data types
- Null counts
- Dataset dimensions

---

### Step 3 — Remove Duplicates

Exact duplicate records are detected using Pandas:

```python
df.duplicated()
```

and removed using:

```python
df.drop_duplicates()
```

The number of removed records is logged.

---

### Step 4 — Correct Invalid Complaints

Negative complaint counts are treated as invalid operational observations.

They are replaced with:

```text
0
```

---

### Step 5 — Missing Numerical Values

Missing:

- `cleanliness_score`
- `odor_score`

are imputed using **location-wise median values**.

This preserves local characteristics better than blindly replacing missing values with one global statistic.

---

### Step 6 — Missing Water Availability

Missing `water_availability` values are replaced using the dataset mode.

---

### Step 7 — Footfall Outlier Treatment

The pipeline calculates:

```text
Q1
Q3
IQR = Q3 - Q1
```

and defines the IQR bounds as:

```text
Lower Bound = Q1 - 1.5 × IQR

Upper Bound = Q3 + 1.5 × IQR
```

Extreme values are then capped to the calculated bounds.

NumPy is used for the numerical calculations and clipping operation.

---

### Step 8 — Date Standardization

Inspection dates are converted into:

```text
datetime64[ns]
```

This ensures reliable date filtering and time-based analysis.

---

## Clean Dataset Output

The cleaned dataset is saved as:

```text
dataset/cleaned_facility_data.csv
```

A machine-readable cleaning report is also generated:

```text
reports/data_quality_report.json
```

---

# 7. Statistical Analysis

The analysis module is:

```text
analysis/facility_analysis.py
```

It uses Pandas and NumPy to produce operational statistics.

## Location-Level Analysis

For every location, the project calculates:

- Average cleanliness
- Average odor
- Average footfall
- Total complaints
- Facility count

---

## Water Availability Analysis

The project compares facilities with:

```text
Water Available = Yes
Water Available = No
```

and calculates:

- Total complaints
- Average complaints
- Average cleanliness
- Average odor
- Facility count

---

## Waste-Level Analysis

The project analyzes:

- Low
- Medium
- High
- Critical

waste categories against:

- Average footfall
- Average complaints
- Average cleanliness
- Facility count

---

# 8. Correlation Analysis

Pearson correlation is calculated across:

```text
cleanliness_score
odor_score
footfall
complaints
```

The correlation matrix helps identify relationships between operational variables.

For example:

```text
Odor ↑
   ↓
Complaints ↑
```

may indicate that odor-related facility conditions are associated with higher complaint volumes.

The exact relationship is calculated from the generated dataset rather than assumed.

---

# 9. Operational Risk Model

The project introduces a simple explainable operational risk score.

The risk score combines:

- High average footfall
- Low average cleanliness

using:

```text
Risk Score =
0.60 × Footfall Risk
+
0.40 × Cleanliness Risk
```

The weighting prioritizes visitor pressure while still accounting for hygiene quality.

This produces a transparent location-level ranking that can be used for operational prioritization.

---

# 10. Business Insights

The analysis automatically generates three data-backed operational insights.

## Insight 1 — Odor vs Complaints

The project calculates the Pearson correlation between:

```text
odor_score
complaints
```

A positive correlation indicates that higher odor severity tends to be associated with increased complaint volumes.

The exact correlation value is generated automatically by:

```text
analysis/facility_analysis.py
```

---

## Insight 2 — Water Availability

The project compares facilities with and without water availability across:

- Cleanliness
- Odor
- Complaints

This helps quantify whether reliable water access is associated with better hygiene outcomes and lower complaint burden.

---

## Insight 3 — Highest-Risk Location

A weighted operational risk score is calculated for each location using:

```text
60% Footfall Risk
40% Cleanliness Risk
```

The location with the highest score is identified automatically as the highest-priority operational area.

This is more useful for decision-making than simply ranking locations by one metric.

---

# 11. Static Visualizations

The project generates five high-resolution visualizations at **300 DPI**.

All charts are stored in:

```text
visualizations/
```

---

## 1. Cleanliness by Location

File:

```text
bar_cleanliness_by_location.png
```

Shows:

- Mean cleanliness score
- Location comparison
- Standard deviation error bars

---

## 2. Complaints by Water Availability

File:

```text
bar_complaints_by_water.png
```

Compares total complaint volume between:

```text
Yes
No
```

water availability categories.

---

## 3. Footfall Distribution

File:

```text
hist_footfall_distribution.png
```

Shows the distribution of daily visitors using:

- Histogram
- KDE curve

---

## 4. Odor vs Cleanliness

File:

```text
scatter_odor_vs_cleanliness.png
```

Shows:

- Odor score on X-axis
- Cleanliness score on Y-axis
- Waste level as color/category
- Regression trendline

---

## 5. Correlation Heatmap

File:

```text
heatmap_correlation_matrix.png
```

Displays annotated Pearson correlations between numerical variables.

---

# 12. Interactive Dashboard

The interactive dashboard is implemented using:

```text
app.py
```

The dashboard uses:

- Streamlit
- Plotly Express
- Plotly Graph Objects
- Pandas
- NumPy

---

## Dashboard Features

### Sidebar Filters

Users can filter the dataset by:

- Location
- Waste Level
- Inspection Date Range

---

## KPI Cards

The dashboard displays:

### 🏢 Total Facilities Inspected

Number of unique facilities in the filtered dataset.

### 🧼 Average Cleanliness Rating

Average cleanliness score.

### 📢 System-wide Complaints

Total registered complaints.

### 💧 Water Availability Uptime

Percentage of facilities with available water.

---

## Interactive Charts

The dashboard provides:

- Cleanliness by location
- Complaints by water availability
- Footfall distribution
- Odor vs cleanliness scatter plot
- Correlation heatmap
- Operational risk ranking

---

## Data Explorer

The cleaned dataset can be:

- Viewed interactively
- Filtered through dashboard controls
- Downloaded as CSV

---

# 13. Repository Structure

```text
day-03-facility-intelligence/
│
├── 📁 dataset/
│   ├── generate_dataset.py
│   ├── raw_facility_data.csv
│   └── cleaned_facility_data.csv
│
├── 📁 data-cleaning/
│   └── clean_data.py
│
├── 📁 analysis/
│   └── facility_analysis.py
│
├── 📁 visualizations/
│   ├── create_visualizations.py
│   ├── bar_cleanliness_by_location.png
│   ├── bar_complaints_by_water.png
│   ├── hist_footfall_distribution.png
│   ├── scatter_odor_vs_cleanliness.png
│   └── heatmap_correlation_matrix.png
│
├── 📁 reports/
│   ├── data_quality_report.json
│   └── analysis_report.json
│
├── 📁 .streamlit/
│   └── config.toml
│
├── app.py
├── requirements.txt
├── render.yaml
├── .gitignore
└── README.md
```

---

# 14. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Core development |
| NumPy | Numerical computation and IQR outlier handling |
| Pandas | Data manipulation and analysis |
| Matplotlib | Static visualization |
| Seaborn | Statistical visualization |
| Plotly | Interactive visualization |
| Streamlit | Interactive dashboard |
| SciPy | Statistical visualization support |
| Statsmodels | Statistical ecosystem / regression support |
| Git | Version control |
| GitHub | Source code management |
| Render | Cloud deployment |

---

# 15. Local Setup

## Prerequisites

Install:

- Python 3.11+
- Git

---

## Step 1 — Clone Repository

```bash
git clone https://github.com/<your-username>/<your-repository>.git
```

```bash
cd day-03-facility-intelligence
```

---

## Step 2 — Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 16. Generate Raw Dataset

Run:

```bash
python dataset/generate_dataset.py
```

This creates:

```text
dataset/raw_facility_data.csv
```

with intentionally injected data-quality issues.

---

# 17. Run Data Cleaning

Run:

```bash
python data-cleaning/clean_data.py
```

This creates:

```text
dataset/cleaned_facility_data.csv
```

and:

```text
reports/data_quality_report.json
```

---

# 18. Run Statistical Analysis

Run:

```bash
python analysis/facility_analysis.py
```

This generates:

```text
reports/analysis_report.json
```

and prints the analytical report in the terminal.

---

# 19. Generate Visualizations

Run:

```bash
python visualizations/create_visualizations.py
```

Five 300-DPI charts will be generated inside:

```text
visualizations/
```

---

# 20. Launch Interactive Dashboard

Run:

```bash
streamlit run app.py
```

The application will normally open at:

```text
http://localhost:8501
```

---

# 21. Complete Pipeline

For a fresh project run:

```bash
python dataset/generate_dataset.py
```

```bash
python data-cleaning/clean_data.py
```

```bash
python analysis/facility_analysis.py
```

```bash
python visualizations/create_visualizations.py
```

```bash
streamlit run app.py
```

---

# 22. Render Deployment

The repository includes:

```text
render.yaml
```

which defines the deployment configuration.

## Build Command

```bash
pip install -r requirements.txt
```

## Start Command

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port $PORT
```

### Deployment Flow

```text
GitHub Repository
       ↓
Render
       ↓
Install requirements
       ↓
Start Streamlit
       ↓
Public Dashboard URL
```

---

# 23. Data Quality Report

The cleaning pipeline automatically records:

- Rows before cleaning
- Rows after cleaning
- Duplicate rows removed
- Invalid complaint values corrected
- Missing water values imputed
- Footfall Q1
- Footfall Q3
- Footfall IQR
- Lower IQR bound
- Upper IQR bound
- Number of footfall outliers capped
- Remaining missing values

The machine-readable report is:

```text
reports/data_quality_report.json
```

This makes the cleaning process auditable and reproducible.

---

# 24. Reproducibility

The dataset generator uses a fixed random seed:

```text
42
```

This ensures that the intentionally generated dataset can be reproduced consistently.

The pipeline is therefore:

```text
Generate
   ↓
Clean
   ↓
Analyze
   ↓
Visualize
   ↓
Deploy
```

---

# 25. Engineering Practices Demonstrated

This project follows several professional development practices:

- Modular Python scripts
- Reusable functions
- Type hints
- Docstrings
- Deterministic dataset generation
- Explicit file paths
- Automated data validation
- Data-quality reporting
- Separation of concerns
- Cached dashboard data loading
- Interactive filtering
- Downloadable analytical data
- Machine-readable analytical reports
- Version-control friendly project structure
- Cloud deployment configuration

---

# 26. Future Enhancements

Potential future extensions include:

- Machine learning-based facility risk prediction
- Automated anomaly detection
- Time-series forecasting of complaints
- Facility-level risk classification
- Automated email alerts for critical facilities
- PostgreSQL integration
- REST API layer
- Docker containerization
- CI/CD pipeline using GitHub Actions
- Role-based dashboard access
- Advanced geospatial visualization
- Automated scheduled data ingestion
- Model monitoring and data drift detection

---

# 27. Resume-Relevant Skills Demonstrated

This project demonstrates practical experience in:

```text
Python
NumPy
Pandas
Data Cleaning
Exploratory Data Analysis
Statistical Analysis
Data Visualization
Matplotlib
Seaborn
Plotly
Streamlit
Data Quality Engineering
Outlier Detection
IQR Analysis
Correlation Analysis
Business Insight Generation
Dashboard Development
Git
GitHub
Cloud Deployment
```

---

# 28. Project Status

<p align="center">

### ✅ COMPLETED

<strong>Data Generation → Data Cleaning → Statistical Analysis → Visualization → Dashboard → Deployment</strong>

</p>

---

# 👩‍💻 Author

## Vaibhavi Mehar

**Final Year Information Technology Engineering Student**

Interested in:

- Data & AI/ML
- Cloud Computing
- DevOps
- Multi-Cloud Engineering
- Python
- Java
- Data Structures & Algorithms

---

# 🏢 Training Program

## PugArch Technology Pvt. Ltd.

### 10-Day Intern Technical Training & Domain Assessment Program

**Day 3 — Data Analysis & Python for AI/ML**

**Area:** Data & AI/ML

**Core Topics:**

```text
NumPy
Pandas
Data Cleaning
Data Analysis
Matplotlib
Seaborn
Plotly
Streamlit
```

---

<p align="center">

<strong>Built with Python 🐍 | Analyzed with Pandas 📊 | Visualized with Seaborn & Plotly 📈 | Deployed with Streamlit 🚀</strong>

</p>
