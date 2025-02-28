from ultralytics import YOLO
import cv2
import pytesseract
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
model_path = os.path.join(project_root, 'models', 'best.pt')

def get_players(file_path):
    model = YOLO(model_path)

    results = model(file_path)

    image_raw = cv2.imread(file_path)
    gray = cv2.cvtColor(image_raw, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)[1]

    detections = results[0].boxes.xyxy
    class_ids = results[0].boxes.cls

    right_players = []

    for i, box in enumerate(detections):
        if class_ids[i] == 1:
            x1, y1, x2, y2 = map(int, box)
            cropped_player = image[y1:y2, x1:x2]
            right_players.append(cropped_player)

    # for debugging
    # for i, crop in enumerate(right_players):
    #     cv2.imshow(f"Right Player {i+1}", crop)  # Show the cropped player image
    #     cv2.waitKey(0)  # Wait for a key press before showing the next one
    #     cv2.destroyAllWindows()  # Close the window after key press

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    extracted_players = []

    custom_config = r"--oem 3 --psm 6 -l eng"
    for i, crop in enumerate(right_players):
        text = pytesseract.image_to_string(crop, config=custom_config)
        player = text.strip()
        extracted_players.append(player)
        # print(f"Detected Right Player {i+1}: {player}")

    return extracted_players