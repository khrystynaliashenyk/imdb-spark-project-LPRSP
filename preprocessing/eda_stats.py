from pyspark.sql import functions as F
from pyspark.sql import DataFrame


def get_metadata(df: DataFrame) -> None:
    print("\n=== METADATA ===")
    print(f"Загальна кількість рядків: {df.count()}")
    print(f"Кількість колонок: {len(df.columns)}")
    df.printSchema()


def get_missing_values(df: DataFrame) -> None:
    print("\n=== MISSING VALUES ===")

    missing_exprs = []

    for col_name, dtype in df.dtypes:
        condition = F.col(col_name).isNull()

        if dtype in ("string",):
            condition = condition | (F.trim(F.col(col_name)) == "")

        elif dtype in ("double", "float"):
            condition = condition | F.isnan(F.col(col_name))

        missing_exprs.append(
            F.count(F.when(condition, 1)).alias(col_name)
        )

    df.select(missing_exprs).show(truncate=False)


def get_duplicates_count(df: DataFrame) -> None:
    print("\n=== DUPLICATES ===")
    total = df.count()
    unique = df.dropDuplicates().count()
    print(f"Кількість дублікатів: {total - unique}")


def get_numerical_stats(df: DataFrame, numerical_cols: list) -> None:
    print("\n=== NUMERICAL STATS ===")
    for col_name in numerical_cols:
        if col_name in df.columns:
            print(f"\n--- Статистика для {col_name} ---")
            df.select(
                F.count(F.col(col_name)).alias("count"),
                F.count(F.when(F.col(col_name).isNull(), 1)).alias("nulls"),
                F.mean(F.col(col_name)).alias("mean"),
                F.stddev(F.col(col_name)).alias("stddev"),
                F.min(F.col(col_name)).alias("min"),
                F.expr(f"percentile_approx({col_name}, 0.5)").alias("median"),
                F.max(F.col(col_name)).alias("max")
            ).show(truncate=False)


def get_categorical_stats(df: DataFrame, categorical_cols: list) -> None:
    print("\n=== CATEGORICAL STATS ===")
    for col_name in categorical_cols:
        if col_name in df.columns:
            print(f"\n--- Найчастіші значення для {col_name} ---")
            df.groupBy(col_name).count().orderBy(F.desc("count")).show(10, truncate=False)