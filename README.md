AuraStyle | Climate-Driven Inventory Routing & Predictive Personalization Pipeline
A production-style, full-stack predictive data engineering application that automates localized asset allocation based on real-time meteorological streams. By integrating third-party REST APIs, a Scikit-Learn decision routing brain, and a persistent MySQL database backend, the system minimizes manual selection friction and delivers active, validated consumer recommendations via an interactive web dashboard.

🛠️ The Production Tech Stack
🌐 Frontend UI Dashboard
Streamlit (Renders dynamic input fields, live metric cards, and vector graphs)

🧠 Algorithmic Engine
Scikit-Learn (Decision Tree Classifier mapping multi-modal threshold patterns)

🔢 Data Transformation Framework
Pandas and NumPy (Manages matrix structures and rolling vector limits)

📡 Live Ingestion Layer
Requests REST API (Harvests live time-series meteorological metrics from OpenWeatherServer)

🗄️ Relational Storage Engine
MySQL Server (Manages persistent asset records via localized Python network sockets)

🏗️ Pipeline Infrastructure Architecture
Automated Telemetry Ingestion Layer
The application initiates a secure network handshake with a remote REST API node, pulling real-time climate parameters like Temperature, Humidity, Wind Speed, and UV Index dynamically based on user localization keys. This eliminates static data reliance.

Machine Learning Evaluation Logic
Instead of fragile, manual hardcoded conditional statements, inputs are instantly routed into a trained Scikit-Learn Decision Tree Classifier. The model maps spatial microclimate boundaries calibrated against 1,000 seasonal tracking records to classify ideal structural silhouette profiles automatically.

Dynamic Relational Routing Filter
Upon model execution, the predicted target profile acts as a routing key. Python opens a localized TCP connection socket to a native MySQL schema, running dynamic indexed queries to check clean status parameters and retrieve available, validated clothing assets instantly.

Feature Interpretability Diagnostics
Leverages Matplotlib visualization frameworks to extract and compute structural Feature Importance Weights directly from the trained decision boundaries, ensuring total model interpretability for technical system operators.

💻 Live Output Matrix Preview
When the data engineering pipeline completes an active execution loop, logs snap into a clean, structured matrix display:

📡 LIVE INGESTION: Udaipur Meteorological Array [34.5°C, 44% Humidity, 31.1 km/h Wind]
🤖 ALGORITHMIC ROUTING: Tagged Profile 0 -> Summer Casual Y2K Silhouette Mapping
🗄️ BACKEND DATABASE QUERY: Executed Transaction handshake over localhost:3306
✨ RUNTIME OUTPUT: Recommended Outfit Combination: Wear your Cobalt Blue Baby Tee.