# README - IMDb Big Data Analysis with PySpark

## Project Overview

This project is dedicated to large-scale processing and analysis of the IMDb dataset using PySpark. The main objective is to build a complete big data workflow that includes data loading, schema definition, preprocessing, transformation, analysis, feature engineering, optimization, and saving final results.

The project is designed to work in both a local PySpark setup and a Docker-based environment, making it convenient for development, testing, and deployment.

---

## Dataset

The project uses the IMDb dataset, which contains information about:

| File | Description |
|------|-------------|
| `name.basics.tsv.gz` | Basic information about people involved in titles |
| `title.akas.tsv.gz` | Alternative titles and regional title variations |
| `title.basics.tsv.gz` | Main information about movies and TV titles |
| `title.crew.tsv.gz` | Information about directors and writers |
| `title.episode.tsv.gz` | Episode-level relationships for TV series |
| `title.principals.tsv.gz` | Main cast and crew for each title |
| `title.ratings.tsv.gz` | Ratings and number of votes for titles |

This dataset makes it possible to explore trends in the entertainment industry, analyze ratings and popularity, and perform business-oriented transformations for deeper insights.

---

## Technologies Used

- Python
- PySpark
- Docker
- Git
- GitHub

---

## Contributors

- Kateryna Rubtsova
- Khrystyna Liashenyk
- Sofia Pryslipska
- Yulia Salishcheva
- Sofia Pasichko

---

## Responsibility Distribution

**Project Manager:** **Yulia Salishcheva**

### Preparation Stage

- **Khrystyna Liashenyk** - repository creation, `.gitignore`
- **Kateryna Rubtsova** - dataset description
- **Sofia Pryslipska** - dataset description
- **Sofia Pasichko** - report preparation
- **Yulia Salishcheva** - presentation preparation

All team members participated in dataset search, selection, and PySpark installation.

### Environment Setup Stage

### Stage 2 - Environment Setup

- **Kateryna Rubtsova** and **Sofia Pryslipska** - Dockerfile setup, `main.py`, PySpark configuration, `.gitignore` update
- **Khrystyna Liashenyk** - `README` preparation
- **Sofia Pasichko** - report formatting
- **Yulia Salishcheva** - presentation formatting

All team members participated in local environment configuration.
