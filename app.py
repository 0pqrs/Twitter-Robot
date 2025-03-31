from flask import Flask, render_template_string
from scraper import TwitterRobot
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# HTML template for displaying trends
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Twitter Trending Topics</title>
    <style>
        body { 
            font-family: Arial; 
            margin: 40px; 
            background-color: #f0f0f0;
        }
        button { 
            padding: 10px 20px; 
            background-color: #1da1f2;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .trends { 
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>Twitter Trends Robot</h1>
    {% if trends %}
    <div class="trends">
        <h2>Popular topics as of {{ trends.timestamp }}:</h2>
        <ul>
            <li>{{ trends.nameoftrend1 }}</li>
            <li>{{ trends.nameoftrend2 }}</li>
            <li>{{ trends.nameoftrend3 }}</li>
            <li>{{ trends.nameoftrend4 }}</li>
            <li>{{ trends.nameoftrend5 }}</li>
        </ul>
        <p>Using computer address: {{ trends.ip_address }}</p>
        <pre>{{ json_data }}</pre>
    </div>
    {% endif %}
    <button onclick="window.location.href='/'">Get New Trends</button>
</body>
</html>
"""

@app.route('/')
def home():
    # When someone visits our website
    robot = TwitterRobot()
    trends = robot.get_trending_topics()
    return render_template_string(
        HTML_TEMPLATE,
        trends=trends,
        json_data=json.dumps(trends, default=str, indent=2)
    )

if __name__ == '__main__':
    app.run(debug=True)
