from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when, split, size
from pyspark.sql.types import IntegerType


def preprocess_name_basics(df: DataFrame) -> DataFrame:
    # Замінюємо службове позначення пропусків \N на null
    df = df.select([
        when(col(c) == "\\N", None).otherwise(col(c)).alias(c)
        for c in df.columns
    ])

    # Приводимо роки до числового типу
    df = df.withColumn("birthYear", col("birthYear").cast(IntegerType()))
    df = df.withColumn("deathYear", col("deathYear").cast(IntegerType()))

    # Парсинг рядків зі списками у масиви
    df = df.withColumn(
        "primaryProfessionArray",
        when(col("primaryProfession").isNotNull(), split(col("primaryProfession"), ","))
    )

    df = df.withColumn(
        "knownForTitlesArray",
        when(col("knownForTitles").isNotNull(), split(col("knownForTitles"), ","))
    )

    # Додаткові похідні ознаки
    df = df.withColumn(
        "professionCount",
        when(col("primaryProfessionArray").isNotNull(), size(col("primaryProfessionArray")))
    )

    df = df.withColumn(
        "knownTitlesCount",
        when(col("knownForTitlesArray").isNotNull(), size(col("knownForTitlesArray")))
    )

    return df