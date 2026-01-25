from flask import Blueprint, request, jsonify
from services.pub_service import PubService

pub_controller = Blueprint('pub_controller', __name__)
service = PubService()

# get all pubs
@pub_controller.route('/publications', methods=['GET'])
def list_pubs():
    return jsonify(service.get_all_pubs())

# get specific pub
@pub_controller.route('/publications/<string:pubname>', methods=['GET'])
def get_pub(pubname):
    pub = service.get_pub(pubname)
    if not pub:
        return jsonify({"error" : "not found"}), 404
    #new comment
    return jsonify(pub), 200

# delete specific pub
@pub_controller.route('/publications/<string:pubname>', methods=['DELETE'])
def delete_pub(pubname):
    isThere = service.get_pub(pubname)
    # name isThere differently - not a bool var, but a pub object or None
    if not isThere:
        return jsonify({"error" : "not found"}), 404
    success = service.delete_pub_by_name(pubname)
    if not success:
        return jsonify({"error" : "not deleted"}), 500
    return jsonify({"message" : "pub deleted"}), 200

@pub_controller.route('/publications', methods=['POST'])
def create():
    data = request.get_json(silent=True) or {}
    #instead of data, make publication.py object
    pubname = data.get("pubname")
    table = data.get("table")

    if not pubname or not table:
        return jsonify({"error" : "pubname and table are required"}), 400

    success = service.create_pub(pubname, table) # send data as param - in repo, check for properties
    # check if the publication has been created in this and put

    if not success:
        return jsonify({"error" : "publication not created"}), 500
    # returns the created pub
    pub = service.get_pub(pubname)
    return jsonify(pub), 201

@pub_controller.route('/publications/<string:pubname>', methods=['PUT'])
def update_pub_publish(pubname):
    data = request.get_json(silent=True) or {}
    publish_ops = data.get("publish")

    if not publish_ops or not isinstance(publish_ops, list):
        return jsonify({"error" : "publish info required"}), 400

    allowed = {"insert", "update", "delete", "truncate"}
    publish_ops = [p.lower().strip() for p in publish_ops]
    if any(p not in allowed for p in publish_ops):
        return jsonify({"error": f"publish options must be subset of {sorted(allowed)}"}), 400

    success = service.update_pub(pubname, publish_ops)
    if not success:
        return jsonify({"error" : "publication not found"}), 404

    pub = service.get_pub(pubname)
    return jsonify(pub), 200