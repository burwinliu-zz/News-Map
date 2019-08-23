from flask import Flask, jsonify, request, render_template, Blueprint, json
import os
from webpage.server.settings import setup_globals
from webpage.server.bridge.to_frontend import get_colour_data

# FOR TESTING PURPOSES USED ENV VARIABLE TODO get working version
setup_globals()
template_dir = os.getenv('PATH_TO_CLIENT_ROOT')
public_dir = os.getenv('PATH_TO_PUBLIC_ROOT')

statics_dir = os.getenv("PATH_TO_STATIC_ROOT")

data_dir = os.getenv('PATH_TO_DATA_ROOT')

styles_dir = os.getenv('PATH_TO_STYLES_ROOT')
scripts_dir = os.getenv('PATH_TO_SCRIPTS_ROOT')

app = Flask(__name__, template_folder=template_dir, static_url_path='/public', static_folder=public_dir)

statics = Blueprint('site', __name__, static_url_path='/static', static_folder=statics_dir)
app.register_blueprint(statics)


def get_app():
    return app


@app.route('/test')
def test():
    res = json.dumps(get_colour_data())
    return render_template('test.html', result=res)


@app.route('/')
def index():
    res = json.dumps(get_colour_data())
    return render_template('index.html', result=res)


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    # POST request
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        return 'OK', 200

    # GET request
    else:
        message = {'greeting': 'Hello from Flask!', 'test_template': template_dir}
        return jsonify(message)  # serialize and use JSON headers


@app.route('/colours/updated_colours', methods=['GET'])
def public_files():
    # look inside `templates` and serve `index.html`
    return jsonify(get_colour_data())


if __name__ == '__main__':
    app.run(debug=True)
