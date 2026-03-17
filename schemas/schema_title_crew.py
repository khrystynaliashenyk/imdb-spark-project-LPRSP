from pyspark.sql.types import StructType, StructField, StringType

title_crew_schema = StructType([
    StructField("tconst", StringType(), True),
    StructField("directors", StringType(), True),
    StructField("writers", StringType(), True)
])