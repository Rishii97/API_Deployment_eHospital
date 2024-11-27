from flask import Flask, jsonify, request, render_template
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "shaalimaar@1",
    "database": "e_hospital"
}

# Function to connect to the database
def get_db_connection():
    return mysql.connector.connect(**db_config)

# API endpoint to fetch data from a specific table
@app.route('/table/<table_name>', methods=['GET'])
def get_table_data(table_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = f"SELECT * FROM `{table_name}` LIMIT 100;"
        cursor.execute(query)
        records = cursor.fetchall()
    except mysql.connector.Error as err:
        conn.close()
        return jsonify({"error": str(err)}), 400

    conn.close()
    return jsonify(records)

# API endpoint to insert data into a specific table
@app.route('/table/<table_name>', methods=['POST'])
def insert_table_data(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = tuple(data.values())

        query = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"
        cursor.execute(query, values)
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        conn.close()
        return jsonify({"error": str(err)}), 400

    conn.close()
    return jsonify({"message": "Data inserted successfully"}), 201

# Route for Welcome Page
@app.route('/')
def welcome_page():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
