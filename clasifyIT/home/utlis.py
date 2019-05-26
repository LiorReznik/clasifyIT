from keras.preprocessing.image import img_to_array
import numpy as np

def prepare_image(image, target_size):
	if image.mode != "RGB":
		image = image.convert("RGB")

	image = image.resize(target_size)
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)

	return image