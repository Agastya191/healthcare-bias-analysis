# Socioeconomic Bias in U.S. Healthcare Access

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Agastya191/healthcare-bias-analysis/blob/main/notebooks/analysis.ipynb)

A data analysis project investigating whether income level and education level are associated with disparities in healthcare access across the United States using CDC BRFSS 2022 survey data (445,132 respondents; 339,702 after cleaning).

This work is motivated by the broader challenge of medical dataset bias: populations with limited healthcare access are systematically underrepresented in clinical data, which propagates downstream bias into medical AI models and treatment guidelines.

---

## Research Questions

1. Do lower-income Americans have significantly lower rates of health insurance coverage?
2. Are low-income/low-education individuals more likely to skip doctor visits due to cost?
3. How strongly do socioeconomic factors predict healthcare access outcomes after controlling for demographic variables?
4. What are the implications for bias in medical datasets and clinical AI?

---

## Dataset

**CDC Behavioral Risk Factor Surveillance System (BRFSS) — 2022**  
- 445,132 U.S. adult respondents (339,702 with complete income, insurance, and cost-barrier answers)  
- Annual telephone health survey  
- Variables: income, education, insurance status, cost barriers, checkup frequency, self-rated health  

The notebook downloads the data from the CDC automatically. See [`data/README.md`](data/README.md) for manual download instructions. Raw data files are not committed to this repo.

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

## Setup & Usage

**In the browser (no setup):** click the Colab badge above, then `Runtime → Run all`. The notebook downloads the code and the BRFSS data itself.

**Locally:**
```bash
git clone https://github.com/Agastya191/healthcare-bias-analysis.git
cd healthcare-bias-analysis
pip install -r requirements.txt
jupyter notebook notebooks/analysis.ipynb   # downloads the data on first run
```

---

## Key Findings

- **Insurance coverage:** 98.6% of respondents earning over $200k had health coverage, compared with 85.5% of those earning under $10k, a 13.1 percentage point gap. In the logistic regression, each step up in income bracket was associated with 19% higher odds of being insured (OR = 1.19, 95% CI 1.19–1.20), controlling for education and sex.
- **Cost barriers:** 22.9% of respondents earning under $10k skipped a doctor visit because of cost in the past year, compared with 1.6% of those earning over $200k, about 14 times as often. Cost barriers fell at nearly every step up the income ladder. Each step up in income bracket was associated with 21% lower odds of a cost barrier (OR = 0.79, 95% CI 0.79–0.80).
- **Education:** College graduates had 97.7% coverage versus 69.2% for respondents who never attended school, a 28.5 percentage point gap. Each step up in education level was associated with 66% higher odds of coverage (OR = 1.66, 95% CI 1.64–1.69).
- **Significance:** Chi-square tests found significant associations between income and insurance (χ² = 8,127, df = 10), income and cost barriers (χ² = 12,511, df = 10), and education and insurance (χ² = 13,548, df = 5), all p < 0.001.

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

Healthcare access disparities don't just affect patient outcomes — they shape the **composition of medical datasets**. When lower SES populations are less likely to visit doctors, they are:

- Underrepresented in EHR-derived training datasets
- Less likely to receive diagnoses that require specialist access
- More likely to present at later disease stages

This means ML models trained on clinical data may systematically underperform for the populations with the highest burden of disease 

---

Data sourced from CDC BRFSS (public domain).
