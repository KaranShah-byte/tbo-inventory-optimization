TBO.com Inventory Optimization Engine 🏨✈️

Hackathon Idea Submission for TBO.com

This repository contains an intelligent decision-support platform designed to help TBO.com maximize availability and profitability by making smarter, data-driven travel inventory procurement decisions.

🎯 Problem Statement

TBO.com needs a solution to optimize budget allocation across hotels, flights, and destinations while accounting for demand fluctuations, pricing changes, cancellations, and unsold inventory risks.

💡 Core Architecture & Features

Our solution directly answers the problem statement by implementing three core components:

Analytics Engine: Ingests historical transactional data (Kaggle Hotel Booking Demand dataset) to calculate true cancellation rates, average daily rates (ADR), and project future demand.

Budget Allocator: Utilizes a Greedy Knapsack algorithm to systematically allocate any given maximum budget to the inventory offering the highest guaranteed Risk-Adjusted Return on Investment (ROI).

Recommendation System: An interactive, web-based dashboard that transforms the backend calculations into a clear, actionable procurement plan for buyers.

🛠️ Tech Stack

Backend & API: Python, FastAPI, Uvicorn

Data Processing: Pandas, NumPy

Frontend: HTML5, CSS3, Vanilla JavaScript (Served directly via FastAPI)

Deployment: Render

🌐 Live Demo

You can view the live, fully functional application here:
[Insert your Render URL here, e.g., https://tbo-inventory-optimization.onrender.com]

🚀 How to Run Locally

Clone the repository:

git clone https://github.com/YOUR-USERNAME/tbo-inventory-optimization.git
cd tbo-inventory-optimization


Install dependencies:
Ensure you have Python installed, then run:

pip install -r requirements.txt


Start the Application:

python -m uvicorn main:app --reload


View the Dashboard:
Open your browser and navigate to http://127.0.0.1:8000. The FastAPI backend will automatically serve the interactive frontend. Enter a budget and click Generate Procurement Plan!

📂 Project Structure

main.py: The FastAPI application, API routes, and frontend server.

optimization_engine.py: The core mathematical algorithm that processes the dataset and allocates the budget.

index.html: The frontend user interface dashboard.

requirements.txt: Python package dependencies.

hotel_bookings.csv: The historical real-world dataset used to train the recommendations.
