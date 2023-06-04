from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/trigger_report', methods=['POST'])
def trigger_report():
    # Generate a random report_id
    report_id = generate_report_id()
    
  
    
    response = {
        'report_id': report_id
    }
    return jsonify(response)

def generate_report_id():
    # Generate a random alphanumeric report_id
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    report_id = ''.join(random.choice(chars) for _ in range(10))
    return report_id

if __name__ == '__main__':
    app.run()
