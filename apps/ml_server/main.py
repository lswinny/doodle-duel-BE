from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from quickdraw import QuickDrawData
from PIL import Image, ImageDraw
import io, base64, numpy as np

app = FastAPI()

# Allow frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize QuickDraw
qd = QuickDrawData()

# Categories to check
CATEGORIES = ["cat", "tree", "house", "car"]

# Helper Functions

def convert_user_strokes(raw_strokes):
    """
    Convert user strokes from [{'x':..,'y':..}, ...] to QuickDraw format [[xs], [ys]]
    """
    xs = [p["x"] for p in raw_strokes]
    ys = [p["y"] for p in raw_strokes]
    return [xs, ys]

def convert_frontend_strokes_to_quickdraw(strokes):
    """
    Convert list of strokes where each stroke is a list of {'x':..,'y':..}
    into QuickDraw format: [[x_coords], [y_coords]]
    """
    converted = []

    for stroke in strokes:
        xs = [p["x"] for p in stroke]
        ys = [p["y"] for p in stroke]
        converted.append([xs, ys])

    return converted

def preprocess_canvas_image(data_url):
    """
    Convert base64 canvas image to 28x28 greyscale numpy array
    """
    img_bytes = base64.b64decode(data_url.split(",")[1]) # convert the text string into bytes we can read as an image
    img = Image.open(io.BytesIO(img_bytes)).convert("L") # greyscale
    img = img.resize((28,28))
    arr = np.array(img)/255.0
    return arr

def strokes_to_vector(strokes, total_points=200):
    """
    Convert a list of strokes [[xs], [ys], ...] into a single fixed-length vector.
    This resamples the entire drawing to `total_points` points.
    """
    all_x = []
    all_y = []

    for stroke in strokes:
        if len(stroke) != 2:
            continue
        x, y = stroke
        if len(x) == 0 or len(y) == 0:
            continue
        all_x.extend(x)
        all_y.extend(y)

    if len(all_x) == 0:
        return np.zeros(total_points * 2)  # empty drawing

    # Interpolate all points to fixed total_points
    x_resampled = np.interp(np.linspace(0, len(all_x)-1, total_points), np.arange(len(all_x)), all_x)
    y_resampled = np.interp(np.linspace(0, len(all_y)-1, total_points), np.arange(len(all_y)), all_y)

    return np.concatenate([x_resampled, y_resampled])

def find_best_match(user_strokes, categories=CATEGORIES, samples=50):
    """
    Compare user drawing/stroke vector to a few QuickDraw stroke samples
    """
    best_category = None
    min_error = float("inf")

    user_vec = strokes_to_vector(user_strokes)

    for cat in categories:
        for _ in range(samples):
            d = qd.get_drawing(cat)
            sample_vec = strokes_to_vector(d.strokes)

            error = np.mean((user_vec - sample_vec) ** 2)
            if error < min_error:
                min_error = error
                best_category = cat

    return best_category, float(min_error)

# API endpoint

@app.post("/api/submit")
async def submit_drawing(request: Request):
    data = await request.json()
    data_url = data.get("image")
    user_strokes_raw = data.get("strokes", [])
    user_strokes = convert_frontend_strokes_to_quickdraw(user_strokes_raw)

    print("RAW STROKES FROM FRONTEND:", user_strokes_raw[:1])
    print("CONVERTED TO QUICKDRAW:", user_strokes[:1])

    if not data_url or not user_strokes:
        return {"error": "No image or strokes provided"}
    
    best_category, error = find_best_match(user_strokes)

    return {
        "message": "Drawing processed",
        "best_category": best_category,
        "match_error": error
    }