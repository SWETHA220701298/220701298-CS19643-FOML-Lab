import io
import base64
from PIL import Image
import google.generativeai as genai

# Set your Gemini API key here
genai.configure(api_key="AIzaSyDDk2hTy44kcr-zjiYED7Z_CUfxU6TVx6o")  # Replace with your actual API key

model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_skin(image_bytes):
    try:
        # Prepare image as JPEG
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_data = buffered.getvalue()

        # Gemini expects MIME type and raw data in inline_data
        prompt = """
Analyze the given face image and respond ONLY in the format below:

Tone: <Fair | Medium | Dark>
Texture: <Dry | Oily | Combination | Sensitive | Normal>
Tip: <one unique skincare tip>
Products:
- <product name> - <brand> WITH LINK WHICH GOES TO PARTICULAR WEBSITE WHEN CLICKED
- <product name> - <brand> WITH LINK WHICH GOES TO PARTICULAR WEBSITE WHEN CLICKED
"""

        response = model.generate_content([
            {"text": prompt},
            {
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": img_data
                }
            }
        ])

        full_text = response.text
        print("Gemini raw response:\n", full_text)  # Debug print

        tone = extract_field(full_text, "Tone")
        texture = extract_field(full_text, "Texture")
        tip = extract_field(full_text, "Tip")
        products = extract_products(full_text)

        return tone, texture, tip, products

    except Exception as e:
        print("Gemini Error:", e)
        return "Unknown", "Unknown", "AI tip not available.", []

def extract_field(text, field_name):
    for line in text.splitlines():
        if line.strip().startswith(f"{field_name}:"):
            return line.split(":", 1)[1].strip()
    return "Unknown"

def extract_products(text):
    products = []
    start = False
    for line in text.splitlines():
        if "Products:" in line:
            start = True
            continue
        if start and line.strip().startswith("-"):
            product_line = line.replace("-", "").strip()
            if product_line not in products:
                products.append(product_line)
    return products[:2]  # return only 2 products


