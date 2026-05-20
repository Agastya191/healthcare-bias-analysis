# Data

## CDC BRFSS Dataset

This project uses the **CDC Behavioral Risk Factor Surveillance System (BRFSS)** annual survey data.

### Download Instructions

The notebook downloads the data automatically. To download it yourself:

1. Download the 2022 SAS Transport file: https://www.cdc.gov/brfss/annual_data/2022/files/LLCP2022XPT.zip
2. Unzip it and place `LLCP2022.XPT` in this `data/` directory (the CDC file may extract with a trailing space in its name, so rename it if needed)

### Why BRFSS?

BRFSS is the world's largest ongoing telephone health survey — over **400,000 U.S. adult respondents** per year. It includes self-reported health status, healthcare access, income, education, and demographics, making it ideal for studying socioeconomic disparities in healthcare access.

### Key Variables Used

| BRFSS Column | Renamed To         | Description                              |
|--------------|--------------------|------------------------------------------|
| `INCOME3`    | `income_level`     | Annual household income (11 brackets)    |
| `EDUCA`      | `education_level`  | Highest education level completed        |
| `_HLTHPLN`   | `has_insurance`    | Any health care coverage (Yes/No)        |
| `MEDCOST1`   | `cost_barrier`     | Skipped doctor due to cost (Yes/No)      |
| `CHECKUP1`   | `last_checkup`     | Time since last routine checkup          |
| `GENHLTH`    | `general_health`   | Self-rated general health (1=Excellent)  |
| `SEXVAR`     | `sex`              | Sex (1=Male, 2=Female)                   |
| `_IMPRACE`   | `race`             | Imputed race/ethnicity                   |
| `_STATE`     | `state`            | State FIPS code                          |

### Data Privacy

Raw data files are **not committed** to this repository. The `.gitignore` excludes `.csv`, `.zip`, `.XPT`, and similar data files.
