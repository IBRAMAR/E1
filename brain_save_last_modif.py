from io import BytesIO
from PIL import Image
path = './TRAIN_CROP/YES/74.jpg'
image_bytes = open(path, "rb").read()
img_crop = Image.open(BytesIO(image_bytes))
img_crop = np.expand_dims(img_crop, axis=0)
#imp_prepro = preprocess_imgs(set_name=[img_crop], img_size=IMG_SIZE)
imp_prepro = preprocess_imgs(set_name=img_crop, img_size=IMG_SIZE)
pred = model.predict_classes(imp_prepro)
result = ["pas de tumeur " if pred[0][0] == 0 else "Possible presence de tumeur"]
print(result[0])

img_crop = cv2.imread('./TRAIN_CROP/YES/74.jpg')
#img_crop = cv2.imread('./TRAIN_CROP/NO/10.jpg')
img_crop = np.expand_dims(img_crop, axis=0)
#imp_prepro = preprocess_imgs(set_name=[img_crop], img_size=IMG_SIZE)
imp_prepro = preprocess_imgs(set_name=img_crop, img_size=IMG_SIZE)
pred = model.predict_classes(imp_prepro)
result = ["pas de tumeur " if pred[0][0] == 0 else "Possible presence de tumeur"]
print(result[0])