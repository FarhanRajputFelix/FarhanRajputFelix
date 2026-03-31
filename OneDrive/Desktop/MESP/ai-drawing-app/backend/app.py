from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import base64
from io import BytesIO
from PIL import Image, ImageOps

app = Flask(__name__)
CORS(app)

# Load model and classes
try:
    model = tf.keras.models.load_model('model.h5')
    with open('classes.txt', 'r') as f:
        CLASSES = [line.strip() for line in f.readlines()]
    print("Model and classes loaded successfully.")
except Exception as e:
    print(f"Error loading model/classes: {e}")
    model = None
    CLASSES = []

def preprocess_image(base64_str):
    # Remove header if present
    if ',' in base64_str:
        base64_str = base64_str.split(',')[1]
        
    # Decode image
    image_data = base64.b64decode(base64_str)
    image = Image.open(BytesIO(image_data))
    
    # Must convert to RGBA then extract alpha or convert to grayscale intelligently
    # Because canvas drawing might be black strokes on transparent background
    if image.mode == 'RGBA':
        # Create a white background image
        background = Image.new('RGBA', image.size, (255, 255, 255))
        alpha_composite = Image.alpha_composite(background, image)
        image = alpha_composite.convert('L')
    else:
        image = image.convert('L')
        
    # Resize to 28x28 used in QuickDraw dataset
    image = image.resize((28, 28), Image.Resampling.LANCZOS)
    
    # Invert colors: QuickDraw has white strokes (255) on black background (0)
    # Our canvas has black strokes on white background
    image = ImageOps.invert(image)
    
    # Convert to numpy array and normalize
    img_array = np.array(image).astype('float32') / 255.0
    
    # Reshape for model (1, 28, 28, 1)
    img_array = img_array.reshape(1, 28, 28, 1)
    
    return img_array

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
        
    try:
        data = request.json
        if 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400
            
        img_array = preprocess_image(data['image'])
        
        # Predict
        predictions = model.predict(img_array)[0]
        
        # Get top 3 predictions
        top_indices = predictions.argsort()[-3:][::-1]
        results = [{'class': CLASSES[i], 'confidence': float(predictions[i])} for i in top_indices]
        
        return jsonify({
            'prediction': results[0]['class'],
            'confidence': results[0]['confidence'],
            'top_3': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
