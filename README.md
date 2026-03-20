# 🦠 Disease Outbreak Detection & Early Warning System

An AI-powered web application that detects potential disease outbreaks by analyzing real-time news data and visualizes them using an interactive dashboard.

---

## 📌 Project Overview

This project focuses on building a **real-time disease outbreak monitoring system** using Python and Django.  
The system collects disease-related data from external APIs, processes the data, predicts outbreak probability, and displays results through:

- 📊 Dashboard Table  
- 🌍 Global Map Visualization  
- 📈 Trend Analysis Chart  

---

## 🚀 Features

- 🔍 Disease detection using keyword-based AI logic  
- 🌐 Real-time data collection from News API & WHO API  
- 📍 Location-based outbreak mapping  
- 📊 Interactive dashboard with table, chart, and map  
- 📥 Export outbreak data as CSV  
- 🔐 User authentication system (Login/Signup)  

---

## 🏗️ Tech Stack

| Technology | Usage |
|----------|------|
| Python | Backend logic |
| Django | Web framework |
| SQLite | Database |
| HTML, CSS, JS | Frontend |
| Leaflet.js | Map visualization |
| Chart.js | Graph visualization |
| News API | Data source |
| WHO API | Health data |

---

## ⚙️ System Architecture

1. **Data Collection Layer**
   - Fetch data from News API & WHO API  

2. **Processing Layer**
   - Detect disease keywords  
   - Assign outbreak probability  

3. **Storage Layer**
   - Store results in SQLite database  

4. **Visualization Layer**
   - Dashboard (Table + Map + Chart)  

---

## 🧠 Working Process

1. Fetch real-time news articles  
2. Extract disease-related keywords  
3. Assign a location (city-based)  
4. Predict outbreak probability  
5. Store data in database  
6. Display results on dashboard
   disease_outbreak/ │ ├── outbreak/ │   ├── models.py │   ├── views.py │   ├── urls.py │   ├── templates/ │   │   └── dashboard.html │ ├── manage.py ├── db.sqlite3 └── requirements.txt

---

## ▶️ How to Run the Project

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/disease-outbreak.git
cd disease-outbreak
2️⃣ Install Dependencies
Bash
pip install -r requirements.txt
3️⃣ Run Migrations
Bash
python manage.py migrate
4️⃣ Start Server
Bash
python manage.py runserver
5️⃣ Open in Browser

http://127.0.0.1:8000/dashboard/
🔑 API Configuration
Update your API key in views.py:
Python
NEWS_API_KEY = "your_api_key_here"
📊 Dashboard Modules
🧾 Table View
Displays outbreak reports with:
Location
Disease
Probability
Prediction
🌍 Global Map
Shows outbreak locations using markers
📈 Trend Chart
Displays monthly outbreak trends
⚠️ Limitations
Uses keyword-based detection (not full ML model)
Depends on external APIs
Location assignment is approximate
🔮 Future Enhancements
🤖 Integrate ML model for better prediction
📍 Use real geolocation APIs
📡 Real-time streaming data
🔥 Heatmap visualization
📊 Advanced analytics dashboard
👨‍💻 Author
Mukesh (Anantha Mukesh)
Final Year B.Tech – CSE
📜 License
This project is for academic and learning purposes.
⭐ Acknowledgements
News API
WHO Data API
Django Documentation

---

## 📂 Project Structure
