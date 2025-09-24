import cv2
import os
import numpy as np
from detector import detect_components # Ensure this file is present

def process_train_video(input_video_path, output_base_dir, train_number):
    """
    Splits a train video, counts coaches, extracts frames, and detects components.
    
    Returns:
        int: The total number of coaches detected.
    """
    if not os.path.exists(input_video_path):
        print(f"Error: The video file '{input_video_path}' was not found.")
        return 0
        
    if not os.path.exists(output_base_dir):
        os.makedirs(output_base_dir)

    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return 0

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    change_threshold = 20000000 # Adjust this value as needed for your video

    coach_count = 0
    coach_frames = []
    last_frame_gray = None
    
    print("Processing video...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if last_frame_gray is not None:
            frame_diff = cv2.absdiff(current_frame_gray, last_frame_gray)
            diff_sum = np.sum(frame_diff)
            
            if diff_sum > change_threshold:
                if coach_frames:
                    coach_count += 1
                    coach_folder = os.path.join(output_base_dir, f"{train_number}_{coach_count}")
                    os.makedirs(coach_folder, exist_ok=True)
                    
                    coach_output_path = os.path.join(coach_folder, f"{train_number}_{coach_count}.mp4")
                    out = cv2.VideoWriter(coach_output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))
                    
                    for f in coach_frames:
                        out.write(f)
                    out.release()
                    print(f"Saved video for Coach {coach_count}")
                    
                    # Extract and save frames
                    extract_frames(coach_output_path, coach_folder, train_number, coach_count)
                    
                    coach_frames = []

        coach_frames.append(frame)
        last_frame_gray = current_frame_gray

    if coach_frames:
        coach_count += 1
        coach_folder = os.path.join(output_base_dir, f"{train_number}_{coach_count}")
        os.makedirs(coach_folder, exist_ok=True)
        
        coach_output_path = os.path.join(coach_folder, f"{train_number}_{coach_count}.mp4")
        out = cv2.VideoWriter(coach_output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))
        
        for f in coach_frames:
            out.write(f)
        out.release()
        print(f"Saved video for Coach {coach_count}")
        
        extract_frames(coach_output_path, coach_folder, train_number, coach_count)

    cap.release()
    print("\nVideo processing and frame extraction complete.")
    print(f"Total number of coaches detected: {coach_count}")
    return coach_count

def extract_frames(video_path, output_folder, train_number, coach_count, frames_to_skip=20):
    """
    Extracts frames from a video and detects components.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video for frame extraction: {video_path}")
        return

    frame_count = 0
    saved_frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % frames_to_skip == 0:
            saved_frame_count += 1
            original_frame_filename = f"{train_number}_{coach_count}_{saved_frame_count}_original.jpg"
            annotated_frame_filename = f"{train_number}_{coach_count}_{saved_frame_count}.jpg"
            
            original_frame_path = os.path.join(output_folder, original_frame_filename)
            annotated_frame_path = os.path.join(output_folder, annotated_frame_filename)
            
            cv2.imwrite(original_frame_path, frame)
            
            annotated_img, detections = detect_components(original_frame_path)
            
            if annotated_img is not None:
                cv2.imwrite(annotated_frame_path, annotated_img)

        frame_count += 1
        
    cap.release()
    print(f"Extracted and annotated {saved_frame_count} frames from {os.path.basename(video_path)}")