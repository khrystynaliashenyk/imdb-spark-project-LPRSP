from pyspark.sql import functions as F
from pyspark.sql.window import Window

MIN_VOTES = 10000


def question_1_debut_directors(title_basics_df, title_crew_df, title_ratings_df, name_basics_df):
    """
    Q1: Які режисери зробили найвищий рейтинговий дебютний фільм?
    Використовує: JOIN (x3), FILTER, WINDOW FUNCTION (row_number)
    """
    director_window = Window.partitionBy("nconst").orderBy("startYear")

    directors_exploded = (
        title_crew_df
        .select("tconst", "directors")
        .filter(F.col("directors").isNotNull() & (F.col("directors") != "\\N"))
        .withColumn("nconst", F.explode(F.split(F.col("directors"), ",")))
    )

    result = (
        directors_exploded
        .join(
            title_basics_df
            .select("tconst", "titleType", "primaryTitle", "startYear")
            .filter(
                (F.col("titleType") == "movie") &
                F.col("startYear").isNotNull()
            ),
            "tconst"
        )
        .join(
            title_ratings_df
            .select("tconst", "averageRating", "numVotes")
            .filter(F.col("numVotes") >= MIN_VOTES),
            "tconst"
        )
        .withColumn("debutRank", F.row_number().over(director_window))
        .filter(F.col("debutRank") == 1)
        .join(name_basics_df.select("nconst", "primaryName"), "nconst")
        .select("primaryName", "primaryTitle", "startYear", "averageRating", "numVotes")
        .orderBy(F.desc("averageRating"))
    )

    result.explain()
    return result


def question_2_top5_genres_by_decade(title_basics_df, title_ratings_df):
    """
    Q2: Топ-5 жанрів по десятиліттях з 1980-го за кількістю фільмів.
    Використовує: JOIN, FILTER, GROUP BY, WINDOW FUNCTION (rank)
    """
    decade_window = Window.partitionBy("decade").orderBy(F.desc("moviesCount"))

    result = (
        title_basics_df
        .select("tconst", "titleType", "startYear", "genres")
        .filter(
            (F.col("titleType") == "movie") &
            F.col("startYear").isNotNull() &
            F.col("genres").isNotNull() &
            (F.col("startYear").cast("int") >= 1980)
        )
        .withColumn("decade", (F.floor(F.col("startYear").cast("int") / 10) * 10).cast("string"))
        .join(
            title_ratings_df
            .select("tconst", "averageRating", "numVotes")
            .filter(F.col("numVotes") >= MIN_VOTES),
            "tconst"
        )
        .withColumn("genre", F.explode(F.split(F.col("genres"), ",")))
        .filter(F.col("genre") != "\\N")
        .groupBy("decade", "genre")
        .agg(
            F.count("*").alias("moviesCount"),
            F.round(F.avg("averageRating"), 2).alias("avgRating")
        )
        .withColumn("rank", F.rank().over(decade_window))
        .filter(F.col("rank") <= 5)
        .orderBy("decade", "rank")
    )

    result.explain()
    return result


def question_3_writer_quality_index(title_crew_df, title_basics_df, title_ratings_df, name_basics_df):
    """
    Q3: Сценаристи з найвищим індексом якості (avgRating * filmsCount), мін. 8 фільмів.
    Використовує: JOIN (x2), FILTER, GROUP BY
    """
    writers_exploded = (
        title_crew_df
        .select("tconst", "writers")
        .filter(F.col("writers").isNotNull() & (F.col("writers") != "\\N"))
        .withColumn("nconst", F.explode(F.split(F.col("writers"), ",")))
    )

    result = (
        writers_exploded
        .join(
            title_basics_df
            .select("tconst", "titleType")
            .filter(F.col("titleType") == "movie"),
            "tconst"
        )
        .join(
            title_ratings_df
            .select("tconst", "averageRating", "numVotes")
            .filter(F.col("numVotes") >= MIN_VOTES),
            "tconst"
        )
        .groupBy("nconst")
        .agg(
            F.round(F.avg("averageRating"), 2).alias("avgRating"),
            F.countDistinct("tconst").alias("filmsCount")
        )
        .filter(F.col("filmsCount") >= 8)
        .withColumn("qualityIndex", F.round(F.col("avgRating") * F.col("filmsCount"), 2))
        .join(name_basics_df.select("nconst", "primaryName"), "nconst")
        .select("primaryName", "avgRating", "filmsCount", "qualityIndex")
        .orderBy(F.desc("qualityIndex"))
    )

    result.explain()
    return result


