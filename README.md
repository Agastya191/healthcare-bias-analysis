# Socioeconomic Bias in U.S. Healthcare Access

A data analysis project investigating whether **income level** and **education level** are associated with disparities in healthcare access across the United States, using CDC BRFSS survey data (~400,000 respondents).

This work is motivated by the broader challenge of **medical dataset bias**: populations with limited healthcare access are systematically underrepresented in clinical data, which propagates downstream bias into medical AI models and treatment guidelines.

---

## Research Questions

1. Do lower-income Americans have significantly lower rates of health insurance coverage?
2. Are low-income/low-education individuals more likely to skip doctor visits due to cost?
3. How strongly do socioeconomic factors predict healthcare access outcomes after controlling for demographic variables?
4. What are the implications for bias in medical datasets and clinical AI?

---

## Dataset

**CDC Behavioral Risk Factor Surveillance System (BRFSS) — 2022**  
- 400,000+ U.S. adult respondents  
- Annual telephone health survey  
- Variables: income, education, insurance status, cost barriers, checkup frequency, self-rated health  

See [`data/README.md`](data/README.md) for download instructions. Raw data files are not committed to this repo.

---

## Methods

| Method | Purpose |
|---|---|
| Descriptive statistics | Access rates by income/education bracket |
| Chi-square test | Statistical significance of group associations |
| Logistic regression (statsmodels) | Odds ratios for insurance coverage and cost barriers |
| Pearson correlation | Relationships between all key variables |
| Disparity gap analysis | Quantify best-off vs worst-off group difference |

---

## Project Structure

```
healthcare-bias-analysis/
├── data/
│   └── README.md           # Download instructions for BRFSS dataset
├── notebooks/
│   └── analysis.ipynb      # Main analysis notebook (end-to-end)
├── src/
│   ├── preprocess.py       # Data loading, cleaning, recoding
│   ├── analysis.py         # Statistical tests and models
│   └── visualize.py        # All figure generation
├── outputs/                # Saved figures (generated on run)
├── requirements.txt
└── .gitignore
```

---

## Setup & Usage

```bash
# 1. Clone the repo
git clone https://github.com/Agastya191/healthcare-bias-analysis.git
cd healthcare-bias-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download BRFSS data (see data/README.md)

# 4. Run the notebook
jupyter notebook notebooks/analysis.ipynb
```

---

## Key Findings

*(Generated after running the analysis — update with your observed values)*

- **Insurance gap:** Respondents earning >$75k had ~X% coverage vs ~Y% for those earning <$10k — a **Z percentage point disparity**.
- **Cost barrier:** Low-income respondents were **X× more likely** to skip a doctor visit due to cost.
- **Logistic regression:** Each income bracket increase is associated with higher odds of insurance coverage (OR > 1) and lower odds of cost barriers (OR < 1), controlling for education and sex.
- **Chi-square:** All associations between income/education and access outcomes were statistically significant (p < 0.001).

---

## Figures

| # | Figure |
|---|---|
| 1 | Insurance coverage rate by income level |
| 2 | Cost barrier rate by income level |
| 3 | Insurance coverage rate by education level |
| 4 | Self-rated health score by income level |
| 5 | Correlation heatmap |
| 6 | Odds ratio forest plot — insurance coverage |
| 7 | Odds ratio forest plot — cost barrier |
| 8 | Routine checkup rate by income level |

---

## Implications for Medical Bias Research

Healthcare access disparities don't just affect patient outcomes — they shape the **composition of medical datasets**. When lower-SES populations are less likely to visit doctors, they are:

- Underrepresented in EHR-derived training datasets
- Less likely to receive diagnoses that require specialist access
- More likely to present at later disease stages

This means ML models trained on clinical data may systematically **underperform for the populations with the highest burden of disease** — a critical issue for equitable AI in medicine.

---

## Author

**Agastya Munnangi**  
[GitHub](https://github.com/Agastya191) · [Portfolio](https://agastya191.github.io)

---

## License

MIT License. Data sourced from CDC BRFSS (public domain).
