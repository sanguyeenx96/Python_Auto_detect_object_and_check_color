import cv2


# Open the camera
cap = cv2.VideoCapture(0)

# Capture a frame
ret, frame = cap.read()

# Save the frame as an image file
cv2.imwrite("test_cam1.jpg", frame)

# Release the camera
cap.release()

