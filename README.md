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