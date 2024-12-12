from flask import Flask, jsonify, request
import pandas as pd
import os
from werkzeug.utils import secure_filename
import cherrypy

# Path to the locally saved CSV file
LOCAL_CSV_PATH = "./nifty50_stocks.csv"

app = Flask(__name__)

# Function to fetch and load CSV data locally
def fetch_csv_data():
    if not os.path.exists(LOCAL_CSV_PATH):
        raise FileNotFoundError("The local CSV file does not exist. Ensure the updater script is running.")
    
    df = pd.read_csv(LOCAL_CSV_PATH)
    return df

# Endpoint: Serve the HTML file
@app.route("/")
def serve_html():
    return app.send_static_file("index.html")

# Endpoint: Fetch all stocks
@app.route("/stocks", methods=["GET"])
def get_all_stocks():
    try:
        df = fetch_csv_data()
        df.fillna("", inplace=True)  # Replace NaN with empty strings
        stocks = df.to_dict(orient="records")
        return jsonify(stocks)  # Return valid JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint: Fetch a stock by symbol
@app.route("/stocks/<symbol>", methods=["GET"])
def get_stock(symbol):
    try:
        df = fetch_csv_data().fillna("")
        stock = df[df['Symbol'] == symbol].to_dict(orient="records")  # Match the column name
        if not stock:
            return jsonify({"error": "Stock not found"}), 404
        return jsonify(stock[0])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint: Filter stocks by a column value
@app.route("/stocks/filter", methods=["GET"])
def filter_stocks():
    try:
        column = request.args.get("column")
        value = request.args.get("value")
        if not column or not value:
            return jsonify({"error": "Please provide both 'column' and 'value' query parameters"}), 400
        
        df = fetch_csv_data()
        filtered = df[df[column] == value]
        if filtered.empty:
            return jsonify({"error": "No stocks found matching the filter"}), 404
        return jsonify(filtered.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Configure upload folder and allowed file types
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)  # Prevent filename injection
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the CSV (example: load into pandas DataFrame)
        df = pd.read_csv(file_path)
        
        # Perform any necessary processing or validation on the data
        expected_columns = ['Symbol', 'Day High', 'Day Low', 'Last Price', 'Change', 'PChange']
        if not all(col in df.columns for col in expected_columns):
            return jsonify({"error": "Invalid CSV format. Missing required columns."}), 400
        
        # Example: Send a confirmation response with summary
        return jsonify({
            "message": "File uploaded successfully!",
            "rows": len(df),
            "columns": list(df.columns)
        })
    else:
        return jsonify({"error": "Invalid file type. Only CSV files are allowed."}), 400

if __name__ == "__main__":
    # CherryPy WSGI server configuration
    cherrypy.config.update({
        "server.socket_host": "127.0.0.1",  # Listen on all interfaces
        "server.socket_port": 8080        # Port for the app
    })
    
    # Mount the Flask app
    cherrypy.tree.graft(app.wsgi_app, "/")

    # Start the CherryPy server
    cherrypy.engine.start()
    cherrypy.engine.block()