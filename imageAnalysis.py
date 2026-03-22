from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

client = ImageAnalysisClient(
    endpoint="<YOUR_ENDPOINT>",
    credential=AzureKeyCredential("<YOUR_KEY>")
)

with open("image.jpg", "rb") as f:
    image_data = f.read()

result = client.analyze(
    image_data=image_data,
    visual_features=[VisualFeatures.CAPTION, VisualFeatures.TAGS],
    gender_neutral_caption=True,
)

if result.caption:
    print(f"Caption: {result.caption.text} (confidence: {result.caption.confidence:.2f})")

if result.tags:
    print("Tags:")
    for tag in result.tags.list:
        print(f"  - {tag.name} (confidence: {tag.confidence:.2f})")
