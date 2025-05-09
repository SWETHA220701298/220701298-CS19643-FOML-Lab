from flask import Blueprint, request, jsonify
from ai.face_model import analyze_skin

face_bp = Blueprint('face', __name__)

@face_bp.route('/analyze-face', methods=['POST'])
def analyze():
    image = request.files.get('image')
    if not image:
        return jsonify({"error": "No image uploaded"}), 400

    image_bytes = image.read()
    tone, texture, tip, products = analyze_skin(image_bytes)
    

    return jsonify({
        "tone": tone,
        "texture": texture,
        "tip": tip,
        "products": products
    })
