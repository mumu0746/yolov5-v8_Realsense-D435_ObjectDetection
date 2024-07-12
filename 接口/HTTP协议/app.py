from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

# 它指定了当HTTP请求的路径为/transfer，且请求方法为GET时，将调用transfer_data函数来处理这个请求
@app.route('/transfer', methods=['GET'])
def transfer_data():
    # 检查是否有文件在POST请求中
    if 'file' in request.files:
        file = request.files['file']
        
        # 指定文件保存的路径
        file.save('/home/max/桌面/python/接口/data.txt')
        return jsonify({'message': 'File received successfully'}), 200
    
    elif 'coordinates' in request.form:
        coordinates = request.form['coordinates']
        # 这里可以添加处理三维坐标的逻辑
        return jsonify({'message': 'Coordinates received successfully', 'coordinates': coordinates}), 200
    
    else:
        return jsonify({'error': 'No file or coordinates provided'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)