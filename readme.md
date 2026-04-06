# Ethnic Wear Sales Dashboard

## Overview
This project is an interactive sales analytics dashboard built using Streamlit. It analyzes the performance of an ethnic wear business by transforming raw transactional data into meaningful business insights.

The dashboard is designed to help stakeholders understand profitability, product performance, customer segments, and geographic trends through a clean and structured interface.

---

## Features

- Interactive web-based dashboard
- KPI tracking for business performance
- Dynamic filters (Category, City, Segment)
- Multi-section layout (Overview, Products, Geography)
- Interactive charts using Plotly
- Data cleaning and transformation for consistency

---

## Key Metrics

- Total Profit
- Total Orders
- Units Sold
- Average Profit per Order
- Loss-Making Orders

---

## Dashboard Sections

### Overview
- Monthly profit trend
- Profit vs loss distribution
- Profit by segment
- Orders and units by category

### Product Analysis
- Profit by product category
- Top 10 products by profit
- Discount vs profit (scatter analysis)
- Category-level summary table

### Geography Analysis
- Profit by city
- Orders by city and segment
- Segment performance comparison

---

## Business Insights

- A portion of orders are loss-making, indicating potential pricing or discount issues
- Certain categories contribute significantly to overall profit
- Customer segments differ in profitability, highlighting targeting opportunities
- Geographic trends show which cities are driving business performance

---

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly

---

## Project Structure

project/
│
├── app.py
├── data/
│   └── cleaned_business.csv
├── notebook/
│   └── EDA.ipynb
├── requirements.txt
└── README.md

---

## Installation and Setup

1. Clone the repository

git clone https://github.com/your-username/your-repo-name.git

2. Navigate to the project directory

cd your-repo-name

3. Install dependencies

pip install -r requirements.txt

4. Run the application

streamlit run app.py

---

## Deployment

The application can be deployed using platforms such as Streamlit Cloud, Render, or any cloud service that supports Python-based web applications.

---

## Future Improvements

- Add user authentication
- Integrate real-time data sources
- Improve UI with advanced styling
- Add export and reporting features

---

## Author

Rajat Singh

---

## License

This project is intended for educational and portfolio purposes.