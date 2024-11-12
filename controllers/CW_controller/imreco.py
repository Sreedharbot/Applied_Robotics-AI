# make a prediction for a new image.
from tensorflow.keras import preprocessing
from tensorflow.keras import  models
import numpy as np

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']


# load and prepare the image
def load_image(filename):
	# load the image
	img = preprocessing.image.load_img(filename, target_size=(32, 32))
	# convert to array
	img = preprocessing.image.img_to_array(img)
	# reshape into a single sample with 3 channels
	img = img.reshape(1, 32, 32, 3)
	# prepare pixel data
	img = img.astype('float32')
	img = img / 255.0
	return img

# load an image and predict the class
def run_example():
	# load the image
	img = load_image('dog.png')
	# load model
	model = models.load_model('final_model.h5')
	# predict the class
	pred_list = model.predict(img)
	result = np.argmax(pred_list[0])
	print("Prediction:", class_names[result])

# run the example
run_example()