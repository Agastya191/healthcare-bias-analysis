# Data

## CDC BRFSS Dataset

This project uses the **CDC Behavioral Risk Factor Surveillance System (BRFSS)** annual survey data.

### Download Instructions

1. Go to: https://www.cdc.gov/brfss/annual_data/annual_data.htm
2. Select the most recent year (e.g. **2022**)
3. Download the **CSV format** file (`LLCP2022CSV.zip`)
4. Unzip and place `LLCP2022.csv` in this `data/` directory

### Why BRFSS?

BRFSS is the world's largest ongoing telephone health survey — over **400,000 U.S. adult respondents** per year. It includes self-reported health status, healthcare access, income, education, and demographics, making it ideal for studying socioeconomic disparities in healthcare access.

### Key Variables Used

| BRFSS Column | Renamed To         | Description                              |
|--------------|--------------------|------------------------------------------|
| `INCOME2`    | `income_level`     | Annual household income (8 brackets)     |
| `EDUCA`      | `education_level`  | Highest education level completed        |
| `HLTHPLN1`   | `has_insurance`    | Any health care coverage (Yes/No)        |
| `MEDCOST`    | `cost_barrier`     | Skipped doctor due to cost (Yes/No)      |
| `CHECKUP1`   | `last_checkup`     | Time since last routine checkup          |
| `GENHLTH`    | `general_health`   | Self-rated general health (1=Excellent)  |
| `SEXVAR`     | `sex`              | Sex (1=Male, 2=Female)                   |

### Data Privacy

Raw data files are **not committed** to this repository. The `.gitignore` excludes all `.csv`, `.gz`, and `.pth` files.
