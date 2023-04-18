import cv2
import numpy as np
import pandas as pd


# Reading the image with OpenCV
img = cv2.imread(r"C:\Users\hp\Downloads\43362 (1).jpg")
img = cv2.resize(img, (800, 600))
# Declaring global variables
clicked = False
r = g = b = xpos = ypos = 0

# Reading CSV file with pandas and giving names to each column
columns = ["color", "color_name", "hex", "r", "g", "b"]
csv = pd.read_csv(r"C:\Users\hp\Downloads\python-project-color-detection\colors.csv", names=columns, header=None)


def get_color_name(r, g, b):
    """
    Function to calculate minimum distance from all colors and get the most matching color
    """
    minimum = 10000
    for i in range(len(csv)):
        d = abs(r - int(csv.loc[i, "r"])) + abs(g - int(csv.loc[i, "g"])) + abs(b - int(csv.loc[i, "b"]))
        if d <= minimum:
            minimum = d
            color_name = csv.loc[i, "color_name"]
    return color_name


def draw_function(event, x, y, flags, param):
    """
    Function to get x,y coordinates of mouse double click
    """
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        xpos, ypos = x, y
        b, g, r = img[y, x]


cv2.namedWindow("image")
cv2.setMouseCallback("image", draw_function)

while True:
    cv2.imshow("image", img)

    if clicked:
        # Creating a rectangle to show the color in the GUI
        cv2.rectangle(img, (20,20), (750,60), (int(b), int(g), int(r)), -1)

        # Creating text string to display (color name and RGB values)
        color_name = get_color_name(r, g, b)
        text = f"{color_name} R={r} G={g} B={b}"

        # If the color is light, we display the text in black color
        font_color = (0, 0, 0) if r + g + b >= 600 else (255, 255, 255)
        cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, font_color, 2, cv2.LINE_AA)

        clicked = False

    # Break the loop when the user hits 'esc' key
    if cv2.waitKey(20) == 27:
        break

cv2.destroyAllWindows()
