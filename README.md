# DSA4264 Project

## Introduction

## Table of Contents

- [DSA4264 Project](#dsa4264-project)
  - [Introduction](#introduction)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Data Collection](#data-collection)
  - [Usage](#usage)
  - [Features](#features)
  - [Dependencies](#dependencies)

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/dsa4264_project.git
```

2. Navigate to the project directory:

```bash
cd dsa4264_project
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

1. Create a .env file in the root directory of the project.
2. Add your API key to the .env file as follows:

```bash
API_KEY= your_api_key_here
```

## Data Collection

To fetch the necessary data files, you need to run the data_pulling.py script. This script will download and prepare the data files required for the application.

```bash
python data/data_pulling.py
```

Once this script completes, you should have the required files in the data folder.

## Usage

After setting up the .env file and running the data collection script, you can launch the Streamlit app to visualize the data.

```bash
streamlit run app.py
```

## Features

## Dependencies

This project uses Python version 3.11.5 and the dependencies are listed in the requirements.txt file.
