import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn
from io import BytesIO
from PIL import Image
from typing import Tuple
import tensorflow as tf

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL = tf.keras.models.load_model("C:/Users/AbdulwajeedOlaniyiGa/Princess Project/saved model/1")
CLASS_NAMES = ['anthracnose	belly_rot','gummy_stem_blight','healthy_leaf','bacterial_wilt','downy_mildew','healthy_cucumber','pythium_fruit_rot']

       
	  	 




def read_file_as_image(data) -> Tuple[np.ndarray, Tuple[int, int]]:
    img = Image.open(BytesIO(data)).convert('RGB')
    img_resized = img.resize((256, 256), resample=Image.BICUBIC)
    image = np.array(img_resized)
    return image, img_resized.size


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image, img_size = read_file_as_image(await file.read())
        img_batch = np.expand_dims(image, 0)

        predictions = MODEL.predict(img_batch)
        predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
        confidence = np.max(predictions[0])

        return {
            'class': predicted_class,
            'confidence': float(confidence)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


'''@app.get("/", response_class=HTMLResponse)
async def index():
    with open("main.html", "r") as file:
        return file.read()'''



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8003)