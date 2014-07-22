import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.wsgi import SharedDataMiddleware
from retask.queue import Queue
from retask.task import Task


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['log', 'txt'])

APP = Flask(__name__)
APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
APP.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
APP.wsgi_app = SharedDataMiddleware(APP.wsgi_app, {
    '/uploads':  APP.config['UPLOAD_FOLDER']
})
APP.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@APP.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(APP.config['UPLOAD_FOLDER'], filename))
            # Now add the information in the queue for processing
            t = Task({'filename': filename})
            queue = Queue('incoming_files')
            queue.connect()
            queue.enqueue(t)
            return "Log uploaded."

    return '''
    <!doctype html>
    <head>
        <title>Upload new File</title>
    </head>
    <body>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    </body>
    </html>
    '''

if __name__ == '__main__':
    APP.debug=True
    APP.run()