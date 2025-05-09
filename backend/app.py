from flask import Flask
from flask_cors import CORS

# Import your route blueprints
from routes.face import face_bp
#from routes.outfit import outfit_bp

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend (JS) to talk to this backend

# Register Blueprints
app.register_blueprint(face_bp)
#app.register_blueprint(outfit_bp)

@app.route('/')
def home():
    return "Face & Outfit AI API is running"

if __name__ == '__main__':
    app.run(debug=True)
