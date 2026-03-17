from pyspark.sql.types import StructType, StructField, StringType

title_episode_schema = StructType([
    StructField("tconst", StringType(), True),
    StructField("parentTconst", StringType(), True),
    StructField("seasonNumber", StringType(), True),
    StructField("episodeNumber", StringType(), True)
])