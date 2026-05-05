from pyspark.sql import functions as F
from pyspark.sql.window import Window

MIN_VOTES_LIMIT = 10000

def high_rating_low_votes(title_basics_df, title_ratings_df):
    return (
        title_basics_df.filter(F.col("titleType") == "movie")
        .join(title_ratings_df, "tconst")
        .filter((F.col("averageRating") >= 8.5) & (F.col("numVotes") < 500))
        .select("primaryTitle", "startYear", "averageRating", "numVotes")
        .orderBy(F.desc("averageRating"))
    )

def best_movie_per_genre(title_basics_df, title_ratings_df):
    window_spec = Window.partitionBy("genre").orderBy(F.desc("averageRating"), F.desc("numVotes"))
    return (
        title_basics_df.filter(F.col("titleType") == "movie")
        .withColumn("genre", F.explode(F.split(F.col("genres"), ",")))
        .join(title_ratings_df, "tconst")
        .filter(F.col("numVotes") >= MIN_VOTES_LIMIT)
        .withColumn("rank", F.row_number().over(window_spec))
        .filter(F.col("rank") == 1)
        .select("genre", "primaryTitle", "averageRating", "numVotes")
        .orderBy("genre")
    )

def median_runtime_per_genre(title_basics_df):
    return (
        title_basics_df.filter((F.col("titleType") == "movie") & (F.col("runtimeMinutes").isNotNull()))
        .withColumn("genre", F.explode(F.split(F.col("genres"), ",")))
        .groupBy("genre")
        .agg(F.expr("percentile_approx(runtimeMinutes, 0.5)").alias("medianRuntime"))
        .orderBy(F.desc("medianRuntime"))
    )

def genre_efficiency(title_basics_df, title_ratings_df):
    return (
        title_basics_df.filter((F.col("titleType") == "movie") & (F.col("runtimeMinutes").isNotNull()))
        .withColumn("genre", F.explode(F.split(F.col("genres"), ",")))
        .join(title_ratings_df, "tconst")
        .filter(F.col("numVotes") >= MIN_VOTES_LIMIT)
        .groupBy("genre")
        .agg(
            F.avg("averageRating").alias("avgRating"),
            F.avg("runtimeMinutes").alias("avgRuntime")
        )
        .withColumn("efficiency", F.round(F.col("avgRating") / F.col("avgRuntime"), 4))
        .orderBy(F.desc("efficiency"))
    )

def epic_high_rated_movies(title_basics_df, title_ratings_df):
    return (
        title_basics_df.filter((F.col("titleType") == "movie") & (F.col("runtimeMinutes") >= 180))
        .join(title_ratings_df, "tconst")
        .filter(F.col("numVotes") >= MIN_VOTES_LIMIT)
        .select("primaryTitle", "runtimeMinutes", "averageRating")
        .orderBy(F.desc("averageRating"), F.desc("runtimeMinutes"))
    )

def old_vs_new_genres(title_basics_df, title_ratings_df):
    return (
        title_basics_df.filter((F.col("titleType") == "movie") & (F.col("startYear").isNotNull()))
        .withColumn("era", F.when(F.col("startYear") < 1980, "Classic")
                            .when(F.col("startYear") > 2015, "Modern")
                            .otherwise(None))
        .filter(F.col("era").isNotNull())
        .withColumn("genre", F.explode(F.split(F.col("genres"), ",")))
        .join(title_ratings_df, "tconst")
        .filter(F.col("numVotes") >= 5000)
        .groupBy("genre", "era")
        .agg(F.round(F.avg("averageRating"), 2).alias("avgRating"))
        .orderBy("genre", "era")
    )