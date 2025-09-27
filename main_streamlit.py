# main_streaming.py (CORRECT VERSION)

import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, ArrayType
from sparknlp.base import DocumentAssembler
from sparknlp.annotator import Tokenizer, SentimentDLModel, SentenceEmbeddings, WordEmbeddingsModel
from pyspark.ml import Pipeline
from pyspark.sql.functions import col, explode
from dotenv import load_dotenv

load_dotenv()
python_path = os.getenv("PYSPARK_PYTHON")
os.environ['PYSPARK_PYTHON'] = python_path
os.environ['PYSPARK_DRIVER_PYTHON'] = python_path

spark = SparkSession.builder \
    .appName('Structured Streaming Sentiment Analysis') \
    .config("spark.jars.packages", "com.johnsnowlabs.nlp:spark-nlp_2.12:5.2.0") \
    .getOrCreate()

# Schema for an array of strings
schema = StructType([
    StructField("headlines", ArrayType(StringType()))
])

stream_df = spark.readStream \
    .format("json") \
    .schema(schema) \
    .load("news_stream")

# Explode the array to create a column named "headline"
headlines_df = stream_df.select(explode(col("headlines")).alias("headline"))

# Pipeline now uses the "headline" column
document_assembler = DocumentAssembler().setInputCol("headline").setOutputCol("document")
tokenizer = Tokenizer().setInputCols(["document"]).setOutputCol("token")
word_embeddings = WordEmbeddingsModel.pretrained("glove_100d", "en").setInputCols(["document", "token"]).setOutputCol("embeddings")
sentence_embeddings = SentenceEmbeddings().setInputCols(["document", "embeddings"]).setOutputCol("sentence_embeddings")
sentiment_dl = SentimentDLModel.pretrained("sentimentdl_glove_imdb", "en").setInputCols(["sentence_embeddings"]).setOutputCol("sentiment")

pipeline = Pipeline().setStages([document_assembler, tokenizer, word_embeddings, sentence_embeddings, sentiment_dl])

# Ensure the final output selects the correct "headline" column
result_stream = pipeline.fit(headlines_df).transform(headlines_df) \
    .select("headline", col("sentiment.result").getItem(0).alias("sentiment"))

query = result_stream.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "results_parquet") \
    .option("checkpointLocation", "checkpoint") \
    .start()

print("Spark Streaming job started. Waiting for data...")
query.awaitTermination()