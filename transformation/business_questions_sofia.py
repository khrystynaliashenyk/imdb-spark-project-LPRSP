from pyspark.sql import functions as F
from pyspark.sql.window import Window

def question_1_top_series_episodes(title_basics_df, title_episode_df):
    basics_filtered = title_basics_df.filter(
        (F.col("titleType") == "tvSeries") &
        (F.col("genres").isNotNull())
    ).select("tconst", "primaryTitle", "genres")

    episode_counts = (
        title_episode_df
        .groupBy("parentTconst")
        .agg(F.count("tconst").alias("total_episodes"))
    )

    genre_window = Window.partitionBy("genre").orderBy(F.desc("total_episodes"))

    result = (
        basics_filtered
        .withColumn("genre", F.explode(F.split(F.col("genres"), ",")))
        .join(
            episode_counts,
            basics_filtered.tconst == episode_counts.parentTconst,
            "inner"
        )
        .withColumn("rank", F.row_number().over(genre_window))
        .filter(F.col("rank") <= 3)
        .select("genre", "primaryTitle", "total_episodes", "rank")
        .orderBy("genre", "rank")
    )

    result.explain()
    return result

def question_2_longest_episode_per_season(title_basics_df, title_episode_df):
    basics_filtered = title_basics_df.filter(
        (F.col("titleType") == "tvEpisode") &
        (F.col("startYear") > 2010) &
        (F.col("runtimeMinutes").isNotNull())
    ).select("tconst", "primaryTitle", "runtimeMinutes")

    episodes_filtered = title_episode_df.filter(
        F.col("seasonNumber").isNotNull()
    ).select("tconst", "seasonNumber")

    season_window = Window.partitionBy("seasonNumber").orderBy(F.desc("runtimeMinutes"))

    result = (
        basics_filtered
        .join(episodes_filtered, "tconst", "inner")
        .withColumn("rank", F.row_number().over(season_window))
        .filter(F.col("rank") == 1)
        .select("seasonNumber", "primaryTitle", "runtimeMinutes", "rank")
        .orderBy("seasonNumber")
    )

    result.explain()
    return result

def question_3_movies_no_writers(title_basics_df, title_crew_df):
    basics_filtered = title_basics_df.filter(
        (F.col("titleType") == "movie") &
        (F.col("startYear") >= 2000)
    ).select("tconst", "startYear")

    crew_filtered = title_crew_df.filter(
        F.col("writers").isNull()
    ).select("tconst")

    result = (
        basics_filtered
        .join(crew_filtered, "tconst", "inner")
        .groupBy("startYear")
        .agg(F.count("tconst").alias("movies_without_writers"))
        .orderBy("startYear")
    )

    result.explain()
    return result

def question_4_longest_movies_per_year(title_basics_df):
    year_window = Window.partitionBy("startYear").orderBy(F.desc("runtimeMinutes"))

    result = (
        title_basics_df
        .filter(
            (F.col("titleType") == "movie") &
            (F.col("startYear") >= 2015) &
            (F.col("runtimeMinutes").isNotNull())
        )
        .withColumn("rank", F.row_number().over(year_window))
        .filter(F.col("rank") <= 5)
        .select("startYear", "primaryTitle", "runtimeMinutes", "rank")
        .orderBy(F.desc("startYear"), "rank")
    )

    result.explain()
    return result

def question_5_multiple_directors(title_basics_df, title_crew_df):
    basics_filtered = title_basics_df.filter(
        (F.col("titleType") == "movie") &
        (F.col("startYear") >= 2014)
    ).select("tconst", "startYear")

    crew_filtered = title_crew_df.filter(
        F.col("directors").isNotNull() &
        F.col("directors").contains(",")
    ).select("tconst")

    result = (
        basics_filtered
        .join(crew_filtered, "tconst", "inner")
        .groupBy("startYear")
        .agg(F.count("tconst").alias("co_directed_movies_count"))
        .orderBy(F.desc("startYear"))
    )

    result.explain()
    return result

def question_6_max_seasons_series(title_basics_df, title_episode_df):
    basics_filtered = (
        title_basics_df
        .filter(F.col("titleType") == "tvSeries")
        .select("tconst", "primaryTitle")
    )

    episodes_filtered = (
        title_episode_df
        .filter(F.col("seasonNumber").isNotNull())
        .select("parentTconst", "seasonNumber")
    )

    result = (
        basics_filtered
        .join(
            episodes_filtered,
            basics_filtered.tconst == episodes_filtered.parentTconst,
            "inner"
        )
        .groupBy(basics_filtered.tconst, "primaryTitle")
        .agg(F.max("seasonNumber").alias("max_seasons"))
        .orderBy(F.desc("max_seasons"))
        .limit(15)
        .select("primaryTitle", "max_seasons")
    )

    result.explain()
    return result