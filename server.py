import os
import pandas as pd
from flask import Flask, jsonify, request

DATA_FILE = os.getenv("DATAJUD_FILE", "datajud.csv")

app = Flask(__name__)

# Load DataJUD into memory on startup
if os.path.isfile(DATA_FILE):
    datajud_df = pd.read_csv(DATA_FILE)
else:
    datajud_df = pd.DataFrame()

@app.route('/datajud', methods=['GET'])
def list_processes():
    """Return all records from the DataJUD dataset."""
    return jsonify(datajud_df.to_dict(orient='records'))

@app.route('/datajud/<int:record_id>', methods=['GET'])
def get_process(record_id):
    """Return a single record by its id."""
    if datajud_df.empty:
        return jsonify({'error': 'dataset not loaded'}), 500
    match = datajud_df[datajud_df['id'] == record_id]
    if match.empty:
        return jsonify({'error': 'not found'}), 404
    return jsonify(match.iloc[0].to_dict())

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
