from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when, split, size, trim, lower
from pyspark.sql.types import IntegerType


def preprocess_name_basics(df: DataFrame) -> DataFrame:
    df = df.select([
        when(col(c) == "\\N", None).otherwise(col(c)).alias(c)
        for c in df.columns
    ])

    df = df.withColumn("birthYear", col("birthYear").cast(IntegerType()))
    df = df.withColumn("deathYear", col("deathYear").cast(IntegerType()))

    df = df.withColumn(
        "primaryProfessionArray",
        when(col("primaryProfession").isNotNull(), split(col("primaryProfession"), ","))
    )

    df = df.withColumn(
        "knownForTitlesArray",
        when(col("knownForTitles").isNotNull(), split(col("knownForTitles"), ","))
    )

    df = df.withColumn(
        "professionCount",
        when(col("primaryProfessionArray").isNotNull(), size(col("primaryProfessionArray")))
    )

    df = df.withColumn(
        "knownTitlesCount",
        when(col("knownForTitlesArray").isNotNull(), size(col("knownForTitlesArray")))
    )

    return df


def _replace_imdb_missing_markers(df: DataFrame) -> DataFrame:

    return df.select([
        when(trim(col(c)) == "\\N", None).otherwise(col(c)).alias(c)
        for c in df.columns
    ])

def preprocess_title_akas(df: DataFrame) -> DataFrame:
    df = _replace_imdb_missing_markers(df)

    text_cols = ["title", "region", "language", "types", "attributes"]
    for c in text_cols:
        if c in df.columns:
            df = df.withColumn(c, trim(col(c)))

    df = df.withColumn("ordering", col("ordering").cast(IntegerType()))
    df = df.withColumn("isOriginalTitle", col("isOriginalTitle").cast(IntegerType()))

    df = df.withColumn(
        "isOriginalTitle",
        when(col("isOriginalTitle").isin(0, 1), col("isOriginalTitle"))
    )

    df = df.withColumn(
        "typesArray",
        when(col("types").isNotNull(), split(col("types"), ","))
    )

    df = df.withColumn(
        "attributesArray",
        when(col("attributes").isNotNull(), split(col("attributes"), ","))
    )

    df = df.withColumn(
        "typesCount",
        when(col("typesArray").isNotNull(), size(col("typesArray")))
    )

    df = df.withColumn(
        "attributesCount",
        when(col("attributesArray").isNotNull(), size(col("attributesArray")))
    )

    if "language" in df.columns:
        df = df.withColumn("languageNorm", lower(col("language")))

    if "region" in df.columns:
        df = df.withColumn("regionNorm", lower(col("region")))

    return df


def preprocess_title_basics(df: DataFrame) -> DataFrame:
    df = _replace_imdb_missing_markers(df)

    text_cols = ["titleType", "primaryTitle", "originalTitle", "genres"]
    for c in text_cols:
        if c in df.columns:
            df = df.withColumn(c, trim(col(c)))

    df = df.withColumn("isAdult", col("isAdult").cast(IntegerType()))
    df = df.withColumn("startYear", col("startYear").cast(IntegerType()))
    df = df.withColumn("endYear", col("endYear").cast(IntegerType()))
    df = df.withColumn("runtimeMinutes", col("runtimeMinutes").cast(IntegerType()))

    df = df.withColumn(
        "isAdult",
        when(col("isAdult").isin(0, 1), col("isAdult"))
    )

    df = df.withColumn(
        "startYear",
        when((col("startYear") >= 1800) & (col("startYear") <= 2026), col("startYear"))
    )

    df = df.withColumn(
        "endYear",
        when((col("endYear") >= 1800) & (col("endYear") <= 2026), col("endYear"))
    )

    df = df.withColumn(
        "endYear",
        when(
            col("startYear").isNotNull() & col("endYear").isNotNull() &
            (col("endYear") >= col("startYear")),
            col("endYear")
        ).when(col("endYear").isNull(), None)
         .otherwise(None)
    )

    df = df.withColumn(
        "runtimeMinutes",
        when(
            col("runtimeMinutes").isNotNull() &
            (col("runtimeMinutes") > 0) &
            (col("runtimeMinutes") <= 1440),
            col("runtimeMinutes")
        )
    )

    df = df.withColumn(
        "genresArray",
        when(col("genres").isNotNull(), split(col("genres"), ","))
    )

    df = df.withColumn(
        "genresCount",
        when(col("genresArray").isNotNull(), size(col("genresArray")))
    )

    df = df.withColumn(
        "isSeries",
        when(col("endYear").isNotNull(), 1).otherwise(0)
    )

    df = df.withColumn(
        "hasGenres",
        when(col("genres").isNotNull(), 1).otherwise(0)
    )

    df = df.withColumn(
        "hasDrama",
        when(col("genres").contains("Drama"), 1).otherwise(0)
    )

    df = df.withColumn(
        "hasComedy",
        when(col("genres").contains("Comedy"), 1).otherwise(0)
    )

    df = df.withColumn(
        "hasAction",
        when(col("genres").contains("Action"), 1).otherwise(0)
    )

    return df


