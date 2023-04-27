# File: manage.py
# Created at 24/03/2023
# Author Khanh

# from flask_cors import CORS
from flask_cors import CORS
from gevent import monkey
monkey.patch_all()

from src import create_app
from flask_script import Manager

app = create_app()

manager = Manager(app)
cors = CORS(app, resources={r"/v1/*": {"origins": "*"}})

@manager.command
def run():
    """Run in local machine."""
    app.run(host='0.0.0.0', debug=True)

manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()
