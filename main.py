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
from preprocessing.preprocessing_files import preprocess_name_basics
from preprocessing.preprocessing_files import preprocess_title_akas, preprocess_title_basics
from preprocessing.eda_stats import (
    get_metadata,
    get_numerical_stats,
    get_missing_values,
    get_duplicates_count,
    get_categorical_stats
)


def main():
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

    spark = (
        SparkSession.builder
        .appName("IMDB-Extraction-Stage")
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

    print(f"\n=== RAW DATA: {dataset_name} ===")
    df.printSchema()
    df.show(5, truncate=False)
    print(f"Total number of rows in {dataset_name}: {df.count()}")

    df = preprocess_name_basics(df)

    print(f"\n=== PREPROCESSED DATA: {dataset_name} ===")
    get_metadata(df)
    get_numerical_stats(df, ["birthYear", "deathYear", "professionCount", "knownTitlesCount"])
    get_missing_values(df)
    get_duplicates_count(df)
    get_categorical_stats(df, ["primaryProfession"])

    df1 = load_data(spark, file_path1, title_akas_schema)

    print(f"\n=== RAW DATA: {dataset_name1} ===")
    df1.printSchema()
    df1.show(5, truncate=False)
    print(f"Total number of rows in {dataset_name1}: {df1.count()}")

    df1 = preprocess_title_akas(df1)

    print(f"\n=== PREPROCESSED DATA: {dataset_name1} ===")
    df1.printSchema()
    df1.show(5, truncate=False)
    get_metadata(df1)
    get_numerical_stats(df1, ["ordering", "typesCount", "attributesCount"])
    get_missing_values(df1)
    get_duplicates_count(df1)
    get_categorical_stats(df1, ["region", "language", "types"])

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


    df3 = load_data(spark, file_path3, title_crew_schema)

    print(f"\n=== RAW DATA: {dataset_name3} ===")
    df3.printSchema()
    df3.show(5, truncate=False)
    print(f"Total number of rows in {dataset_name3}: {df3.count()}")

    df3 = preprocess_title_crew(df3)

    print(f"\n=== PREPROCESSED DATA: {dataset_name3} ===")
    get_metadata(df3)
    get_numerical_stats(df3, ["directorsCount", "writersCount"])
    get_missing_values(df3)
    get_duplicates_count(df3)
    get_categorical_stats(df3, ["directors", "writers"])

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
    get_categorical_stats(df3, ["directors", "writers"])

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

    df6 = load_data(spark, file_path6, title_ratings_schema)
    print(f"\n=== Schema for {dataset_name6} ===")
    df6.printSchema()
    print(f"\n=== First 5 rows from {dataset_name6} ===")
    df6.show(5, truncate=False)
    print(f"\n=== Total number of rows in {dataset_name6} ===")
    print(df6.count())

    spark.stop()


if __name__ == "__main__":
    main()