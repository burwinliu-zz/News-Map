import os

from flask import Flask, jsonify, request, render_template, Blueprint, json

from server.to_frontend import get_colour_data, get_news_item, get_country_name
from server.database_access.config.setup import setup_globals

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

print(template_dir)
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(template_dir) if isfile(join(template_dir, f))]
print(onlyfiles)

def get_app():
    return app


@app.route('/data', methods=['GET'])
def test():
    if request.method == 'GET':
        iso_code = request.args.get('iso')
        res = get_news_item(iso_code)
        return jsonify(res)


@app.route('/data_country_name', methods=['GET'])
def get_name():
    if request.method == 'GET':
        iso_code = request.args.get('iso')
        res = get_country_name(iso_code)
        return jsonify({'code': res})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/map')
def map_page():
    res = json.dumps(get_colour_data())
    return render_template('map.html', result=res)


@app.route('/display-news')
def display_news():
    pass


@app.route("/contact")
def contact():
    pass


@app.route('/about')
def about():
    pass


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
    app.run(
        host=os.getenv('LISTEN', '0.0.0.0'),
        debug= True,
        port=5000
    )
