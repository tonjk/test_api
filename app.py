from flask import Flask,request,jsonify

app = Flask(__name__)

# check health path
@app.route('/healthy',methods=['GET'])
def test_api():
    return 'Testing API is completed.', 200

@app.route('/test_post',methods=['POST'])
def test_post():
    data = request.json
    sentence = data.get('sentence')
    response = str(sentence) + ' ' + 'Thank you for your request. ^^'
    return jsonify({"response": response}), 200
    


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
