from PIL import Image, ImageEnhance
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers


# gets an img name and returns only the volt
def get_volt_from_img_name(name:str)->float:
    return float(name.split('_')[-1].replace('.png',''))


def data_generator(inputDataPath:str, outputDataPath:str, batchSize:int, train_mode:bool=True,  resized_width:int=None, resized_height:int=None):
    '''
    :return: a generator of a bach of data(input,output) from the dataPath dir,
             in the size of batchSize.
             the data will all resize to dim : (resized_width, resized_height),
             then flattend.
             the input is a flattend img + input and output volteges + their subtraction
             the output is is a flattend img
    '''
    a = os.scandir(inputDataPath)
    b = os.scandir(outputDataPath)
    while True:
        input = [0]*batchSize
        output = [0]*batchSize
        for i in range(batchSize):
            try:
                input_file_name = next(a).name
                output_file_name = next(b).name
            except StopIteration:
                if train_mode:
                    a = os.scandir(inputDataPath)
                    b = os.scandir(outputDataPath)
                    input_file_name = next(a).name
                    output_file_name = next(b).name
                else:
                    raise StopIteration

            input_img = cv2.imread(os.path.join(inputDataPath,input_file_name), cv2.IMREAD_GRAYSCALE)
            output_img = cv2.imread(os.path.join(outputDataPath,output_file_name), cv2.IMREAD_GRAYSCALE)
            # ensures all images be the same size:
            if resized_height is not None:
                input_img = cv2.resize(input_img, (resized_width, resized_height))
                output_img = cv2.resize(output_img, (resized_width, resized_height))
            input_volt = get_volt_from_img_name(input_file_name)
            output_volt = get_volt_from_img_name(output_file_name)
            # flatten images to vectors, and adds vols to input:
            input[i] = np.append(input_img.flatten(),
                            [input_volt, output_volt, output_volt-input_volt])  # todo : divide by 255, just img or volts too?
            output[i] = output_img.flatten()
        yield input, output


def img_from_input(input:np.array, resized_width:int, resized_height:int):
    flattened_img = np.delete(input, [-1, -2, -3])
    return flattened_img.reshape([resized_width, resized_height])


def img_from_output(output:np.array, resized_width:int, resized_height:int):
    return output.reshape([resized_width, resized_height])



               ########### Model Construction ###########

#(based on keras example: Next-Frame Video Prediction with Convolutional LSTMs)

##constants:
resized_width=10**3
resized_height=10**3
input_shape = resized_width*resized_height+3
trainingInputDataPath = './data/train/input'
trainingOutputDataPath = './data/train/output'
testingInputDataPath = './data/test/input'
testingOutputDataPath = './data/test/output'
# Define modifiable training hyperparameters.
epochs = 20
batch_size = 5

# Construct the input layer.
inp = layers.Input(shape=(input_shape,))

# We will construct 3 `ConvLSTM2D` layers with batch normalization,
# followed by a `Conv3D` layer for the spatiotemporal outputs.
x = layers.ConvLSTM2D(
    filters=64,
    kernel_size=(5, 5),
    padding="same",
    return_sequences=True,
    activation="relu",
)(inp)
x = layers.BatchNormalization()(x)
x = layers.ConvLSTM2D(
    filters=64,
    kernel_size=(3, 3),
    padding="same",
    return_sequences=True,
    activation="relu",
)(x)
x = layers.BatchNormalization()(x)
x = layers.ConvLSTM2D(
    filters=64,
    kernel_size=(1, 1),
    padding="same",
    return_sequences=True,
    activation="relu",
)(x)
x = layers.Conv3D(
    filters=1, kernel_size=(3, 3, 3), activation="sigmoid", padding="same"
)(x)

# Next, we will build the complete model and compile it.
model = keras.models.Model(inp, x)
model.compile(
    loss=keras.losses.binary_crossentropy, optimizer=keras.optimizers.Adam(),
)

# Define some callbacks to improve training.
early_stopping = keras.callbacks.EarlyStopping(monitor="val_loss", patience=10)
reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor="val_loss", patience=5)

# initialize data gen.
training_data_gen = data_generator(trainingInputDataPath, trainingOutputDataPath, batch_size)
testing_data_gen = data_generator(testingInputDataPath, testingOutputDataPath, batch_size)

# Fit the model to the training data.
model.fit(
    training_data_gen,
    batch_size=batch_size,
    epochs=epochs,
    validation_data=testing_data_gen,
    callbacks=[early_stopping, reduce_lr],
)

     ##### Frame Prediction Visualizations #####

# Select a random example from the validation dataset.
frame, original_ext_frame = next(testing_data_gen)


# Extract the model's prediction and post-process it.
new_prediction = model.predict(np.expand_dims(frame, axis=0))
new_prediction = np.squeeze(new_prediction, axis=0)
predicted_frame = np.expand_dims(new_prediction, axis=0)

# Construct a figure for the original and new frames.
fig, axes = plt.subplots(3, 1, figsize=(20, 4))

# Plot the input frame.
ax = axes[0]
ax.imshow(np.squeeze(img_from_input(frame)), cmap="gray")
ax.set_title(f"input frame")
ax.axis("off")

# Plot the original new frame.
ax = axes[1]
ax.imshow(np.squeeze(img_from_output(original_ext_frame)), cmap="gray")
ax.set_title(f"original frame")
ax.axis("off")

# Plot the new frame.
ax = axes[2]
ax.imshow(np.squeeze(img_from_output(predicted_frame)), cmap="gray")
ax.set_title(f"new frame")
ax.axis("off")

# Display the figure.
plt.show()










if __name__ == '__main__':
    for i,j in enumerate(data_generator('./data/train/input', './data/train/output', 2)):
        print(j)
        break
    # print(next(gen))
    # print(next(gen))