import os
import sys
from pyspark.sql import SparkSession
from data_loader import load_data
from schemas.schema_name_basics import name_basics_schema
from schemas.schema_title_akas import title_akas_schema
from schemas.schema_title_basics import title_basics_schema
from schemas.schema_title_crew import title_crew_schema
from schemas.schema_title_episode import title_episode_schema
from schemas.schema_title_principals import title_principals_schema
from schemas.schema_title_ratings import title_ratings_schema
from preprocessing.preprocessing_files import preprocess_name_basics, preprocess_title_ratings
from preprocessing.preprocessing_files import preprocess_title_akas, preprocess_title_basics, preprocess_title_crew, preprocess_title_episode, preprocess_title_principals
from preprocessing.eda_stats import (
    get_metadata,
    get_numerical_stats,
    get_missing_values,
    get_duplicates_count,
    get_categorical_stats,
    analyze_feature_informativeness, get_column_types
)
from pyspark.sql.types import NumericType
from preprocessing.eda_stats import run_numerical_plots

from transformation.business_questions_katya import (
   question_1_top_modern_genres,
   question_2_runtime_rating,
   question_3_top_actors,
   question_4_rating_by_year,
   question_5_top_movies_by_genre,
   question_6_top_movie_each_year
)

from transformation.business_questions_sofia import (
    question_1_top_series_episodes,
    question_2_longest_episode_per_season,
    question_3_movies_no_writers,
    question_4_longest_movies_per_year,
    question_5_multiple_directors,
    question_6_max_seasons_series
)
from transformation import business_questions_yuliia as bq

from transformation.business_questions_sofiia_pas import (
    question_1_ua_movies_2024,
    question_2_longest_tv_series_post_2020,
    question_3_akas_count_by_type,
    question_4_avg_runtime_by_genre_2023,
    question_5_top_translated_movies,
    question_6_top_rated_movie_per_year
)

from transformation.business_questions_khrystyna import (
   question_1_debut_directors,
   question_2_top5_genres_by_decade,
   question_3_writer_quality_index,
   question_4_high_rated_per_year,
   question_5_avg_rating_by_country,
   question_6_actors_by_total_votes
)

def save_to_csv(df, output_path):
    (
        df.coalesce(1)
        .write
        .mode("overwrite")
        .option("header", "true")
        .csv(output_path)
    )


