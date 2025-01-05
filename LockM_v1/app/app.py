from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from hdfs import InsecureClient
import os
from datetime import datetime
import logging
# In app.py, add these imports and setup
from flask_wtf.csrf import CSRFProtect

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key'
# csrf = CSRFProtect(app)



# HDFS client setup
HDFS_HOST = os.getenv('HDFS_HOST', 'namenode')
HDFS_PORT = os.getenv('HDFS_PORT', '9870')
HDFS_URL = f'http://{HDFS_HOST}:{HDFS_PORT}'

# Initialize HDFS client with retry logic
def get_hdfs_client():
    try:
        client = InsecureClient(HDFS_URL)

        logger.info(f"Successfully connected to HDFS at {HDFS_URL}")
        # Test the connection
        client.status('/')
        logger.info(f"Successfully connected to HDFS at {HDFS_URL}")
        return client
    
    except Exception as e:
        logger.error(f"Failed to connect to HDFS: {e}")
        return None

# hdfs_client = get_hdfs_client()
HDFS_PATH = '/files'

# Ensure the base directory exists
# if hdfs_client:
#     try:
#         hdfs_client.makedirs(HDFS_PATH)
#         logger.info(f"Ensured HDFS directory exists: {HDFS_PATH}")
#     except Exception as e:
#         logger.error(f"Error creating HDFS directory: {e}")

@app.route('/')
def index():
    try:
        hdfs_client = get_hdfs_client()
        files = []
        for file_status in hdfs_client.list(HDFS_PATH, status=True):
            filename, status = file_status
            files.append({
                'name': filename,
                'size': status['length'],
                'modified': datetime.fromtimestamp(status['modificationTime']/1000).strftime('%Y-%m-%d %H:%M:%S'),
                'permissions': status['permission']
            })
        return render_template('index.html', files=files)
    except Exception as e:
        flash(f'Error listing files: {str(e)}', 'error')
        return render_template('index.html', files=[])

@app.route('/edit/<filename>', methods=['GET'])
def edit_file(filename):
    hdfs_client = get_hdfs_client()
    hdfs_path = os.path.join(HDFS_PATH, filename)
    try:
        with hdfs_client.read(hdfs_path) as reader:
            content = reader.read().decode('utf-8')
        return render_template('index.html', filename=filename, content=content)
    except Exception as e:
        flash(f'Error reading file: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/read/<filename>')
def read_file(filename):
    hdfs_client = get_hdfs_client()
    hdfs_path = os.path.join(HDFS_PATH, filename)
    try:
        with hdfs_client.read(hdfs_path) as reader:
            content = reader.read().decode('utf-8')
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    hdfs_client = get_hdfs_client()
    hdfs_path = os.path.join(HDFS_PATH, filename)
    try:
        hdfs_client.delete(hdfs_path)
        flash(f'File {filename} deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting file: {str(e)}', 'error')
    return redirect(url_for('index'))

@app.route('/create_file', methods=['GET', 'POST'])
def create_file():
    hdfs_client = get_hdfs_client()
    if request.method == 'POST':
        logger.info("Received POST request to /create_file")
        logger.info(f"Request headers: {request.headers}")
        logger.info(f"Request form data: {request.form}")

        filename = request.form.get('filename', '')
        content = request.form.get('content', '')

        logger.info(f"Filename: {filename}")
        logger.info(f"Content: {content}")

        if not filename:
            logger.error("Filename is required!")
            flash('Filename is required!', 'error')
            return redirect(url_for('index'))

        if not filename.endswith('.txt'):
            filename += '.txt'

        hdfs_path = os.path.join(HDFS_PATH, filename)

        try:
            if hdfs_client.status(hdfs_path, strict=False) is not None:
                logger.error("File already exists!")
                flash('File already exists! Use edit function to modify.', 'error')
                return redirect(url_for('index'))

            with hdfs_client.write(hdfs_path) as writer:
                writer.write(content.encode('utf-8'))
            logger.info(f"File {filename} created successfully!")
            flash(f'File {filename} created successfully!', 'success')
        except Exception as e:
            logger.error(f"Error creating file: {str(e)}")
            flash(f'Error creating file: {str(e)}', 'error')

        return redirect(url_for('index'))
    logger.info("Received GET request to /create_file")
    return redirect(url_for('index'))


@app.route('/update/<filename>', methods=['GET', 'POST'])
def update_file(filename):
    hdfs_client = get_hdfs_client()
    if request.method == 'POST':
        hdfs_path = os.path.join(HDFS_PATH, filename)
        content = request.form.get('content', '')
        
        try:
            with hdfs_client.write(hdfs_path, overwrite=True) as writer:
                writer.write(content.encode('utf-8'))
            flash(f'File {filename} updated successfully!', 'success')
        except Exception as e:
            flash(f'Error updating file: {str(e)}', 'error')
        
        return redirect(url_for('index'))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)