import cv2

# Haarcascade for number plate detection
haarcascade = "model\\haarcascade_russian_plate_number.xml"

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Set width
cap.set(4, 480)  # Set height
min_area = 500  # Minimum area for number plate detection
count = 0  # Counter for saved images

while True:
    success, img = cap.read()  # Read frames from the camera
    if not success:
        print("Failed to capture video")
        break

    plate_cascade = cv2.CascadeClassifier(haarcascade)  # Load the cascade classifier
    flip_img = cv2.flip(img, 1)  # Flip the image horizontally
    img_gray = cv2.cvtColor(flip_img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

    # Detect number plates
    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

    # Loop through detected plates
    for (x, y, w, h) in plates:
        area = w * h
        if area > min_area:
            # Draw rectangle around the detected number plate
            cv2.rectangle(flip_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(flip_img, "Number Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

            # Extract the region of interest (ROI)
            img_roi_flip = flip_img[y:y + h, x:x + w]
            img_roi = cv2.flip(img_roi_flip, 1)  # Flip the ROI back to original orientation
            cv2.imshow("ROI", img_roi)

    # Display instructions on the main window
    cv2.putText(flip_img, "Press 'S' to Save | 'Q' to Quit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Show the main window
    cv2.imshow('Result', flip_img)

    # Key event handling
    key = cv2.waitKey(1) & 0xFF
    if key == ord("s"):  # Save the detected plate
        if 'img_roi' in locals():  # Ensure ROI exists
            cv2.imwrite(f"plates/scanned_img_{count}.jpg", img_roi)
            print(f"Image saved: plates/scanned_img_{count}.jpg")
            count += 1
        else:
            print("No number plate detected to save.")

    if key == ord("q"):  # Quit the application
        print("Exiting...")
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
