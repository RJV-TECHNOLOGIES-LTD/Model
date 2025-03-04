from flask import Flask, render_template, jsonify
import psutil

app = Flask(__name__)

@app.route('/performance', methods=['GET'])
def get_performance():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    return jsonify({"cpu": cpu_usage, "ram": ram_usage})

@app.route('/')
def index():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
