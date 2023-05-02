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

config = {
  'ORIGINS': [
    'http://localhost:3000',  # React
    'http://172.16.0.36:3000',  # React
  ],
}

CORS(app, resources={ r'/*': {'origins': config['ORIGINS']}}, supports_credentials=True)


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
