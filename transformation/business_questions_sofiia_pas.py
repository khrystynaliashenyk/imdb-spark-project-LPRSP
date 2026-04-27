from pyspark.sql import functions as F
from pyspark.sql.window import Window


def question_1_ua_movies_2024(title_basics_df, title_akas_df):

    ua_titles = title_akas_df.filter(F.col("region") == "UA").select(F.col("titleId").alias("tconst_ua")).distinct()

    result_df = (
        title_basics_df
        .filter((F.col("titleType") == "movie") & (F.col("startYear") == 2024))
        .join(F.broadcast(ua_titles), title_basics_df.tconst == ua_titles.tconst_ua, "inner")
        .select("primaryTitle", "startYear", "genres")
    )

    print("\n=== План виконання для Q1 (Explain) ===")
    result_df.explain()

    return result_df


def question_2_longest_tv_series_post_2020(title_basics_df):

    window_spec = Window.orderBy(F.desc("runtimeMinutes"))

    result = (
        title_basics_df
        .filter(
            (F.col("titleType") == "tvSeries") &
            (F.col("startYear") > 2020) &
            (F.col("runtimeMinutes").isNotNull())
        )
        .withColumn("runtimeMinutes", F.col("runtimeMinutes").cast("int"))
        .withColumn("rank", F.row_number().over(window_spec))
        .filter(F.col("rank") <= 10)
        .select("primaryTitle", "startYear", "runtimeMinutes")
    )

    print("\n=== План виконання для Q2 (Explain + Window) ===")
    result.explain()
    return result


def question_3_akas_count_by_type(title_basics_df, title_akas_df):

    basics_small = title_basics_df.select("tconst", "titleType")

    result = (
        title_akas_df
        .select("titleId")
        .join(F.broadcast(basics_small), title_akas_df.titleId == basics_small.tconst)
        .groupBy("titleType")
        .agg(F.count("*").alias("akasCount"))
        .orderBy(F.desc("akasCount"))
    )

    print("\n=== План виконання для Q3 (Explain) ===")
    result.explain()
    return result


def question_4_avg_runtime_by_genre_2023(title_basics_df):

    result = (
        title_basics_df
        .filter(
            (F.col("titleType") == "movie") &
            (F.col("startYear") == 2023) &
            (F.col("runtimeMinutes").isNotNull())
        )
        .withColumn("runtimeMinutes", F.col("runtimeMinutes").cast("int"))
        .withColumn("genre", F.explode(F.split(F.col("genres"), ",")))
        .groupBy("genre")
        .agg(F.round(F.avg("runtimeMinutes"), 2).alias("avgRuntime"))
        .orderBy(F.desc("avgRuntime"))
    )

    print("\n=== План виконання для Q4 (Explain) ===")
    result.explain()
    return result


def question_5_top_translated_movies(title_basics_df, title_akas_df):

    akas_counts = title_akas_df.groupBy("titleId").agg(F.count("*").alias("translationCount"))

    result = (
        title_basics_df
        .filter(F.col("titleType") == "movie")
        .select("tconst", "primaryTitle")
        .join(akas_counts, title_basics_df.tconst == akas_counts.titleId)
        .orderBy(F.desc("translationCount"))
        .limit(10)
    )

    print("\n=== План виконання для Q5 (Explain) ===")
    result.explain()
    return result


def question_6_top_rated_movie_per_year(title_basics_df, title_ratings_df):

    window_spec = Window.partitionBy("startYear").orderBy(F.desc("averageRating"), F.desc("numVotes"))

    result = (
        title_basics_df
        .filter(
            (F.col("titleType") == "movie") &
            (F.col("startYear").between(2020, 2024))
        )
        .join(F.broadcast(title_ratings_df), "tconst")
        .withColumn("rank", F.rank().over(window_spec))
        .filter(F.col("rank") == 1)
        .select("startYear", "primaryTitle", "averageRating")
        .orderBy(F.desc("startYear"))
    )

    print("\n=== План виконання для Q6 (Explain + Window) ===")
    result.explain()
    return result