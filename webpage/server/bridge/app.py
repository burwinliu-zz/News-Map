from flask import Flask, jsonify, request, render_template, send_from_directory
import os
from webpage.server.settings import setup_globals

# FOR TESTING PURPOSES USED ENV VARIABLE TODO get working version
setup_globals()
template_dir = os.getenv('PATH_TO_CLIENT_ROOT')
static_dir = os.getenv('PATH_TO_STATIC_ROOT')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


@app.route('/')
def index():
    return render_template('index.html')


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


@app.route('/static/<path:filename>')
def static_test(filename):
    # look inside `templates` and serve `index.html`
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
