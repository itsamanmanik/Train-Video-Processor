from ultralytics import YOLO
import cv2

# Load a pre-trained YOLO model
# You can choose 'yolov8n.pt' (nano) for speed or a larger model for better accuracy.
model = YOLO('yolov8n.pt')

def detect_components(image_path):
    """
    Performs object detection on an image and returns the annotated image and detections.
    
    Args:
        image_path (str): The path to the image file.
        
    Returns:
        tuple: (annotated_image, detections_list)
    """
    try:
        results = model(image_path)
        
        # Get the first result object (assuming one image is processed at a time)
        result = results[0]
        
        # The annotated image with bounding boxes
        annotated_image = result.plot()
        
        # Process detections
        detections = []
        for box in result.boxes:
            x1, y1, x2, y2 = [int(coord) for coord in box.xyxy[0]]
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            
            detections.append({
                'class_name': class_name,
                'confidence': confidence,
                'bbox': [x1, y1, x2, y2]
            })
            
        return annotated_image, detections
        
    except Exception as e:
        print(f"Error during detection on {image_path}: {e}")
        return None, []

if __name__ == '__main__':
    # This is a test block for the detector
    # Replace with the path to one of your extracted frames
    test_image_path = "path/to/your/image.jpg"
    
    annotated_img, detections = detect_components(test_image_path)
    if annotated_img is not None:
        cv2.imshow("Detected Components", annotated_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print("Detections:")
        for det in detections:
            print(f"- Class: {det['class_name']}, Confidence: {det['confidence']:.2f}")