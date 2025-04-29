from flask import Flask, render_template, request
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ml.predict import predict_match



app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/', methods=['GET', 'POST'])
def home():
    donor_info = None
    confidence = None

    if request.method == 'POST':
        blood_type = request.form['blood_type']
        organ_type = request.form['organ_type']
        age = int(request.form['age'])
        urgency = int(request.form['urgency'])

        recipient = {
            'blood_type': blood_type,
            'organ_type': organ_type,
            'age': age,
            'urgency': urgency
        }

        result = predict_match(recipient)
        
        if result.get('match'):
            donor_info = result['donor']
            confidence = result['confidence']

    return render_template('index.html', donor=donor_info, confidence=confidence)

if __name__ == '__main__':
    app.run(debug=True)
