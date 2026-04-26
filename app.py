from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        predictions = []
        
        for case in data['cases']:
            current_desc = case['current_study']['study_description'].lower()
            
            for prior in case['prior_studies']:
                prior_desc = prior['study_description'].lower()
                
                # Simple logic: same body part = relevant
                body_parts = ['brain', 'head', 'chest', 'abdomen', 'spine', 'pelvis', 'knee', 'shoulder']
                is_relevant = any(
                    word in current_desc and word in prior_desc
                    for word in body_parts
                )
                
                predictions.append({
                    'case_id': case['case_id'],
                    'study_id': prior['study_id'],
                    'predicted_is_relevant': is_relevant
                })
        
        return jsonify({'predictions': predictions})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': 'Radiology API is running'})

if __name__ == '__main__':
    print("Starting server on http://localhost:8000")
    app.run(host='0.0.0.0', port=8000, debug=True)