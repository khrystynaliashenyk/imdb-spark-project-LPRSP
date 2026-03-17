import os
import sys
from pyspark.sql import SparkSession
from data_loader import load_data
from schemas.schema_name_basics import name_basics_schema
from schemas.schema_title_akas import title_akas_schema
from schemas.schema_title_basics import title_basics_schema
from schemas.schema_title_crew import title_crew_schema
from schemas.schema_title_episode import title_episode_schema

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

    df = load_data(spark, file_path, name_basics_schema)

    print(f"\n=== Schema for {dataset_name} ===")
    df.printSchema()

    print(f"\n=== First 5 rows from {dataset_name} ===")
    df.show(5, truncate=False)

    print(f"\n=== Total number of rows in {dataset_name} ===")
    print(df.count())

    df1 = load_data(spark, file_path1, title_akas_schema)

    print(f"\n=== Schema for {dataset_name1} ===")
    df1.printSchema()

    print(f"\n=== First 5 rows from {dataset_name1} ===")
    df1.show(5, truncate=False)

    print(f"\n=== Total number of rows in {dataset_name1} ===")
    print(df1.count())

    df2 = load_data(spark, file_path2, title_basics_schema)

    print(f"\n=== Schema for {dataset_name2} ===")
    df2.printSchema()

    print(f"\n=== First 5 rows from {dataset_name2} ===")
    df2.show(5, truncate=False)

    print(f"\n=== Total number of rows in {dataset_name2} ===")
    print(df2.count())

    df3 = load_data(spark, file_path3, title_crew_schema)
    print(f"\n=== Schema for {dataset_name3} ===")
    df3.printSchema()
    print(f"\n=== First 5 rows from {dataset_name3} ===")
    df3.show(5, truncate=False)
    print(f"\n=== Total number of rows in {dataset_name3} ===")
    print(df3.count())

    df4 = load_data(spark, file_path4, title_episode_schema)
    print(f"\n=== Schema for {dataset_name4} ===")
    df4.printSchema()
    print(f"\n=== First 5 rows from {dataset_name4} ===")
    df4.show(5, truncate=False)
    print(f"\n=== Total number of rows in {dataset_name4} ===")
    print(df4.count())

    spark.stop()


if __name__ == "__main__":
    main()