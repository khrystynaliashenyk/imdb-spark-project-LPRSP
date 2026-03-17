from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

title_ratings_schema = StructType([
    StructField("tconst", StringType(), True),
    StructField("averageRating", DoubleType(), True),
    StructField("numVotes", IntegerType(), True)
])