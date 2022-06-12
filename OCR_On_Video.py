import cv2
import pytesseract
import os


pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract"
folder_Path = "Screenshot Images"
count = 0


def file_Manager():
    """
    to create a folder for storing the screenshots, if necessary,
    or remove the existing contents of the concerned folder, if any.
    """
    try:
        if not os.path.exists(folder_Path):
            os.makedirs(folder_Path)
        else:
            all_Content = os.listdir(folder_Path)
            if len(all_Content) != 0:
                for content in all_Content:
                    path = os.path.join(folder_Path, content)
                    if os.path.exists(path): os.remove(path)
    except OSError: pass


def store_SS(img):
    """
    to store the screenshots in the concerned folder and send them for pre-processing
    :param img: a numpy array
    """
    global count
    count += 1
    print("Taking screenshot...")
    path = os.path.join(folder_Path, f"Screenshot_{str(count)}.png")
    cv2.imwrite(path, img)
    pre_Processing(path)


def pre_Processing(path):
    """
    to pre-process all the screenshots taken and stored in the folder,
    and send them to another function in order to extract text from them
    :param: path of the current screenshot stored
    """
    img = cv2.imread(path)
    height, width, _ = img.shape
    # for eliminating the headers and footers
    img_Cropped = img[40:height - 40, 0:width]
    image_To_Text(img_Cropped)


def image_To_Text(img):
    """
    to extract the text from the screenshots taken, and paste all the text in a text file
    :param img: a numpy array
    """
    str = pytesseract.image_to_string(img)
    print("Text extracted...\n")
    with open("Screenshot Images\\Full_Text.txt", "a+", encoding='utf-8') as file:
        file.write(str)
        file.write(f"\n\n------------------ PAGE {count} ----------------------\n\n")


def main():
    """
    the main function which would be executed in the beginning
    """
    try:
        file_Manager()

        wCam, hCam = 640, 480
        cap = cv2.VideoCapture("Digital Image Processing.mp4")
        cap.set(3, wCam)
        cap.set(4, hCam)

        while True:
            success, img = cap.read()
            if success:
                cv2.imshow("Lecture Video", img)
                if cv2.waitKey(1) & 0xFF == 32: store_SS(img)
            if cv2.waitKey(1) & 0xFF == ord('q'): break
        cap.release()
        cv2.destroyAllWindows()

    except Exception:
        print("Sorry! An exception has been encountered. Exiting application...")
        exit()


if __name__ == "__main__": main()