from pyspark.sql.types import StructType, StructField, StringType, IntegerType

title_basics_schema = StructType([
    StructField("tconst", StringType(), True),
    StructField("titleType", StringType(), True),
    StructField("primaryTitle", StringType(), True),
    StructField("originalTitle", StringType(), True),
    StructField("isAdult", IntegerType(), True),
    StructField("startYear", StringType(), True),
    StructField("endYear", StringType(), True),
    StructField("runtimeMinutes", StringType(), True),
    StructField("genres", StringType(), True)
])