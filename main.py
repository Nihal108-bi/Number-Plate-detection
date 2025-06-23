import cv2
import os
import time
import numpy as np

# --- Configuration ---
# Choose your source (uncomment the one you want to use)
# source = 0  # Webcam
source = 'videos/multicars.mp4'  # Local video file
# source = 'http://<ip_address>:<port>/video'  # IP Camera or streaming URL

cascade_path = "model/haarcascade_russian_plate_number.xml"
output_folder = "plates"
os.makedirs(output_folder, exist_ok=True)

# Load cascade classifier
plate_cascade = cv2.CascadeClassifier(cascade_path)
if plate_cascade.empty():
    print("Error loading cascade classifier!")
    exit()

# Initialize video capture
cap = cv2.VideoCapture(source)
if not cap.isOpened():
    print("Error opening video source!")
    exit()

# Set resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Parameters
min_area = 500
save_delay = 1.5  # Seconds between saves of same plate
frame_skip = 2    # Process every Nth frame
recent_plates = [] # Stores recent plate positions and timestamps
count = 0
last_time = time.time()
fps = 0

# For performance tracking
frame_count = 0
start_time = time.time()

while True:
    success, frame = cap.read()
    if not success:
        print("End of video or can't read frame.")
        break
    
    frame_count += 1
    if frame_count % frame_skip != 0:
        continue  # Skip frames to improve performance

    # Preprocessing for better detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)  # Improve contrast
    gray = cv2.GaussianBlur(gray, (5, 5), 0)  # Reduce noise
    
    # Detect number plates with optimized parameters
    plates = plate_cascade.detectMultiScale(
        gray, 
        scaleFactor=1.05, 
        minNeighbors=3,
        minSize=(60, 20),
        maxSize=(300, 100)
    )
    
    current_time = time.time()
    
    # Process detected plates
    for (x, y, w, h) in plates:
        area = w * h
        if area > min_area:
            center = (x + w//2, y + h//2)
            
            # Check if plate is similar to recent detections
            is_duplicate = False
            for plate in recent_plates:
                dist = np.sqrt((center[0]-plate[0])**2 + (center[1]-plate[1])**2)
                time_diff = current_time - plate[2]
                
                # Consider duplicate if close position and recent detection
                if dist < 50 and time_diff < save_delay:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                # Extract and save plate
                plate_img = frame[y:y+h, x:x+w]
                filename = f"{output_folder}/plate_{int(time.time())}_{count}.jpg"
                cv2.imwrite(filename, plate_img)
                print(f"✅ Saved: {filename}")
                count += 1
                
                # Remember this plate
                recent_plates.append((center[0], center[1], current_time))
            
            # Draw bounding box
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"Plate {count}", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Cleanup old plate records
    recent_plates = [p for p in recent_plates if current_time - p[2] < save_delay * 2]
    
    # Calculate and display FPS
    fps = frame_count / (time.time() - start_time)
    cv2.putText(frame, f"FPS: {fps:.1f} | Plates: {count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    
    # Display frame
    cv2.imshow("Number Plate Detection", frame)
    
    # Exit on 'q' press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
print(f"Processed {frame_count} frames at {fps:.1f} FPS")