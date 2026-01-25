from flask import Flask
from controllers.pub_controller import pub_controller
from controllers.sub_controller import sub_controller

app = Flask(__name__)
app.register_blueprint(pub_controller)
app.register_blueprint(sub_controller)


print(app.url_map)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)