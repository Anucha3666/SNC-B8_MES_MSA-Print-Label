from flask import Blueprint, current_app, jsonify, request

from app.services import print_hello_world, print_label
from app.utils import jsonifyContentType

print_blueprint = Blueprint("print", __name__, url_prefix="/api/print")

@print_blueprint.route('', methods=['GET'])
def get_print_test():
    return print_hello_world()
    
@print_blueprint.route('', defaults={'id': 0}, methods=['POST'])
@print_blueprint.route('/<int:id>', methods=['POST'])
def post_print_label(id):
    if request.content_type != 'application/json':
        return jsonifyContentType()
    req = request.json or {}
        
    return print_label(req, int(id))