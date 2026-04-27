from pyspark.sql import functions as F
from pyspark.sql.window import Window

MIN_VOTES = 10000

def question_1_top_modern_genres(title_basics_df, title_ratings_df):
   result = (
       title_basics_df
       .select("tconst", "titleType", "startYear", "genres")
       .join(
           title_ratings_df.select("tconst", "averageRating", "numVotes"),
           "tconst"
       )
       .filter(
           (F.col("titleType") == "movie") &
           (F.col("startYear") >= 2010) &
           (F.col("genres").isNotNull()) &
           (F.col("numVotes") >= MIN_VOTES)
       )
       .withColumn("genre", F.explode(F.split(F.col("genres"), ",")))
       .groupBy("genre")
       .agg(
           F.round(F.avg("averageRating"), 2).alias("avgRating"),
           F.count("*").alias("moviesCount")
       )
       .filter(F.col("moviesCount") >= 20)
       .orderBy(F.desc("avgRating"))
   )

   result.explain()
   return result

def question_2_runtime_rating(title_basics_df, title_ratings_df):
   result = (
       title_basics_df
       .select("tconst", "titleType", "runtimeMinutes")
       .join(
           title_ratings_df.select("tconst", "averageRating", "numVotes"),
           "tconst"
       )
       .filter(
           (F.col("titleType") == "movie") &
           (F.col("runtimeMinutes").isNotNull()) &
           (F.col("averageRating").isNotNull()) &
           (F.col("numVotes") >= MIN_VOTES)
       )
       .withColumn(
           "runtimeCategory",
           F.when(F.col("runtimeMinutes") < 60, "short")
            .when(F.col("runtimeMinutes") <= 120, "medium")
            .otherwise("long")
       )
       .groupBy("runtimeCategory")
       .agg(
           F.round(F.avg("averageRating"), 2).alias("avgRating"),
           F.round(F.avg("runtimeMinutes"), 2).alias("avgRuntime"),
           F.count("*").alias("moviesCount")
       )
       .orderBy(F.desc("avgRating"))
   )


   result.explain()
   return result


def question_3_top_actors(name_basics_df, title_principals_df, title_ratings_df):
   popular_ratings = (
       title_ratings_df
       .select("tconst", "averageRating", "numVotes")
       .filter(F.col("numVotes") >= 40000)
   )

   result = (
       title_principals_df
       .select("tconst", "nconst", "category")
       .filter(F.col("category").isin("actor", "actress"))
       .join(popular_ratings, "tconst")
       .join(name_basics_df.select("nconst", "primaryName"), "nconst")
       .groupBy("nconst", "primaryName")
       .agg(
           F.round(F.avg("averageRating"), 2).alias("avgRating"),
           F.countDistinct("tconst").alias("titlesCount")
       )
       .filter(F.col("titlesCount") >= 5)
       .orderBy(F.desc("avgRating"))
   )

   result.explain()
   return result

def question_4_rating_by_year(title_basics_df, title_ratings_df):
   result = (
       title_basics_df
       .select("tconst", "titleType", "startYear")
       .join(
           title_ratings_df.select("tconst", "averageRating", "numVotes"),
           "tconst"
       )
       .filter(
           (F.col("titleType") == "movie") &
           (F.col("startYear").isNotNull()) &
           (F.col("averageRating").isNotNull()) &
           (F.col("numVotes") >= MIN_VOTES)
       )
       .groupBy("startYear")
       .agg(
           F.round(F.avg("averageRating"), 2).alias("avgRating"),
           F.count("*").alias("moviesCount")
       )
       .filter(F.col("moviesCount") >= 20)
       .orderBy("startYear")
   )

   result.explain()
   return result

def question_5_top_movies_by_genre(title_basics_df, title_ratings_df):
   genre_window = Window.partitionBy("genre").orderBy(
       F.desc("averageRating"),
       F.desc("numVotes")
   )


   result = (
       title_basics_df
       .select("tconst", "titleType", "primaryTitle", "startYear", "genres")
       .join(
           title_ratings_df.select("tconst", "averageRating", "numVotes"),
           "tconst"
       )
       .filter(
           (F.col("titleType") == "movie") &
           (F.col("genres").isNotNull()) &
           (F.col("numVotes") >= MIN_VOTES)
       )
       .withColumn("genre", F.explode(F.split(F.col("genres"), ",")))
       .withColumn("rank", F.row_number().over(genre_window))
       .filter(F.col("rank") <= 3)
       .select(
           "genre",
           "rank",
           "primaryTitle",
           "startYear",
           "averageRating",
           "numVotes"
       )
       .orderBy("genre", "rank")
   )

   result.explain()
   return result


def question_6_top_movie_each_year(title_basics_df, title_ratings_df):
   year_window = Window.partitionBy("startYear").orderBy(
       F.desc("averageRating"),
       F.desc("numVotes")
   )


   result = (
       title_basics_df
       .select("tconst", "titleType", "primaryTitle", "startYear")
       .join(
           title_ratings_df.select("tconst", "averageRating", "numVotes"),
           "tconst"
       )
       .filter(
           (F.col("titleType") == "movie") &
           (F.col("startYear").isNotNull()) &
           (F.col("numVotes") >= MIN_VOTES)
       )
       .withColumn("rank", F.row_number().over(year_window))
       .filter(F.col("rank") == 1)
       .select(
           "startYear",
           "primaryTitle",
           "averageRating",
           "numVotes",
           "rank"
       )
       .orderBy("startYear")
   )

   result.explain()
   return result
