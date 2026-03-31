from pyspark.sql import functions as F
from pyspark.sql import DataFrame


def get_metadata(df: DataFrame) -> None:
    print("\n=== METADATA ===")
    print(f"Загальна кількість рядків: {df.count()}")
    print(f"Кількість колонок: {len(df.columns)}")
    df.printSchema()

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

