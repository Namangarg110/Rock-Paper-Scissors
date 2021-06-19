from tensorflow.keras.models import load_model
import cv2
import numpy as np
import sys

path = sys.argv[1]

REV_CLASS_MAP = {
    0: "none",
    1: "paper",
    2: "rock",
    3: "scissors"
}


def mapper(val):
    return REV_CLASS_MAP[val]


model = load_model("rock-paper-scissors-model.h5")

img = cv2.imread(path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.resize(img, (227, 227))

# predict the move made
pred = model.predict(np.array([img]))
move_code = np.argmax(pred[0])
move_name = mapper(move_code)


print("Predicted: {}".format(move_name))