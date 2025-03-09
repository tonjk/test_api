from flask import Flask,request,jsonify

app = Flask(__name__)

# check health path
@app.route('/',methods=['GET'])
def health_check():
    return 'Hello world, this testing is completed.', 200

@app.route('/test_api',methods=['GET'])
def test_api():
    return 'Testing API is completed.', 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
