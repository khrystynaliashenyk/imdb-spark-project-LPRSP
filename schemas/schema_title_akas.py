from pyspark.sql.types import StructType, StructField, StringType, IntegerType

title_akas_schema = StructType([
    StructField("titleId", StringType(), True),
    StructField("ordering", IntegerType(), True),
    StructField("title", StringType(), True),
    StructField("region", StringType(), True),
    StructField("language", StringType(), True),
    StructField("types", StringType(), True),
    StructField("attributes", StringType(), True),
    StructField("isOriginalTitle", IntegerType(), True)
])