from azure.ai.vision.face import FaceClient
from azure.ai.vision.face.models import (
    FaceAttributeTypeDetection01,
    FaceDetectionModel,
    FaceRecognitionModel,
)
from azure.core.credentials import AzureKeyCredential

face_client = FaceClient(
    endpoint="<YOUR_ENDPOINT>",
    credential=AzureKeyCredential("<YOUR_KEY>")
)

features = [
    FaceAttributeTypeDetection01.HEAD_POSE, # example: slight upward tilt (pitch 3.8°), nearly straight (roll 0.3°, yaw -1.3°)  
    FaceAttributeTypeDetection01.OCCLUSION, # nothing blocking the forehead, eyes, or mouth
    FaceAttributeTypeDetection01.ACCESSORIES, # stuff like face mask, glasses, helmet
]

with open("face3.jpg", mode="rb") as image_data:
    detected_faces = face_client.detect(
        image_content=image_data.read(),
        # detection_model options:
        # DETECTION01 - General use, good balance
        # DETECTION02 - Better accuracy, but no face attributes (no head pose, occlusion etc.)
        # DETECTION03 - Best for small/blurry faces and faces at angles
        detection_model=FaceDetectionModel.DETECTION01,
        # recognition_model options:
        # RECOGNITION01 - Oldest, basic accuracy
        # RECOGNITION02 - Improved accuracy
        # RECOGNITION03 - Better than 02
        # RECOGNITION04 - Latest, most accurate (recommended)
        recognition_model=FaceRecognitionModel.RECOGNITION04,
        # face identification requires special Microsoft approval due to privacy concerns
        # we're only using it to detect face attributes like head pose and occlusion
        return_face_id=False,
        return_face_attributes=features,
    )

    

print(f"Detected {len(detected_faces)} face(s).")

for i, face in enumerate(detected_faces):
    print(f"\nFace {i + 1}:")
    print(f"  Face ID: {face.face_id}")

    if face.face_attributes:
        attrs = face.face_attributes

        if attrs.head_pose:
            print(f"  Head Pose:")
            print(f"    Pitch: {attrs.head_pose.pitch:.1f}")
            print(f"    Roll:  {attrs.head_pose.roll:.1f}")
            print(f"    Yaw:   {attrs.head_pose.yaw:.1f}")

        if attrs.occlusion:
            print(f"  Occlusion:")
            print(f"    Forehead: {attrs.occlusion.forehead_occluded}")
            print(f"    Eyes:     {attrs.occlusion.eye_occluded}")
            print(f"    Mouth:    {attrs.occlusion.mouth_occluded}")

        if attrs.accessories:
            if attrs.accessories:
                print(f"  Accessories: {[a.type for a in attrs.accessories]}")
            else:
                print(f"  Accessories: None")