def question_4_high_rated_per_year(title_basics_df, title_ratings_df):
    """
    Q4: Скільки фільмів щороку отримують рейтинг вище 8.0?
    Використовує: JOIN, FILTER, GROUP BY
    """
    result = (
        title_basics_df
        .select("tconst", "titleType", "startYear")
        .filter(
            (F.col("titleType") == "movie") &
            F.col("startYear").isNotNull() &
            (F.col("startYear").cast("int") >= 1980)
        )
        .join(
            title_ratings_df
            .select("tconst", "averageRating", "numVotes")
            .filter(
                (F.col("averageRating") >= 8.0) &
                (F.col("numVotes") >= MIN_VOTES)
            ),
            "tconst"
        )
        .groupBy("startYear")
        .agg(
            F.count("*").alias("highRatedCount"),
            F.round(F.avg("averageRating"), 2).alias("avgRating")
        )
        .orderBy("startYear")
    )

    result.explain()
    return result


def question_5_avg_rating_by_country(title_akas_df, title_basics_df, title_ratings_df):
    """
    Q5: Який середній рейтинг фільмів за країною виробництва?
    Використовує: JOIN (x2), FILTER, GROUP BY
    """
    # Спочатку join двох малих таблиць — отримуємо малий набір tconst
    rated_movies = (
        title_ratings_df
        .select("tconst", "averageRating", "numVotes")
        .filter(F.col("numVotes") >= MIN_VOTES)
        .join(
            title_basics_df
            .select("tconst", "titleType")
            .filter(F.col("titleType") == "movie"),
            "tconst"
        )
        .select("tconst", "averageRating")
    )

    # Тепер join важкого akas лише з вже відфільтрованим набором
    result = (
        title_akas_df
        .select("titleId", "region")
        .filter(
            F.col("region").isNotNull() &
            (F.col("region") != "\\N") &
            (F.length(F.col("region")) == 2)
        )
        .dropDuplicates(["titleId", "region"])
        .join(
            rated_movies,
            F.col("titleId") == F.col("tconst"),
            "inner"
        )
        .groupBy("region")
        .agg(
            F.round(F.avg("averageRating"), 2).alias("avgRating"),
            F.count("*").alias("moviesCount")
        )
        .filter(F.col("moviesCount") >= 10)
        .orderBy(F.desc("avgRating"))
    )

    result.explain()
    return result


def question_6_actors_by_total_votes(title_principals_df, title_basics_df, title_ratings_df, name_basics_df):
    """
    Q6: Хто з акторів знімався у фільмах з найбільшою сумарною кількістю голосів?
    Використовує: JOIN (x3), FILTER, GROUP BY
    """
    result = (
        title_principals_df
        .select("tconst", "nconst", "category")
        .filter(F.col("category").isin("actor", "actress"))
        .join(
            title_basics_df
            .select("tconst", "titleType")
            .filter(F.col("titleType") == "movie"),
            "tconst"
        )
        .join(
            title_ratings_df
            .select("tconst", "averageRating", "numVotes")
            .filter(F.col("numVotes") >= MIN_VOTES),
            "tconst"
        )
        .groupBy("nconst")
        .agg(
            F.round(F.avg("averageRating"), 2).alias("avgRating"),
            F.sum("numVotes").alias("totalVotes"),
            F.countDistinct("tconst").alias("filmsCount")
        )
        .filter(F.col("filmsCount") >= 5)
        .join(name_basics_df.select("nconst", "primaryName"), "nconst")
        .select("primaryName", "avgRating", "totalVotes", "filmsCount")
        .orderBy(F.desc("totalVotes"))
    )

    result.explain()
    return result



