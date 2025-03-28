import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import generate_zpl_label, print_ascii_art, print_zpl, read_zpl_file

app = Flask(__name__)
CORS(app)

load_dotenv()
DEFAULT_PRINTER = os.getenv("DEFAULT_PRINTER", "zebra_printer")  # Added default value

@app.route('/printtest', methods=['POST'])
def print_label():
    data_request = request.json
    print(data_request)

    if not data_request or not all(key in data_request for key in ['form_data', 'serial_number', 'state']):
        return jsonify({"error": "ข้อมูลไม่ครบถ้วน ต้องมี 'form_data', 'serial_number', และ 'state'"}), 400

    if data_request['state'] != "1":
        return jsonify({"error": "สถานะไม่ถูกต้องสำหรับการพิมพ์"}), 400

    # Generate ZPL content
    zpl_content = generate_zpl_label(data_request)

    if zpl_content:
        try:
            # Print directly using the ZPL content
            print_zpl(zpl_content, DEFAULT_PRINTER)
            return jsonify({
                "message": f"ส่งงานพิมพ์เรียบร้อยแล้วไปยัง {DEFAULT_PRINTER}",
                "current_counter": 1
            })
        except Exception as e:
            return jsonify({"error": f"เกิดข้อผิดพลาดในการพิมพ์: {str(e)}"}), 500
    else:
        return jsonify({"error": "ไม่สามารถสร้าง ZPL content ได้"}), 500

if __name__ == '__main__':
    print_ascii_art()
    print(f"Using printer: {DEFAULT_PRINTER}")
    app.run(host='0.0.0.0', port=5000, debug=True)
