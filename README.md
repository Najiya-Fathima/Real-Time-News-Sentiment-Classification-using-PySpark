# Real-Time-News-Sentiment-Classification-using-PySpark

This project demonstrates a complete, real-time data pipeline that fetches live news headlines, processes them using PySpark and Spark NLP to determine their sentiment, and visualizes the results on a live dashboard built with Streamlit.



## 🔹 Project Architecture

The application is composed of three independent services that communicate through the filesystem, simulating a real-world streaming architecture.

```
┌──────────────────┐      ┌───────────────┐      ┌──────────────────┐      ┌─────────────────┐      ┌───────────┐
│   NewsAPI.org    ├─────►│ data_producer.py │───►│   news_stream/   │───►│ main_streamlit.py  │───►│  results/   │
│ (Live Headlines) │      │ (Fetches Data)   │    │  (JSON Files)    │     │  (Spark NLP Job)  │    │(Parquet Files)│
└──────────────────┘      └───────────────┘      └───────────────┘      └──────────────────┘      └──────┬──────┘
                                                                                                        │
                                                                                                        ▼
                                                                                             ┌──────────────────┐
                                                                                             │ streamlit_app.py │
                                                                                             │  (Live Dashboard)│
                                                                                             └──────────────────┘
```

## ✨ Features

- **Real-Time Data Ingestion**: Fetches the latest headlines from the BBC News source every 30 seconds.
- **Scalable NLP Processing**: Uses PySpark and Spark NLP to process a stream of headlines and classify their sentiment (Positive, Negative, Neutral).
- **Live Dashboard**: A Streamlit web application provides a real-time view of the processed data.
- **Key Metrics**: Displays total headlines processed and counts for each sentiment category.
- **Visualizations**: A live bar chart shows the distribution of sentiments.
- **Full Data View**: A table displays all processed headlines and their assigned sentiment, with the latest news at the top.

## 🔧 Tech Stack

- **Data Ingestion**: Python, `newsapi-python`
- **Data Processing**: Apache Spark (PySpark), Spark NLP
- **Dashboard**: Streamlit
- **Core Libraries**: Pandas, PyArrow, python-dotenv

---

## 🚀 Getting Started

Follow these steps to set up and run the project on your local machine.

### 1. Prerequisites

- **Python 3.9+**
- **Java 8 or 11** (Required for PySpark)
- **Conda** (Recommended for managing Python environments)

### 2. Setup and Installation

**Clone the repository:**
```bash
git clone <your-repository-url>
cd <your-repository-name>
```

**Create a Conda environment:**
```bash
conda create --name news-sentiment python=3.9
conda activate news-sentiment
```

**Install the required Python libraries:**
Create a file named `requirements.txt` with the following content:
```txt
pyspark==3.5.0
newsapi-python==0.2.7
streamlit==1.30.0
pandas
pyarrow
python-dotenv
```
Then, install them using pip:
```bash
pip install -r requirements.txt
```

**Get a NewsAPI Key:**
- Go to [newsapi.org](https://newsapi.org/) and register for a free developer API key.
- Once you have the key, copy it.

**Create the Environment File:**
- In the main project directory, create a file named `.env`.
- Add your API key to this file like so:
  ```
  NEWS_API="YOUR_API_KEY_HERE"
  ```
- **Important:** Also add the path to your conda environment's Python executable. This is crucial for PySpark to work correctly.
  ```
  PYSPARK_PYTHON="C:/path/to/your/conda/envs/news-sentiment/python.exe"
  ```
  *(Replace the path with the actual path on your system. You can find it by running `where python` or `which python` in your activated conda terminal.)*

### 3. How to Run the Application

You will need to open **three separate terminal windows**, all with the `news-sentiment` conda environment activated.

**➡️ Terminal 1: Start the Data Producer**

This script fetches the news and creates the JSON files.

```bash
python data_producer.py
```
You should see output like: `[YYYY-MM-DD HH:MM:SS] Fetching new headlines...`

**➡️ Terminal 2: Start the Spark Processing Job**

This script listens for new JSON files, performs the sentiment analysis, and writes the results as Parquet files.

```bash
python main_streamlit.py
```
You will see Spark initialization logs, and then it will wait for data: `Spark Streaming job started. Waiting for data...`

**➡️ Terminal 3: Start the Streamlit Dashboard**

This script reads the results from the Spark job and displays them.

```bash
streamlit run streamlit_app.py
```
This will automatically open a new tab in your web browser. The dashboard will initially show "Waiting for data...". After the first batch of headlines is produced and processed (this may take 30-60 seconds), the dashboard will come to life and will auto-refresh every 10 seconds.

---

## 📂 Project Structure

```
.
├── 📂 news_stream/           # (Auto-created) Input directory where JSON headlines are dropped.
├── 📂 results_parquet/       # (Auto-created) Output directory where Spark saves processed data.
├── 📂 checkpoint/            # (Auto-created) Directory for Spark to save streaming state.
│
├── 📜 data_producer.py       # Script to fetch news from NewsAPI.
├── 📜 main_streamlit.py      # The PySpark application for NLP processing.
├── 📜 streamlit_app.py       # The Streamlit dashboard application.
│
├── 📜 .env                   # Your local environment file with API keys and paths.
├── 📜 requirements.txt       # List of Python dependencies.
└── 📜 README.md              # This file.
```
