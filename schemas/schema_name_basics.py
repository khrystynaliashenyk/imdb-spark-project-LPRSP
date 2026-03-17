from pyspark.sql.types import StructType, StructField, StringType


name_basics_schema = StructType([
    StructField("nconst", StringType(), True),
    StructField("primaryName", StringType(), True),
    StructField("birthYear", StringType(), True),
    StructField("deathYear", StringType(), True),
    StructField("primaryProfession", StringType(), True),
    StructField("knownForTitles", StringType(), True)
])