def preprocess_title_crew(df: DataFrame) -> DataFrame:
    df = _replace_imdb_missing_markers(df)

    text_cols = ["directors", "writers"]
    for c in text_cols:
        if c in df.columns:
            df = df.withColumn(c, trim(col(c)))

    df = df.withColumn(
        "directorsArray",
        when(col("directors").isNotNull(), split(col("directors"), ","))
    )

    df = df.withColumn(
        "writersArray",
        when(col("writers").isNotNull(), split(col("writers"), ","))
    )

    df = df.withColumn(
        "directorsCount",
        when(col("directorsArray").isNotNull(), size(col("directorsArray")))
    )

    df = df.withColumn(
        "writersCount",
        when(col("writersArray").isNotNull(), size(col("writersArray")))
    )

    return df


def preprocess_title_episode(df: DataFrame) -> DataFrame:
    df = _replace_imdb_missing_markers(df)

    if "parentTconst" in df.columns:
        df = df.withColumn("parentTconst", trim(col("parentTconst")))

    df = df.withColumn("seasonNumber", col("seasonNumber").cast(IntegerType()))
    df = df.withColumn("episodeNumber", col("episodeNumber").cast(IntegerType()))

    df = df.withColumn(
        "seasonNumber",
        when(col("seasonNumber") >= 0, col("seasonNumber"))
    )

    df = df.withColumn(
        "episodeNumber",
        when(col("episodeNumber") >= 0, col("episodeNumber"))
    )

    return df

def preprocess_title_principals(df: DataFrame) -> DataFrame:
    df = _replace_imdb_missing_markers(df)

    text_cols = ["tconst", "nconst", "category", "job", "characters"]
    for c in text_cols:
        if c in df.columns:
            df = df.withColumn(c, trim(col(c)))

    df = df.withColumn("ordering", col("ordering").cast(IntegerType()))

    if "category" in df.columns:
        df = df.withColumn("categoryNorm", lower(col("category")))

    df = df.withColumn(
        "jobArray",
        when(col("job").isNotNull(), split(col("job"), ","))
    )

    df = df.withColumn(
        "jobCount",
        when(col("jobArray").isNotNull(), size(col("jobArray")))
    )

    df = df.withColumn(
        "charactersClean",
        when(col("characters").isNotNull(), trim(col("characters")))
    )

    df = df.withColumn(
        "charactersClean",
        when(col("charactersClean").isNotNull(),
             col("charactersClean").substr(2, 1000))
    )

    df = df.withColumn(
        "charactersArray",
        when(col("characters").isNotNull(), split(col("characters"), ","))
    )

    df = df.withColumn(
        "charactersCount",
        when(col("charactersArray").isNotNull(), size(col("charactersArray")))
    )

    df = df.withColumn(
        "isActor",
        when(col("category").isin("actor", "actress"), 1).otherwise(0)
    )

    df = df.withColumn(
        "isDirector",
        when(col("category") == "director", 1).otherwise(0)
    )

    df = df.withColumn(
        "hasJob",
        when(col("job").isNotNull(), 1).otherwise(0)
    )

    df = df.withColumn(
        "hasCharacters",
        when(col("characters").isNotNull(), 1).otherwise(0)
    )

    return df