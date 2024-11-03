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
<br>
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
Data cleaning was relatively easy, as compared to most datasets found online, since the data we are using was taken from public datasets from established APIs such as OneMap API and LTA Datamall.

## 3. Methodology

### 3.1 Phase One
We ran with two phases of filtering, the first being a parallelisation filtering. So amongst all the bus services in Singapore, we compared their route to determine if there was a high percentage overlap with the MRT.
<br>
In our second phase, we ran a distance filtering. This was because there are bus services that are known as residential trunk. More will be elaborated below.

#### 3.1.1 Creating the base map
The base plot of the map we used was made using Folium.js. We then created the polygons and plots and overlaid it on our interactive map. At the end of our map creation, we output it as a HTML file to be used for our interactive frontend.

#### 3.1.3 Mapping Bus Routes
To map all bus routes available in Singapore, we utilized the Open Source Routing Machine (OSRM) API to plot each route segment between consecutive bus stops along the road network. This methodology involved several key steps:

1. **Data Preparation and Grouping**: We began by grouping the dataset of bus routes by each unique ‘ServiceNo’ (bus service number) and ‘Direction’. To ensure that each route was traced in the correct sequence, the data was sorted by ‘StopSequence’, aligning each bus stop in the order the route follows.
2. **Retrieving Route Segments Using OSRM**: For each pair of consecutive bus stops within a route, we issued an OSRM API query to retrieve the encoded polyline representing the road network path between the stops. The OSRM API provides a polyline encoding format that captures the sequence of coordinates between stops, which we stored for further analysis.
3. **Mapping Routes on Folium**: We used the Folium mapping library to represent each decoded route segment on a map of Singapore. The encoded polylines were decoded back into latitude and longitude pairs and displayed as continuous lines on the map. Each bus route was colored in black for visibility, with pop-up markers indicating the specific bus service and direction for user interaction.

#### 3.1.4 Mapping MRT Lines
We processed MRT geospatial data from Singapore’s LTA Datamall to create unified geometry objects for each MRT line, allowing for analysis of route parallelism with bus lines. The steps involved were:

1. **Coordinate Reference System (CRS)**: We set the data’s CRS to EPSG:3414, then transformed it to EPSG:4326 for geographic compatibility.
2. **Station Ordering and Categorisation**: Stations were grouped by MRT line and ordered to connect them accurately along each route.
3. **Centroid Representation**: Each station’s polygon footprint was represented by its centroid, enabling a simplified line route.
4. **Line Creation**: We connected centroids sequentially to form a “LineString” for each MRT line, outlining its path.
5. **Union of Line and Polygons**: Each MRT line’s line and station polygons were merged into a single geometry object.
6. **Buffering of lines**: We then created a 200m buffer for each line.

#### 3.1.5 Combining to One Plot
The MRT geometries were added to `df_bus_combined_geometry` alongside bus routes, enabling parallelism analysis across bus and MRT networks in Singapore.

#### 3.1.6 Filter 1: Calculating MRT-BUS Parallelism
1. Adding MRT Geometries: Each MRT line geometry (e.g., North-South, East-West) was added as a new column in the bus route GeoDataFrame (bus_mrt_combined_gdf), providing a spatial reference for each line alongside the bus routes.
2. Buffering Bus Routes: Bus routes were buffered to account for proximity to MRT lines, creating a buffered_bus_route_geom column with a 200-meter buffer around each route. This provides a margin for measuring spatial overlap.
3. Visualising Bus and MRT Lines: For each bus service, the bus route and MRT lines were plotted on a Folium map, with each MRT line shown in a unique colour. This visualisation allowed for a clear comparison of routes and potential overlaps.
4. Calculating Overlap: For each bus service, we calculated the percentage overlap between the buffered bus route and each MRT line geometry. This was done by computing the intersection area of each bus-MRT pair relative to the bus route’s buffered area.
5. Storing Results: The calculated overlap percentages were stored in a new DataFrame, allowing for further analysis of how closely bus routes parallel MRT lines across Singapore’s transport network.

#### 3.1.7 Filter 2: Residential Trunks
Residential trunks are a subset of trunk services in Singapore. Residential trunk services not only connect services between different neighbourhoods, they also loop through some neighbourhoods, acting as a feeder bus service. In our analytics, we wish to filter out such bus services as it can be confused with feeder bus services.
<br>
Using bus service `71` as an example. 
[Insert the plot here please]
We noticed that it operates from Yio Chu Kang Bus Interchange, and then loops at Bishan, then loops with Ang Mo Kio and then Bishan again. 
<br>
However, it is impossible identify residential trunks as they are not labelled as such, so we ran a filtering algorithm on it. So we used a clustering algorithm, clustering on the average distance, to identify the residential trunk services. 

### 3.2 Phase Two
#### 3.2.1 Mapping Planning Area
We used the OneMap API to plot out the residential planning areas and their population numbers. For each bus routes that travels through the residential area, we then added the population number. The population number is not definite, but it is still a decent estimator of the population it could be served.
#### 3.2.1 Obtaining Bus Frequency
We obtained bus frequency data
#### 3.2.2 Calculating BUS-BUS Parallelism
#### 3.2.3 Clustering Model

## 4. Results
### 4.1 Results of Phase 1 
#### 4.1.1 Filter 1: MRT-BUS Parallelisation
#### 4.1.2 Filter 2: Identifying Residential Trunks
### 4.2 Results of Phase 2

## 5. Discussion
### 5.1 Interpreting Results
### 5.2 Proposed Changes of Bus Routes

## 6. Conclusion
### 6.1 Limitations
### 6.2 Future Work