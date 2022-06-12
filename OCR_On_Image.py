import cv2
import pytesseract
from pyautogui import screenshot
from tkinter.filedialog import *
import os


pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract"
folder_Path = "Screenshot Images"
count = 0


def file_Manager():
    """
    to store the screenshots taken, in a folder, or create the folder if necessary,
    or remove the existing contents of the folder, if any.
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
    except OSError:
        pass


def take_Screenshot():
    """
    to take screenshot of the current screen
    """
    global count
    count += 1
    print("Taking screenshot...")
    ss = screenshot()
    path = os.path.join(folder_Path, f"Screenshot_{str(count)}.png")
    ss.save(path)
    pre_Processing(path)


def pre_Processing(path):
    """
    to pre-process each screenshot taken
    :param path: path where the screenshot has been stored
    """
    img = cv2.imread(path)
    height, width, _ = img.shape
    # for eliminating the headers and footers
    img_Cropped = img[40:height - 50, 0:width]
    image_To_Text(img_Cropped)


def image_To_Text(img):
    """
    to extract the text from the screenshot and store it in a text file
    :param img: a numpy array
    """
    str = pytesseract.image_to_string(img)
    with open("Screenshot Images\\Full_Text.txt", "a+", encoding='utf-8') as file:
        file.write(str)
        file.write(f"\n\n--------------------- PAGE {count} ------------------------- \n\n")


def main():
    """
    the main function which would be executed in the beginning
    """
    file_Manager()
    root = Tk()
    window = Canvas(root, width=100, height=100)
    window.pack()
    ss_Button = Button(text="Take ss", command=take_Screenshot, font=10)
    window.create_window(50, 50, window=ss_Button)
    root.mainloop()


if __name__ == "__main__": main()

'''
img_Gray = cv2.imread(path, 0)
    height, width = img_Gray.shape
    # for eliminating the headers and footers
    img_Cropped = img_Gray[40:height - 50, 0:width]
    img_Blur = cv2.GaussianBlur(img_Cropped, (3,3), 0)
    img_Thresh = cv2.threshold(img_Blur, 127, 256, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.imshow("Binary image", img_Thresh)
    image_To_Text(img_Thresh)
'''