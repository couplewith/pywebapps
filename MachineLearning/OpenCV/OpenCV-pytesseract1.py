import cv2
import pytesseract

# 저장한 이미지를 불러와서
image = cv2.imread("pytesseract1.png")

# Display the image
cv2.imshow("Image", image)

# Wait for the user to press a key
cv2.waitKey(0)

# 글씨가 있는 좌표만 짤라서 다시 target.png로 저장함
#Image = image[0:0, 20:500]
# image_tmp = cv2.imread("pytesseract1.png")
# cv2.imwrite("target.png", image_tmp)
#
# # Display the image
# cv2.imshow("Image2", image_tmp)

# 저장한 이미지를 다시 불러옴
image2 = cv2.imread("sample/target1.png")
cv2.imshow("Image2", image2)
# Wait for the user to press a key
cv2.waitKey(0)

pytesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# 해당 이미지에 있는 글씨(문자)를 pytersseract를 이용하여 추출함
pytesseract.pytesseract.tesseract_cmd = pytesseract_cmd
text = pytesseract.image_to_string(image2)

print("pytersseract -> ", text)


# ---------------------------------------------
# https://github.com/UB-Mannheim/tesseract/wiki
# * The latest installer can be downloaded here:
# https://github.com/tesseract-ocr/tessdoc
# tesseract-ocr-w64-setup-5.3.1.20230401.exe (64 bit)
#
# ---------------------------------------------
# * https://github.com/UB-Mannheim/tesseract/wiki/Install-additional-language-and-script-models
#
# Choose the additional language and script models from e.g. one of the places linked from https://github.com/tesseract-ocr/tesseract/wiki/Data-Files .
# Download the traineddata file to the tessdata folder of tesseract on your PC, e.g. C:\Program Files\Tesseract-OCR\tessdata. It is also possible to create new subfolders within that folder to distinguish for example the best and fast models.
# tesseract --list-langs