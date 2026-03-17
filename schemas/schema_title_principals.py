from pyspark.sql.types import StructType, StructField, StringType, IntegerType

title_principals_schema = StructType([
    StructField("tconst", StringType(), True),
    StructField("ordering", StringType(), True),
    StructField("nconst", StringType(), True),
    StructField("category", StringType(), True),
    StructField("job", StringType(), True),
    StructField("characters", StringType(), True)
])