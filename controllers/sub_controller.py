from flask import Blueprint, request, jsonify
from services.sub_services import SubService

sub_controller = Blueprint('sub_controller', __name__)
service = SubService()

# get all pubs
@sub_controller.route('/subscriptions', methods=['GET'])
def list_subs():
    return jsonify(service.get_subs())