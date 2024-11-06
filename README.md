# DSA4264 Project

This project is part of the DSA4264 module at the National University of Singapore (NUS). It was completed by Year 4 students from Data Science and Analytics, as well as Data Science and Economics majors. The primary objective is to identify three bus routes for potential removal based on data-driven insights.

## Table of Contents

- [DSA4264 Project](#dsa4264-project)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
  - [Features](#features)
  - [Technical Documentation](#technical-documentation)
  - [Dependencies](#dependencies)
  - [Credits](#credits)

## Introduction

This project leverages data analysis to evaluate bus route efficiency in Singapore and aims to identify routes that can be optimised or removed to improve public transportation efficiency.

## Installation

To set up the project on your local machine, follow these steps:

1. **Clone the repository** to your local machine:

    ```bash
    git clone https://github.com/your-username/dsa4264_project.git
    ```

2. **Navigate to the project directory**:

    ```bash
    cd dsa4264_project
    ```

3. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. **Create a `.env` file** in the root directory of the project.
2. **Obtain two API keys** from:
   - [LTA DataMall API](https://datamall.lta.gov.sg/content/datamall/en.html)
   - [OneMap API](https://www.onemap.gov.sg/apidocs/)
   
3. **Add the API keys** to the `.env` file as shown below:

    ```bash
    API_KEY = 'your_lta_api_key_here'        # LTA Datamall API Key
    ACCESS_TOKEN = 'your_onemap_api_key_here' # OneMap API Key
    ```

4. **Fetch the data files** by running the `data_pulling.py` script, which downloads and prepares the necessary datasets.

    ```bash
    python data_pulling.py
    ```

5. **Process the data** by running `data_processing.ipynb`. Click on Run all, and this will clean and process the data accordingly. Do note that some functions, such as OSRM will take approximately 5 hours to run.

6. **Analyze and view results** by opening the `main.ipynb` Jupyter notebook. Run all cells to review the analytics, code logic, and decision-making process behind identifying bus routes for removal.

## Usage

After setting up the `.env` file and running `data_pulling.py` + `data_processing.ipynb` + `main.ipynb`, you can launch the Flask application to visualise the data:

```bash
python app.py
```

The web app will allow users to interact with the data and view analyses performed in the project.

## Features

- **Data Collection**: Automates the retrieval of data from LTA DataMall and OneMap APIs.
- **Analysis**: Includes comprehensive data analysis to evaluate the viability of bus routes.
- **Visualisation**: Provides visual representations of key insights for improved understanding and decision-making.
- **Data-Driven Decision-Making**: Supports recommendations for optimizing the bus route network by suggesting potential route removals.

## Technical Documentation
You can read our technical documentation in `technical_report.html`

## Dependencies

This project uses **Python 3.11.5**. All other dependencies are listed in `requirements.txt`.

## Credits
This project was completed in five weeks and was completed by (in no order of contribution): 
- Brandon NEO (NUS Y4 DSE)
- CHOW Xin Tian (NUS Y4 DSE)
- LIM Choon Hao (NUS Y4 DSA)
- YOUNG Zhan Heng (NUS Y4 DSE)
We will also like to thank your Adjunct Lecturer, Shaun Khoo, for guiding us throughout this project.