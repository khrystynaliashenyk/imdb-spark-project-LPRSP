import os
import sys
from pyspark.sql import SparkSession


def main():
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

    spark = (
        SparkSession.builder
        .appName("IMDB-Docker-Test")
        .config("spark.driver.host", "localhost")
        .getOrCreate()
    )

    print("\n=== Spark Session started successfully ===")
    print("Application name:", spark.sparkContext.appName)
    print("Spark version:", spark.version)

    sample_data = [
        ("Initialization", "Successful"),
        ("Container", "Running"),
        ("PySpark", "Ready")
    ]

    df = spark.createDataFrame(sample_data, ["Component", "Status"])

    print("\n--- Sample DataFrame Preview ---")
    df.show(truncate=False)

    print("\n=== Execution completed successfully ===\n")

    spark.stop()


if __name__ == "__main__":
    main()