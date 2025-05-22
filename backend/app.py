from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'PricePulse: Price Tracker'
    })

if __name__ == '__main__':
    app.run(debug=True)
