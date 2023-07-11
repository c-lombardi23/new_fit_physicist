from flask import Blueprint, send_from_directory
import app

uploads_bp = Blueprint('uploads', __name__)

@uploads_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)