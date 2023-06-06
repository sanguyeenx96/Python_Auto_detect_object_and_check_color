import cv2

index = 0
total = 0

while True:
    cap = cv2.VideoCapture(index)
    print(index)
    if not cap.read()[0]:
        break
    total += 1
    index += 1

print("Total cameras:", total)