def main():
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

    spark = (
        SparkSession.builder
        .appName("IMDB-Extraction-Stage")
        .config("spark.driver.memory", "4g")
        .config("spark.executor.memory", "4g")
        .config("spark.sql.shuffle.partitions", "10")
        .config("spark.driver.host", "localhost")
        .getOrCreate()
    )

    dataset_name = "name.basics"
    file_path = "/data/name.basics.tsv.gz"

    dataset_name1 = "title.akas"
    file_path1 = "/data/title.akas.tsv.gz"

    dataset_name2 = "title.basics"
    file_path2 = "/data/title.basics.tsv.gz"

    dataset_name3 = "title.crew"
    file_path3 = "/data/title.crew.tsv.gz"

    dataset_name4 = "title.episode"
    file_path4 = "/data/title.episode.tsv.gz"

    dataset_name5 = "title.principals"
    file_path5 = "/data/title.principals.tsv.gz"

    dataset_name6 = "title.ratings"
    file_path6 = "/data/title.ratings.tsv.gz"

    df = load_data(spark, file_path, name_basics_schema)

    # На цьому етапі RAW DATA виводити не потрібно
    print(f"\n=== RAW DATA: {dataset_name} ===")
    df.printSchema()
    df.show(5, truncate=False)
    print(f"Total number of rows in {dataset_name}: {df.count()}")

    df = preprocess_name_basics(df)

    # EDA для name.basics на цьому етапі не потрібне
    print(f"\n=== PREPROCESSED DATA: {dataset_name} ===")
    get_metadata(df)
    get_numerical_stats(df, ["birthYear", "deathYear", "professionCount", "knownTitlesCount"])
    get_missing_values(df)
    get_duplicates_count(df)
    get_categorical_stats(df, ["primaryProfession"])
    numerical_cols, categorical_cols = get_column_types(df)
    analyze_feature_informativeness(df, numerical_cols, categorical_cols)
    run_numerical_plots(
         df,
         ["birthYear", "deathYear", "professionCount", "knownTitlesCount"],
         dataset_name="name_basics"
     )

    df1 = load_data(spark, file_path1, title_akas_schema)

    print(f"\n=== RAW DATA: {dataset_name1} ===")
    df1.printSchema()
    df1.show(5, truncate=False)
    print(f"Total number of rows in {dataset_name1}: {df1.count()}")

    df1 = preprocess_title_akas(df1)

    # EDA для title.akas на цьому етапі не потрібне
    print(f"\n=== PREPROCESSED DATA: {dataset_name1} ===")
    df1.printSchema()
    df1.show(5, truncate=False)
    get_metadata(df1)
    get_numerical_stats(df1, ["ordering", "typesCount", "attributesCount"])
    get_missing_values(df1)
    get_duplicates_count(df1)
    get_categorical_stats(df1, ["region", "language", "types"])
    numerical_cols, categorical_cols = get_column_types(df1)
    analyze_feature_informativeness(df1, numerical_cols, categorical_cols)
    run_numerical_plots(
        df1,
        ["ordering", "typesCount", "attributesCount"],
        dataset_name="title_akas"
    )

    df2 = load_data(spark, file_path2, title_basics_schema)

    print(f"\n=== RAW DATA: {dataset_name2} ===")
    df2.printSchema()
    df2.show(5, truncate=False)
    print(f"Total number of rows in {dataset_name2}: {df2.count()}")

    df2 = preprocess_title_basics(df2)

    print(f"\n=== PREPROCESSED DATA: {dataset_name2} ===")
    df2.printSchema()
    df2.show(5, truncate=False)
    get_metadata(df2)
    get_numerical_stats(df2, ["startYear", "endYear", "runtimeMinutes", "genresCount"])
    get_missing_values(df2)
    get_duplicates_count(df2)
    get_categorical_stats(df2, ["titleType", "isAdult", "genres"])
    numerical_cols, categorical_cols = get_column_types(df2)

    analyze_feature_informativeness(df2, numerical_cols, categorical_cols)

    run_numerical_plots(
        df2,
        ["startYear", "endYear", "runtimeMinutes", "genresCount"],
        dataset_name="title_basics"
    )

    df3 = load_data(spark, file_path3, title_crew_schema)

    print(f"\n=== RAW DATA: {dataset_name3} ===")
    df3.printSchema()
    df3.show(5, truncate=False)
    print(f"Total number of rows in {dataset_name3}: {df3.count()}")

    df3 = preprocess_title_crew(df3)

    # EDA для title.crew на цьому етапі не потрібне
    print(f"\n=== PREPROCESSED DATA: {dataset_name3} ===")
    get_metadata(df3)
    get_numerical_stats(df3, ["directorsCount", "writersCount"])
    get_missing_values(df3)
    get_duplicates_count(df3)
    get_categorical_stats(df3, ["directors", "writers"])
    numerical_cols, categorical_cols = get_column_types(df3)
    analyze_feature_informativeness(df3, numerical_cols, categorical_cols)
    run_numerical_plots(
        df3,
        ["directorsCount", "writersCount"],
        dataset_name="title_crew"
    )

    df4 = load_data(spark, file_path4, title_episode_schema)

    print(f"\n=== RAW DATA: {dataset_name4} ===")
    df4.printSchema()
    df4.show(5, truncate=False)
    print(f"Total number of rows in {dataset_name4}: {df4.count()}")

    df4 = preprocess_title_episode(df4)

    print(f"\n=== PREPROCESSED DATA: {dataset_name4} ===")
    get_metadata(df4)
    get_numerical_stats(df4, ["seasonNumber", "episodeNumber"])
    get_missing_values(df4)
    get_duplicates_count(df4)
    get_categorical_stats(df4, ["directors", "writers"])
    numerical_cols, categorical_cols = get_column_types(df4)

    analyze_feature_informativeness(df4, numerical_cols, categorical_cols)

    run_numerical_plots(
        df4,
        ["seasonNumber", "episodeNumber"],
        dataset_name="title_episode"
    )

    df5 = load_data(spark, file_path5, title_principals_schema)

    print(f"\n=== RAW DATA: {dataset_name5} ===")
    df5.printSchema()
    df5.show(5, truncate=False)
    print(f"Total number of rows in {dataset_name5}: {df5.count()}")

    df5 = preprocess_title_principals(df5)

    print(f"\n=== PREPROCESSED DATA: {dataset_name5} ===")
    get_metadata(df5)
    get_numerical_stats(df5, ["ordering", "jobCount", "charactersCount"])
    get_missing_values(df5)
    get_duplicates_count(df5)
    get_categorical_stats(df5, ["category", "job"])
    numerical_cols, categorical_cols = get_column_types(df5)

    analyze_feature_informativeness(df5, numerical_cols, categorical_cols)

    run_numerical_plots(
        df5,
        ["ordering", "jobCount", "charactersCount"],
        dataset_name="title_principals"
    )

    df6 = load_data(spark, file_path6, title_ratings_schema)

    print(f"\n=== RAW DATA: {dataset_name6} ===")
    df6.printSchema()
    df6.show(5, truncate=False)
    print(f"Total number of rows in {dataset_name6}: {df6.count()}")
    df6 = preprocess_title_ratings(df6)

    print(f"\n=== PREPROCESSED DATA: {dataset_name6} ===")
    get_metadata(df6)

    numerical_stats_cols = ["averageRating", "numVotes", "weightedScore"]
    get_numerical_stats(df6, [c for c in numerical_stats_cols if c in df6.columns])

    get_missing_values(df6)
    get_duplicates_count(df6)
    numerical_cols, categorical_cols = get_column_types(df6)

    analyze_feature_informativeness(df6, numerical_cols, categorical_cols)
    run_numerical_plots(
        df6,
        ["averageRating", "numVotes", "weightedScore"],
        dataset_name="title_ratings"
    )

    print("\n=== TRANSFORMATION STAGE ===")

    print("\n=== Q1: Які жанри фільмів після 2010 року мають найвищий середній рейтинг? ===")
    q1 = question_1_top_modern_genres(df2, df6)
    q1.show(20, truncate=False)
    save_to_csv(q1, "results/katya_q1_top_modern_genres")

    print("\n=== Q2: Як тривалість фільму впливає на його рейтинг? ===")
    q2 = question_2_runtime_rating(df2, df6)
    q2.show(20, truncate=False)
    save_to_csv(q2, "results/katya_q2_runtime_rating")

    print("\n=== Q3: Які актори мають найвищий середній рейтинг, якщо вони знялися мінімум у 10 фільмах? ===")
    q3 = question_3_top_actors(df, df5, df6)
    q3.show(20, truncate=False)
    save_to_csv(q3, "results/katya_q3_top_actors")

    print("\n=== Q4: Як змінювався середній рейтинг фільмів по роках? ===")
    q4 = question_4_rating_by_year(df2, df6)
    q4.show(65, truncate=False)
    save_to_csv(q4, "results/katya_q4_rating_by_year")

    print("\n=== Q5: Які ТОП-3 фільми в кожному жанрі за рейтингом? ===")
    q5 = question_5_top_movies_by_genre(df2, df6)
    q5.show(100, truncate=False)
    save_to_csv(q5, "results/katya_q5_top_movies_by_genre")

    print("\n=== Q6: Який фільм був найрейтинговішим у кожному році? ===")
    q6 = question_6_top_movie_each_year(df2, df6)
    q6.show(100, truncate=False)
    save_to_csv(q6, "results/katya_q6_top_movie_each_year")


    print("\n=== Q1: Які 3 серіали у кожному кіножанрі мають найбільшу загальну кількість випущених епізодів? ===")
    q1 = question_1_top_series_episodes(df2, df4)
    q1.show(20, truncate=False)

    print("\n=== Q2: Який епізод має найбільшу тривалість у кожному сезоні? ===")
    q2 = question_2_longest_episode_per_season(df2, df4)
    q2.show(20, truncate=False)

    print("\n=== Q3: Скільки фільмів випущено без сценаристів? ===")
    q3 = question_3_movies_no_writers(df2, df3)
    q3.show(20, truncate=False)

    print("\n=== Q4: Які 5 найдовших фільмів кожного року? ===")
    q4 = question_4_longest_movies_per_year(df2)
    q4.show(20, truncate=False)

    print("\n=== Q5: Фільми у 'режисерському співавторстві'? ===")
    q5 = question_5_multiple_directors(df2, df3)
    q5.show(20, truncate=False)

    print("\n=== Q6: Які серіали мають найбільшу кількість сезонів? ===")
    q6 = question_6_max_seasons_series(df2, df4)
    q6.show(20, truncate=False)

    print("\n=== Q1: Фільми з високим рейтингом, але малою кількістю голосів: ===")
    bq.high_rating_low_votes(df2, df6).explain()
    bq.high_rating_low_votes(df2, df6).show(10)

    print("\n=== Q2: Найкращий фільм у кожному жанрі за рейтингом:  ===")
    bq.best_movie_per_genre(df2, df6).explain()
    bq.best_movie_per_genre(df2, df6).show(10)

    print("\n=== Q3: Медіанна тривалість фільмів у кожному жанрі:  ===")
    bq.median_runtime_per_genre(df2).explain()
    bq.median_runtime_per_genre(df2).show(10)

    print("\n=== Q4: Ефективність жанрів (Рейтинг / Тривалість):  ===")
    bq.genre_efficiency(df2, df6).explain()
    bq.genre_efficiency(df2, df6).show(10)

    print("\n=== Q5: Фільми-рекордсмени (Довгі та високий рейтинг):  ===")
    bq.epic_high_rated_movies(df2, df6).explain()
    bq.epic_high_rated_movies(df2, df6).show(10)

    print("\n=== Q6: Порівняння ер: Класика vs Сучасність:  ===")
    bq.old_vs_new_genres(df2, df6).explain()
    bq.old_vs_new_genres(df2, df6).show(10)

    print("\n=== Q1: Фільми 2024 року з українською локалізацією ===")
    sq1 = question_1_ua_movies_2024(df2, df1)
    sq1.show(10, truncate=False)

    print("\n=== Q2: Топ-10 найдовших серіалів (tvSeries), випущених після 2020 року ===")
    sq2 = question_2_longest_tv_series_post_2020(df2)
    sq2.show(10, truncate=False)

    print("\n=== Q3: Кількість записів у файлі akas для кожного типу контенту ===")
    sq3 = question_3_akas_count_by_type(df2, df1)
    sq3.show(20, truncate=False)

    print("\n=== Q4: Середня тривалість фільмів для кожного жанру (тільки 2023 рік) ===")
    sq4 = question_4_avg_runtime_by_genre_2023(df2)
    sq4.show(50, truncate=False)

    print("\n=== Q5: Топ-10 фільмів з найбільшою кількістю назв (перекладів) у akas ===")
    sq5 = question_5_top_translated_movies(df2, df1)
    sq5.show(10, truncate=False)

    print("\n=== Q6: Найрейтинговіший фільм кожного року (2020-2024) ===")
    sq6 = question_6_top_rated_movie_per_year(df2, df6)
    sq6.show(10, truncate=False)

    print("\n=== TRANSFORMATION STAGE ===")

    print("\n=== Q1: Найвищий рейтинговий дебютний фільм режисера ===")
    q1 = question_1_debut_directors(df2, df3, df6, df)
    q1.show(20, truncate=False)

    print("\n=== Q2: Топ-5 жанрів по десятиліттях з 1980-го ===")
    q2 = question_2_top5_genres_by_decade(df2, df6)
    q2.show(50, truncate=False)

    print("\n=== Q3: Сценаристи з найвищим індексом якості (мін. 8 фільмів) ===")
    q3 = question_3_writer_quality_index(df3, df2, df6, df)
    q3.show(20, truncate=False)

    print("\n=== Q4: Скільки фільмів щороку отримують рейтинг вище 8.0? ===")
    q4 = question_4_high_rated_per_year(df2, df6)
    q4.show(50, truncate=False)

    print("\n=== Q5: Середній рейтинг фільмів за країною виробництва ===")
    q5 = question_5_avg_rating_by_country(df1, df2, df6)
    q5.show(20, truncate=False)

    print("\n=== Q6: Актори у фільмах з найбільшою сумарною кількістю голосів ===")
    q6 = question_6_actors_by_total_votes(df5, df2, df6, df)
    q6.show(20, truncate=False)

    spark.stop()

if __name__ == "__main__":
    main()