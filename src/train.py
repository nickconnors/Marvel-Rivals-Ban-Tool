from ultralytics import YOLO
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
model_path = os.path.join(project_root, 'models', 'yolo11l.pt')
yaml_path = os.path.join(project_root, 'dataset_custom.yaml')
runs_path = os.path.join(project_root, 'runs')

model = YOLO(model_path)
model.train(data=yaml_path, imgsz=640, batch=8, epochs=100, workers=0, device=0, project=runs_path)