import tkinter as tk
from PIL import Image, ImageColor, ImageTk
import argparse


def create_image(mode : int, size):
    size_field_x = int(size/32)
    size_field_y = int(size/128)
    image = Image.new("1", (size, size))
    cols = (ImageColor.getcolor("black", "1"), ImageColor.getcolor("white", "1"))
    sel = 0
    half = int(size/2)
    square_min = int(half/4)
    square_max = 3*square_min
    square_range = range(square_min, square_max)

    if mode == 1:
        """ Mode 1:
        - Only calculates top left quadrant
        - Calculates pixels of background pattern (excluding these in square area)
        - Calculates pixels of square area
        - Copies pixels of top left quadrant to all other quadrants
        """
        # ranges for less calculation in nested loops
        field_x_range = range(size_field_x)
        field_y_range = range(size_field_y)
        x_range = range(0, half, size_field_x)
        y_range = range(0, half, size_field_y)

        # Calculate background pixel of top left quadrant
        for y in y_range:
            for x in x_range:
                # Skips square in middle
                if x in square_range and y in square_range:
                    continue
                if x != 0:
                    sel = 1 if sel == 0 else 0
                for i in field_x_range:
                    for j in field_y_range:
                        image.putpixel((x + i, y + j), cols[sel])

        x_range = range(square_min, square_max, size_field_y)
        y_range = range(square_min, square_max, size_field_x)
        # Calculate pixel of square in middle of top left quadrant
        for y in y_range:
            for x in x_range:
                if x != square_min:
                    sel = 1 if sel == 0 else 0
                for i in field_y_range:
                    for j in field_x_range:
                        image.putpixel((x + i, y + j), cols[sel])

        x_range = range(half)
        # Copy to other three quadrants
        for i in x_range:
            for j in x_range:
                cur = image.getpixel((i, j))
                image.putpixel((i, j + half), cur)
                image.putpixel((i + half, j), cur)
                image.putpixel((i + half, j + half), cur)

    elif mode == 2:
        """ Mode 2:
        - Only calculates top left quadrant
        - Calculates all pixels in relation to their position
        - Copies pixels of top left quadrant to all other quadrants
        """
        double_x = 2*size_field_x
        double_y = 2*size_field_y
        r = range(half)

        for y in r:
            for x in r:
                if x in square_range and y in square_range:
                    # inner square
                    sel = 1 if ((y % double_x < size_field_x) ^ (x % double_y < size_field_y)) else 0
                else:
                    # outer field
                    sel = 1 if ((x % double_x < size_field_x) ^ (y % double_y < size_field_y)) else 0
                image.putpixel((x, y), cols[sel])

        # Copy to other three quadrants
        for i in r:
            for j in r:
                cur = image.getpixel((i, j))
                image.putpixel((i, j + half), cur)
                image.putpixel((i + half, j), cur)
                image.putpixel((i + half, j + half), cur)

    else:
        """ Mode 3:
        - Calculates all pixels in relation to their position
        """
        double_x = 2*size_field_x
        double_y = 2*size_field_y
        r = range(size)

        for y in r:
            for x in r:
                if x % half in square_range and y % half in square_range:
                    # inner square
                    sel = 1 if ((y % double_x < size_field_x) ^ (x % double_y < size_field_y)) else 0
                else:
                    # outer field
                    sel = 1 if ((x % double_x < size_field_x) ^ (y % double_y < size_field_y)) else 0
                image.putpixel((x, y), cols[sel])

    return image, size

def setup(img, size):
    root = tk.Tk()
    root.title("Ouchi Illusion")
    image = ImageTk.PhotoImage(img)
    canvas = tk.Canvas(root, width=size, height=size, bd=-2)
    canvas.pack()
    canvas.create_image(0,0, anchor="nw", image=image)
    canvas.image = image
    root.mainloop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ouchi Illusion")
    parser.add_argument("-e", "--exponent", action="store", type=int, nargs="?",
        default=9, help="exponent for the image size as power of two (min: 7) (default: 9)")
    parser.add_argument("-m", "--mode", action="store", type=int, nargs="?",
        default=2, help="type of processing mode (1, 2 or 3) (default: 2)")

    p = parser.parse_args()
    if p.mode not in [1, 2, 3]:
        parser.error("Mode has to be 1, 2 or 3")
    if p.exponent < 7:
        parser.error("Minimum exponent is 7")
        
    image, size = create_image(p.mode, 2 ** p.exponent)
    setup(image, size)