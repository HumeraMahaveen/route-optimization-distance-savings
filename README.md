# Route Optimization & Distance Savings

> A Python-based last-mile delivery route optimization project that uses Nearest Neighbor and 2-opt algorithms to reduce travel distance and improve delivery efficiency.

---

## 📌 Project Overview

Last-mile delivery is a major operational challenge for e-commerce and logistics companies. Poorly planned delivery routes can result in:

- Higher travel distance
- Increased fuel consumption
- Longer delivery times
- Higher operational costs

This project develops a route optimization model for a simulated delivery network containing **20 customer stops**.

The model compares an original delivery route with an optimized route generated using:

- Nearest Neighbor algorithm
- 2-opt local search optimization

The objective is to minimize total route distance and estimate the resulting operational savings.

---

## 🎯 Objectives

The main objectives of this project are to:

1. Optimize delivery routes between multiple customer locations.
2. Reduce total travel distance.
3. Compare the original route with the optimized route.
4. Estimate potential time savings.
5. Estimate potential fuel savings.
6. Demonstrate practical applications of route optimization algorithms.

---

## 🧠 Algorithms Used

### 1. Nearest Neighbor

The Nearest Neighbor algorithm constructs an initial route by repeatedly selecting the closest unvisited location.

The basic process is:


Start at depot
      ↓
Find nearest unvisited customer
      ↓
Travel to customer
      ↓
Mark customer as visited
      ↓
Repeat until all customers are visited
      ↓
Return to depot

2. 2-opt Optimization

The 2-opt algorithm improves an existing route by testing whether exchanging two route edges can reduce the total distance.

The algorithm repeatedly:

Selects two edges.
Removes the selected edges.
Reverses the route segment between them.
Calculates the new distance.
Keeps the change if it improves the route.

This process continues until no further improvement is found.

📊 Dataset

The project uses a simulated delivery network with 20 customer stops and a central delivery hub.

Each location contains:

Location identifier
X coordinate
Y coordinate

The coordinates are used to calculate distances between delivery locations.

📈 Results

The optimization produced the following results:
| Metric                   |      Result |
| ------------------------ | ----------: |
| Customer stops           |          20 |
| Original route distance  |   240.17 km |
| Optimized route distance |    85.58 km |
| Distance saved           |   154.59 km |
| Distance reduction       |       64.4% |
| Estimated time saved     | 371 minutes |
| Estimated fuel saved     |     12.37 L |

The optimized route reduced the total travel distance by approximately 64.4% compared with the original route.

📊 Route Comparison

The project generates a visualization comparing the original and optimized delivery routes.

⛽ Distance & Savings Analysis

The project also generates a visual summary of the distance reduction and estimated savings.

🖥️ Project Workflow
Simulated Delivery Locations
            ↓
Calculate Initial Route
            ↓
Nearest Neighbor
            ↓
Generate Initial Optimized Route
            ↓
Apply 2-opt Improvement
            ↓
Calculate Optimized Distance
            ↓
Compare Original vs Optimized Route
            ↓
Estimate Time & Fuel Savings

🛠️ Tools & Technologies
-Python
-Python data structures
-Mathematical distance calculations
-Nearest Neighbor algorithm
-2-opt optimization
-CSV data processing
-Data visualization

📂 Project Structure
route-optimization-distance-savings/
│
├── route_optimizer.py
├── results_summary.csv
├── route_comparison.png
├── distance_savings.png
└── README.md

💼 Business Application

Route optimization can be applied to:

-E-commerce delivery networks
-Warehouse-to-customer delivery
-Logistics companies
-Last-mile delivery operations
-Fleet management
-Distribution networks

Reducing travel distance can potentially reduce:
-Fuel consumption
-Driver travel time
-Vehicle operating costs
-Delivery delays
-Overall logistics costs


This is an independent academic/student project using simulated delivery data.

The project is not affiliated with, sponsored by, or based on confidential data from Flipkart or any other logistics company.


