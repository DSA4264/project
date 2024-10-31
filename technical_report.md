# Technical Report

## Table of Contents
1. [Introduction](#1-introduction)  
   1.1 [Problem Statement](#11-problem-statement)  
   1.2 [Background](#12-background)  

2. [Data](#2-data)  
   2.1 [Datasets Used](#21-datasets-used)  
      2.1.1 [LTA Datamall](#211-lta-datamall)  
      2.1.2 [OneMap API](#212-onemap-api)  
      2.1.3 [Wikipedia](#213-wikipedia)  
   2.2 [Data Cleaning](#22-data-cleaning)  
   2.3 [Exploratory Data Analytics](#23-exploratory-data-analytics)  

3. [Methodology](#3-methodology)  
   3.1 [Phase One](#31-phase-one)  
      3.1.1 [Mapping Bus Routes](#311-mapping-bus-routes)  
      3.1.2 [Mapping MRT Lines](#312-mapping-mrt-lines)  
      3.1.3 [Mapping Planning Area](#313-mapping-planning-area)  
      3.1.4 [Combining to One Plot](#314-combining-to-one-plot)  
      3.1.5 [Calculating MRT-BUS Parallelism](#315-calculating-mrt-bus-parallelism)  
      3.1.6 [Features Generation](#316-features-generation)  
   3.2 [Phase Two](#32-phase-two)  
      3.2.1 [Obtaining Bus Frequency](#321-obtaining-bus-frequency)  
      3.2.2 [Calculating BUS-BUS Parallelism](#322-calculating-bus-bus-parallelism)  
      3.2.3 [Clustering Model](#323-clustering-model)  

4. [Results](#4-results)  
   4.1 [Results of Phase 1](#41-results-of-phase-1)  
   4.2 [Results of Phase 2](#42-results-of-phase-2)  

5. [Discussion](#5-discussion)  
   5.1 [Interpreting Results](#51-interpreting-results)  
   5.2 [Proposed Changes of Bus Routes](#52-proposed-changes-of-bus-routes)  

6. [Conclusion](#6-conclusion)  
   6.1 [Limitations](#61-limitations)  
   6.2 [Future Work](#62-future-work)  

---

## 1. Introduction
We were approached by the Land Transport Authority (LTA) to use their publicly available datasets to address the issue of redundant bus routes. 

### 1.1 Problem Statement
Our project focuses on two main objectives:
1. Identify approximately 10 bus routes that could be discontinued, based primarily on their overlap with MRT lines.
2. Among the identified bus routes, determine additional factors that might affect rider sentiment, and narrow down to three redundant bus routes.

### 1.2 Background
In October 2023, LTA announced that it would be [discontinuing bus service "167"](https://www.straitstimes.com/singapore/bus-service-167-to-be-terminated-from-dec-10), citing “falling ridership numbers due to the construction of the Thomson-East Coast Line (TEL)” as the primary reason. This decision led to widespread discussion, with many riders of bus service 167 voicing that they found it unfair.

In a rare move by the Singaporean government, they later [reversed this decision](https://www.straitstimes.com/singapore/transport/lta-u-turns-on-decision-to-stop-bus-service-167-route-to-be-retained-with-30-minute-intervals), choosing to retain the bus service, albeit with increased intervals from 10 to 30 minutes. However, LTA emphasised that this was an exceptional case and that more bus services could be cut in the future.

This incident highlights a lack of a robust data science methodology within LTA to identify supposedly "redundant" bus routes. Fortunately, we are a team of data science students who use public buses daily. Using a combination of data analytics and machine learning techniques, we aim to address this issue.

## 2. Data

### 2.1 Datasets Used
Before delving into the analytics, we would like to reemphasise that we are using publicly available dataset, which were obtained mainly from the LTA Datamall and OneMapAPI. 
We used our own API keys to obtain the data, and we have included our data pulling code in our Jupyter Notebook.

#### 2.1.1 LTA Datamall
We obtained the following data from the LTA Datamall API:
1. Passenger origin-destination (OD) data

#### 2.1.2 OneMap API
We obtained the following data from the OneMap API:
1. Bus routes
2. MRT Routes

#### 2.1.3 Wikipedia 
We obtained the following data from Wikipedia:
1. MRT station name

We trawled the web to find relevant MRT station data, but there is no data that included future stations, other than Wikipedia.

### 2.2 Data Cleaning
### 2.3 Exploratory Data Analytics

## 3. Methodology

### 3.1 Phase One
#### 3.1.1 Mapping Bus Routes
#### 3.1.2 Mapping MRT Lines
#### 3.1.3 Mapping Planning Area
#### 3.1.4 Combining to One Plot
#### 3.1.5 Calculating MRT-BUS Parallelism
#### 3.1.6 Features Generation

### 3.2 Phase Two
#### 3.2.1 Obtaining Bus Frequency
#### 3.2.2 Calculating BUS-BUS Parallelism
#### 3.2.3 Clustering Model

## 4. Results
### 4.1 Results of Phase 1 
### 4.2 Results of Phase 2

## 5. Discussion
### 5.1 Interpreting Results
### 5.2 Proposed Changes of Bus Routes

## 6. Conclusion
### 6.1 Limitations
### 6.2 Future Work