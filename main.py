import os
import sys
from pyspark.sql import SparkSession
from data_loader import load_data
from schemas.schema_name_basics import name_basics_schema


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

    df = load_data(spark, file_path, name_basics_schema)

    print(f"\n=== Schema for {dataset_name} ===")
    df.printSchema()

    print(f"\n=== First 5 rows from {dataset_name} ===")
    df.show(5, truncate=False)

    print(f"\n=== Total number of rows in {dataset_name} ===")
    print(df.count())

    spark.stop()


if __name__ == "__main__":
    main()