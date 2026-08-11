import cv2

# Load the inspection image
image = cv2.imread("sample_part.jpg")

if image is None:
    print("Error: Could not load the image.")
    exit()

# 1. Convert image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 2. Apply Gaussian Blur
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# 3. Apply thresholding
_, threshold = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)

# 4. Find contours
contours, _ = cv2.findContours(
    threshold,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

# Defect detection criteria
minimum_defect_area = 500
defects = []

for contour in contours:
    area = cv2.contourArea(contour)

    if area > minimum_defect_area:
        x, y, w, h = cv2.boundingRect(contour)
        defects.append((x, y, w, h))

        # Draw bounding box around detected defect
        cv2.rectangle(
            image,
            (x, y),
            (x + w, y + h),
            (0, 0, 255),
            2
        )

# PASS/FAIL decision
if len(defects) == 0:
    result = "PASS"
else:
    result = "FAIL"

print("Inspection Result:", result)
print("Defects Detected:", len(defects))

# Display result
cv2.putText(
    image,
    result,
    (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 255, 0) if result == "PASS" else (0, 0, 255),
    2
)

cv2.imshow("Automated Quality Inspection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
