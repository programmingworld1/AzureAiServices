from msrest.authentication import ApiKeyCredentials
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

# Authenticate a client for the prediction API
credentials = ApiKeyCredentials(in_headers={"Prediction-key": ""})
prediction_client = CustomVisionPredictionClient(endpoint="https://324345435345customvision.cognitiveservices.azure.com/",
                                                 credentials=credentials)

# Get classification predictions for an image
image_file = "image.jpg"
image_data = open(image_file, "rb").read()
results = prediction_client.classify_image("mytest1",
                                           "<YOUR_PUBLISHED_MODEL_NAME>",
                                           image_data)

# Process predictions
for prediction in results.predictions:
    if prediction.probability > 0.5:
        print(image_file + ': {} ({:.0%})'.format(prediction.tag_name, prediction.probability))
