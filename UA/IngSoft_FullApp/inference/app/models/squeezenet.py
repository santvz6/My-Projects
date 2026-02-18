from typing import Optional
import numpy as np
from PIL import Image
import io
from onnxruntime import InferenceSession

class SqueezeNet:
    """ SqueezeNet model for image classification. """

    __session: Optional[InferenceSession] = None

    def __init__(self, model_path: str, classes_path: str):
        if self.__session is None:
            self.__session = InferenceSession(model_path)

        # Classes Label
        with open(classes_path, "r") as f:
            self.class_names = [line.strip() for line in f.readlines()]

    def __preprocess_image(self, image_data: bytes) -> np.ndarray:
        """
        Preprocess the image data for SqueezeNet model.
        Resizes the image to 224x224, normalizes it, and converts it to a tensor.
            :param image_data: Image data in bytes.
            :return: Preprocessed image tensor.
        """
        # Convert bytes to image
        image = Image.open(io.BytesIO(image_data))

        # Resize to 224x224 (SqueezeNet input size)
        image = image.resize((224, 224))

        # Convert image to numpy array
        image_array = np.array(image)

        # Normalize the image (important for most pre-trained models)
        # You might need to adjust these values based on the model's requirements.
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        image_array = (image_array - mean) / std

        # Convert image to channel-first format (C, H, W) and add batch dimension
        image_array = np.transpose(image_array, (2, 0, 1))  # Convert to (C, H, W)
        image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension

        return image_array.astype(np.float32)

    def __softmax(self, x: np.ndarray) -> np.ndarray:
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()
    

    def __call__(self, image_data: bytes):
        """
        Classify the image using SqueezeNet model.
            :param image_data: Image data in bytes.
            :return: Top 3 predictions with their probabilities.
        """
        # Preprocess the image
        preprocessed_image = self.__preprocess_image(image_data)

        # Run inference on the preprocessed image
        input_name = self.__session.get_inputs()[0].name
        output_name = self.__session.get_outputs()[0].name
        raw_predictions = self.__session.run([output_name], {input_name: preprocessed_image})[0] # [0]: Numpy Array

        # "Aplanamos" nuestro Array: (1, A) --> (A,) 
        predictions = raw_predictions.squeeze()

        #predictions = self.__softmax(predictions)

        # Extract the top 3 predictions
        top_indices = predictions.argsort()[-3:][::-1]
        top_probabilities = predictions[top_indices]

        return [{"label": self.class_names[int(idx)], "score": float(prob)} for idx, prob in zip(top_indices, top_probabilities)]

