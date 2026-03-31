from pyspark.sql import functions as F
from pyspark.sql import DataFrame
from pyspark.sql.types import NumericType


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

def get_missing_values(df: DataFrame) -> None:
    print("\n=== MISSING VALUES ===")

    df = df.withColumn("_row_id", F.monotonically_increasing_id())

    first_id = df.select("_row_id").orderBy("_row_id").first()[0]
    df = df.filter(F.col("_row_id") != first_id).drop("_row_id")

    missing_exprs = []

    for col_name, dtype in df.dtypes:
        col = F.col(col_name)
        condition = col.isNull()

        if dtype == "string":
            condition = condition | (F.trim(col) == "")

        elif dtype in ("double", "float"):
            condition = condition | F.isnan(col)

        missing_exprs.append(
            F.count(F.when(condition, 1)).alias(col_name)
        )

    df.select(missing_exprs).show(truncate=False)


def get_duplicates_count(df: DataFrame) -> None:
    print("\n=== DUPLICATES ===")
    total = df.count()
    unique = df.dropDuplicates().count()
    print(f"Кількість дублікатів: {total - unique}")


def get_categorical_stats(df: DataFrame, categorical_cols: list) -> None:
    print("\n=== CATEGORICAL STATS ===")
    for col_name in categorical_cols:
        if col_name in df.columns:
            print(f"\n--- Найчастіші значення для {col_name} ---")
            df.groupBy(col_name).count().orderBy(F.desc("count")).show(10, truncate=False)

def analyze_feature_informativeness(df: DataFrame, numerical_cols: list, categorical_cols: list):


   print("\n=== FEATURE INFORMATIVENESS ===")
   total_rows = df.count()


   print("\n--- Числові ознаки ---")
   for col_name in numerical_cols:


       stats = df.select(F.stddev(F.col(col_name)).alias("stddev")).collect()[0]
       stddev = stats["stddev"]


       if stddev is None or stddev == 0:
           print(f"{col_name}: неінформативна (константа)")
       elif stddev < 0.01:
           print(f"{col_name}: слабка варіативність")
       else:
           print(f"{col_name}: інформативна")


   print("\n--- Категоріальні ознаки ---")
   for col_name in categorical_cols:


       if col_name.lower() in ["id", "nconst"]:
           print(f"{col_name}: неінформативна (ідентифікатор)")
           continue


       unique_count = df.select(col_name).distinct().count()
       ratio = unique_count / total_rows


       if ratio > 0.95:
           print(f"{col_name}: неінформативна ")
       elif ratio > 0.8:
           print(f"{col_name}: слабко інформативна")
       else:
           print(f"{col_name}: інформативна")

def get_column_types(df):
    numerical_cols = [f.name for f in df.schema.fields if isinstance(f.dataType, NumericType)]
    categorical_cols = [f.name for f in df.schema.fields if f.dataType.simpleString() == "string"]
    return numerical_cols, categorical_cols

import os
import matplotlib.pyplot as plt
import seaborn as sns
from pyspark.sql import DataFrame

OUTPUT_PLOT_DIR = "plots"


def plot_numerical_feature(df: DataFrame, col_name: str, dataset_name: str = "") -> None:
    os.makedirs(OUTPUT_PLOT_DIR, exist_ok=True)

    pd_df = df.select(col_name).dropna().toPandas()

    if pd_df.empty:
        return

    lower_bound = pd_df[col_name].quantile(0.01)
    upper_bound = pd_df[col_name].quantile(0.99)

    filtered_df = pd_df[
        (pd_df[col_name] >= lower_bound) &
        (pd_df[col_name] <= upper_bound)
    ]

    plt.figure(figsize=(10, 6))
    sns.histplot(filtered_df[col_name], kde=True, color="skyblue")

    title = f"{dataset_name} - {col_name}" if dataset_name else col_name
    plt.title(title)

    plt.xlim(lower_bound, upper_bound)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    file_path = os.path.join(OUTPUT_PLOT_DIR, f"{dataset_name}_{col_name}.png")
    plt.savefig(file_path)
    plt.close()

    print(f"Графік збережено: {file_path}")


def run_numerical_plots(df: DataFrame, numerical_cols: list, dataset_name: str = "") -> None:
    print("\n=== GENERATING PLOTS ===")

    for col_name in numerical_cols:
        if col_name in df.columns:
            print(f"Plot: {col_name}")
            plot_numerical_feature(df, col_name, dataset_name)