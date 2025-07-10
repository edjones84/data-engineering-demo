# 🚀 Data Engineering Demo

A demo project showcasing data engineering workflows, including SQLite integration, Python-based data processing, and glider stream ingestion using Docker.

---

## 🧑‍💻 Recommended IDEs

We recommend using one of the following IDEs for the best development experience:

- Visual Studio Code
- PyCharm

---

## 🧑‍💻Git setup
- If you do not have git setup please follow the steps in git_setup.md
---

## 🐍 Python Environment Setup

### 1. Install Python (3.8 or later)

- **Mac**: Use [Homebrew](https://brew.sh/)
```
brew install python
  ```

- **Windows**: Download and install from python.org


## 🗃  ️ SQLite Installation
**Mac**
SQLite is usually pre-installed


**Windows**
Download the SQLite tools from the official SQLite website
Extract the ZIP file and add the folder path to your system’s PATH environment variable.


## 🐳 Docker Setup Mac & Windows (Optional if you want to run with Kafka)
1. Install Docker Desktop
Download from Docker Desktop
Follow the installation instructions for your operating system.
After installation, verify Docker is running by launching PowerShell (windows) or Command Line (Mac) an d running:
```commandline
docker --version
docker-compose --version

```



## 🧑‍💻 Batch Weather Data ETL Tutorial

This tutorial will guide you through building an automated batch ETL pipeline that extracts weather data from an API, loads it into a SQLite database, and exports the results to a CSV file.

### 🏁 Getting Started

#### 1. Set Up Your Python Environment

- **Create a virtual environment** (recommended):
  ```bash
  python -m venv venv
  ```
- **Activate your virtual environment:**
  - **Windows:**
    ```bash
    venv\Scripts\activate
    ```
  - **Mac/Linux:**
    ```bash
    source venv/bin/activate
    ```

- **Install required packages:**
  ```bash
  pip install -r requirements.txt
   ```

#### 2. Explore the Solution

- The `weather-batch-pipeline/solution/` folder contains completed solution files.
- You can run these files to see the expected output and understand the ETL process:
  ```bash
  cd weather-batch-pipeline/solution
  dagster dev -f dagster_weather_etl_workflow.py
 - In your browser, navigate to http://127.0.0.1:3000
 
Alternatively:
 - You can run your python script implementation with:
  ```bash
  python weather-batch-pipeline/starter/weather_data_etl.py
  ```

#### 3. Build Your Own Solution

- Use the starter files in `weather-batch-pipeline/starter/` to build your own ETL pipeline.
- The main file to edit is `weather_data_etl.py`. Implement the following functions:
  - `extract_data_as_json`: Fetches weather data from the API.
  - `transform_json_to_dataframe`: Processes and flattens the JSON into a DataFrame.
  - `load_dataframe_to_sqllite_db`: Loads new weather data into a SQLite database, avoiding duplicates.
  - `export_to_csv`: Exports the database table to a CSV file.

- You can run your implementation in dagster with:
  ```bash
  cd weather-batch-pipeline/starter
  dagster dev -f dagster_weather_etl_workflow.py
  ```
- In your browser, navigate to http://127.0.0.1:3000



#### 4. Tips

- Refer to the solution files if you get stuck or want to check your approach.
- The ETL pipeline should:
  1. Extract weather data from the Open-Meteo API.
  2. Transform the JSON response into a flat DataFrame, including units in column names.
  3. Load only new rows (by time) into the SQLite database.
  4. Export the full table to a CSV file.

#### 5. Next Steps

- Once you complete the batch ETL, try modifying the pipeline to handle schema drift or add new weather variables.
- Explore the streaming lab for real-time data processing with Kafka.

---




## Streaming Lab
🌐 Glider Stream Integration
This project uses the python-ogn-client to stream glider data.

First once you have downloaded this git repo you will need to install python libraries:

Navigate to the project directory, open a command line and run:
```commandline
pip install -r requirements.txt
```

### Option A (without Kafka)
Run the following in your IDE command line
```bash
python glider-stream/glider.py
```
Go into the glider.py stream and work out what you want to change


### Option B (with Kafka)
Run the following in your IDE command line (ensure docker desktop is running)
```bash
docker compose -f glider-stream/kafka/docker-compose.yaml up
```
Create a new terminal window and now run the following to start producing data to kafka
```bash
python glider-stream/kafka/beacon_producer.py
```
Navigate to http://localhost:19000/ to view the messages in Kafdrop


Create a new terminal window and now run the following to start consuming data to a local db
```bash
python glider-stream/kafka/beacon_consumer.py
```