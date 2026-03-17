# README - IMDb Big Data Analysis with PySpark

## Project Overview

This project is dedicated to large-scale processing and analysis of the IMDb dataset using PySpark. The main objective is to build a complete big data workflow that includes data loading, schema definition, preprocessing, transformation, analysis, feature engineering, optimization, and saving final results.

The project is designed to work in both a local PySpark setup and a Docker-based environment, making it convenient for development, testing, and deployment.

---

## Dataset

This project uses the official IMDb Non-Commercial Datasets, which are distributed as compressed tab-separated files (`.tsv.gz`). The dataset is encoded in UTF-8, updated daily, and uses `\N` to represent missing values.

For this project, we selected **7 IMDb data files** that describe titles, people, ratings, episodes, alternative names, and production roles.  
Together, these files contain **39 features in total**, which makes the dataset rich enough for large-scale processing, integration, and analytical tasks in PySpark.

### Selected Files

| File | Number of features | Description |
|------|--------------------|-------------|
| `name.basics.tsv.gz` | 6 | Basic information about people in the film industry, including names, birth and death years, professions, and well-known titles. |
| `title.akas.tsv.gz` | 8 | Alternative names of titles in different regions and languages. |
| `title.basics.tsv.gz` | 9 | Main information about movies, series, and other titles, including title type, names, years, runtime, and genres. |
| `title.crew.tsv.gz` | 3 | Information about directors and writers of each title. |
| `title.episode.tsv.gz` | 4 | Relations between episodes and their parent TV series, including season and episode numbers. |
| `title.principals.tsv.gz` | 6 | Main cast and crew information for each title, including role category, job, and characters. |
| `title.ratings.tsv.gz` | 3 | IMDb ratings data, including average rating and number of votes. |

### Why this dataset is suitable for the project

The selected IMDb dataset is well suited for a big data project because it combines multiple related tables that can be joined and analyzed together. It includes both descriptive and relational data, which allows us to perform preprocessing, filtering, aggregation, feature engineering, and business-oriented transformations.

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

---
# README - Аналіз великих даних IMDb за допомогою PySpark

## Огляд проєкту

Цей проєкт присвячений масштабній обробці та аналізу датасету IMDb за допомогою PySpark. Основна мета полягає у побудові повного процесу роботи з великими даними, який включає завантаження даних, визначення схеми, попередню обробку, трансформацію, аналіз, створення ознак, оптимізацію та збереження фінальних результатів.

Проєкт розроблений для роботи як у локальному середовищі PySpark, так і в Docker-середовищі, що робить його зручним для розробки, тестування та розгортання.

---

## Датасет

У цьому проєкті використовується офіційний IMDb Non-Commercial Datasets, який поширюється у вигляді стиснених таблично-розділених файлів (`.tsv.gz`). Датасет має кодування UTF-8, оновлюється щодня, а `\N` використовується для позначення пропущених значень.

Для цього проєкту ми обрали **7 файлів IMDb**, які описують назви, людей, рейтинги, епізоди, альтернативні назви та ролі у виробництві.  
Разом ці файли містять **39 ознак**, що робить датасет достатньо насиченим для масштабної обробки, інтеграції та аналітичних завдань у PySpark.

### Обрані файли

| Файл | Кількість ознак | Опис |
|------|------------------|------|
| `name.basics.tsv.gz` | 6 | Базова інформація про людей у кіноіндустрії, зокрема імена, роки народження та смерті, професії та найвідоміші роботи. |
| `title.akas.tsv.gz` | 8 | Альтернативні назви фільмів і серіалів у різних регіонах та різними мовами. |
| `title.basics.tsv.gz` | 9 | Основна інформація про фільми, серіали та інші типи назв, включаючи тип, назву, роки випуску, тривалість і жанри. |
| `title.crew.tsv.gz` | 3 | Інформація про режисерів і сценаристів для кожної назви. |
| `title.episode.tsv.gz` | 4 | Зв’язки між епізодами та батьківськими телесеріалами, включаючи номер сезону та епізоду. |
| `title.principals.tsv.gz` | 6 | Основний акторський склад і знімальна група для кожної назви, включаючи категорію ролі, роботу та персонажів. |
| `title.ratings.tsv.gz` | 3 | Дані про рейтинги IMDb, включаючи середній рейтинг і кількість голосів. |

### Чому цей датасет підходить для проєкту

Обраний датасет IMDb добре підходить для проєкту з великих даних, оскільки поєднує кілька пов’язаних таблиць, які можна об’єднувати та аналізувати разом. Він містить як описові, так і реляційні дані, що дозволяє виконувати попередню обробку, фільтрацію, агрегацію, створення нових ознак і бізнес-орієнтовані трансформації.

---

## Використані технології

- Python
- PySpark
- Docker
- Git
- GitHub

---

## Учасники

- Kateryna Rubtsova
- Khrystyna Liashenyk
- Sofia Pryslipska
- Yulia Salishcheva
- Sofia Pasichko

---

## Розподіл обов’язків

**Керівник проєкту:** **Yulia Salishcheva**

### Етап 1 — Підготовка

- **Khrystyna Liashenyk** - створення репозиторію, `.gitignore`
- **Kateryna Rubtsova** - опис датасету
- **Sofia Pryslipska** - опис датасету
- **Sofia Pasichko** - підготовка звіту
- **Yulia Salishcheva** - підготовка презентації

Усі учасники брали участь у пошуку датасету, його виборі та встановленні PySpark.

### Етап 2 — Налаштування середовища

- **Kateryna Rubtsova** та **Sofia Pryslipska** - налаштування Dockerfile, `main.py`, конфігурація PySpark, оновлення `.gitignore`
- **Khrystyna Liashenyk** - підготовка `README`
- **Sofia Pasichko** - оформлення звіту
- **Yulia Salishcheva** - оформлення презентації

Усі учасники брали участь у локальному налаштуванні середовища.

### Етап 3 — Етап видобування

- **Kateryna Rubtsova** - реалізація універсального модуля data_loader, створення схеми до name.basics, інтеграція та тестування в main.py.
- **Sofia Pasichko** - main, title.akas, title.basics, оформлення звіту
- **Khrystyna Liashenyk** - main, title.ratings
- **Yulia Salishcheva** - main, title.principals, офомлення README.md
- **Khrystyna Liashenyk** - main, title.ratings, офомлення презентації
