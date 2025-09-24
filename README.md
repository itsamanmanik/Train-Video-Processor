# Train Video Processing and Analysis

## Project Overview
This project processes a raw video of a train from a side view to perform the following tasks:
1.  **Video Splitting:** Splits the full video into smaller segments, one for each train coach.
2.  **Coach Counting:** Counts the total number of coaches detected in the video.
3.  **Frame Extraction:** Extracts a minimal set of frames from each coach's video segment to ensure full visual coverage.
4.  **Component Detection:** Utilizes an object detection model (YOLOv8) to identify and annotate key components on each coach, such as doors.
5.  **Report Generation:** Compiles a final PDF report summarizing the analysis and providing annotated images for each coach.

## Files and Directory Structure
-   `raw_video.mp4`: The input video file.
-   `main.py`: The primary script that orchestrates the entire workflow.
-   `video_processor.py`: Contains the core logic for video splitting, frame extraction, and component detection.
-   `detector.py`: A utility file containing the object detection model.
-   `report_generator.py`: Script to compile the final PDF report.
-   `Processed_Video/`: The output directory, structured as follows:
    -   `12309_1/`
        -   `12309_1.mp4`
        -   `12309_1_1.jpg` (Annotated image)
    -   `12309_2/`
    -   ...
-   `Final Report.pdf`: The generated PDF report.

## How to Set Up and Run the Project
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/itsamanmanik/Train-Video-Processor.git
    cd <Your-Repo-Name>
    ```
2.  **Place the input video:**
    -   Download the `raw_video.mp4` file and place it in the project's root directory.
3.  **Install dependencies:**
    -   Ensure you have Python installed. Then, install the required libraries using pip:
    ```bash
    pip install opencv-python numpy ultralytics reportlab
    ```
4.  **Run the entire pipeline:**
    -   Execute the `main.py` script. This single command will run the entire process, from video processing to report generation.
    ```bash
    python main.py
    ```

## Key Features Implemented
-   **Modular Code:** The project is broken down into logical files (`main.py`, `video_processor.py`, `detector.py`, `report_generator.py`) for clarity and maintainability.
-   **Structured Output:** All processed files are organized into a logical folder structure as requested.
-   **Automated Reporting:** A comprehensive PDF report is automatically generated, including a summary and visual evidence for each coach.

## Limitations and Assumptions
-   **Object Detection:** The pre-trained YOLO model is used for a generic object detection task. While it may identify some features on the train, it is not specifically trained to detect "doors" or distinguish between "open" and "closed" doors. Fine-tuning would be required for higher accuracy on these specific components.
-   **Coach Detection Logic:** The change detection logic relies on a pixel difference threshold. This value may need to be adjusted based on the specific video to accurately detect gaps between coaches.
-   **Input Video:** It is assumed that the input video shows a single train moving from one end to the other without significant camera movement or occlusion.
