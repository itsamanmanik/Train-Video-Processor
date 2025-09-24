from video_processor import process_train_video
from report_generator import generate_report
import os

if __name__ == "__main__":
    # --- Project Configuration ---
    INPUT_VIDEO_PATH = "raw_video.mp4" 
    TRAIN_NUMBER = "12309"
    OUTPUT_BASE_DIR = "Processed_Video"
    REPORT_FILENAME = "Final Report.pdf"
    
    print("Step 1: Running video processor to split video and extract frames...")
    # Execute the video processing and capture the returned coach count
    total_coaches = process_train_video(INPUT_VIDEO_PATH, OUTPUT_BASE_DIR, TRAIN_NUMBER)
    
    if total_coaches > 0:
        print("\nStep 2: Generating the final PDF report...")
        # Pass the dynamic coach count to the report generator
        generate_report(REPORT_FILENAME, TRAIN_NUMBER, total_coaches, OUTPUT_BASE_DIR)
        print("\nProcess completed successfully! ✨")
    else:
        print("\nNo coaches were detected. Skipping report generation.")