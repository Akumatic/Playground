import tkinter as tk

class Color:
    def __init__(self,  hex = "#000000", red = 0, green = 0, blue = 0, hue = 0, sat = 0, val = 0):
        if hex == "#000000" and red == 0 and green == 0 and blue == 0 and hue == 0 and sat == 0 and val == 0:
            self.red = red
            self.green = green
            self.blue = blue
            self.hue = hue
            self.sat = sat
            self.val = val
            self.hex = hex
        elif hex != "#000000":
            self.updateHex(hex)
        elif red != 0 or green != 0 or blue != 0:
            self.updateRGB(red, green, blue)
        else:
            self.updateHsv(hue, sat, val)
        
    def __str__(self):
        return f"HEX: {self.hex}\nRGB: {self.red}, {self.green}, {self.blue}\n" \
            f"HSV: {self.hue}°, {self.sat}%, {self.val}%"

    def getHexRed(self):
        val = hex(self.red)[2:]
        return f"#{val if len(val) == 2 else f'0{val}'}0000"

    def getHexGreen(self):
        val = hex(self.green)[2:]
        return f"#00{val if len(val) == 2 else f'0{val}'}00"

    def getHexBlue(self):
        val = hex(self.blue)[2:]
        return f"#0000{val if len(val) == 2 else f'0{val}'}"

    def updateHex(self, hex):
        self.hex = hex
        rgb = self.hexToRgb(hex)
        hsv = self.rgbToHsv(rgb)
        self.red, self.green, self.blue = rgb[0], rgb[1], rgb[2]
        self.hue, self.sat, self.val = hsv[0], hsv[1], hsv[2]
    
    def updateRGB(self, red = None, green = None, blue = None):
        if red is not None:
            self.red = red       
        if green is not None:
            self.green = green       
        if blue is not None:
            self.blue = blue
        hsv = self.rgbToHsv((self.red, self.green, self.blue))
        self.hue, self.sat, self.val = hsv[0], hsv[1], hsv[2]
        self.hex = self.rgbToHex((self.red, self.green, self.blue))

    def updateHsv(self, hue = None, sat = None, val = None):
        if hue is not None:
            self.hue = hue       
        if sat is not None:
            self.sat = sat       
        if val is not None:
            self.val = val
        rgb = self.HsvToRgb((self.hue, self.sat, self.val))
        self.red, self.green, self.blue = rgb[0], rgb[1], rgb[2]
        self.hex = self.rgbToHex((rgb[0], rgb[1], rgb[2]))

    def hexToRgb(self, hex : str) -> tuple:
        hex = hex.split("#")[1]
        return (int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16))

    def rgbToHex(self, rgb : tuple) -> str:
        a = hex(rgb[0])[2:]
        b = hex(rgb[1])[2:]
        c = hex(rgb[2])[2:]

        return f"#{a if len(a) == 2 else f'0{a}'}" \
            f"{b if len(b) == 2 else f'0{b}'}" \
            f"{c if len(c) == 2 else f'0{c}'}"

    def rgbToHsv(self, rgb : tuple) -> tuple:
        red = rgb[0] / 255
        green = rgb[1] / 255
        blue = rgb[2] / 255

        color_max = max(red, green, blue)
        color_min = min(red, green, blue)
        color_delta = color_max - color_min

        if color_delta == 0:
            hue = 0
        elif color_max == red:
            hue = int(round(60 * (((green - blue) / color_delta) % 6), 0))
        elif color_max == green:
            hue = int(round(60 * ((blue - red) / color_delta + 2), 0))
        else:
            hue = int(round(60 * ((red - green) / color_delta + 4), 0))
        sat = 0 if color_max == 0 else int(round(color_delta/color_max * 100, 0))
        val = int(round(color_max * 100, 0))
        return (hue, sat, val)

    def HsvToRgb(self, hsv : tuple) -> tuple:
        hue = hsv[0] % 360
        sat = hsv[1] / 100
        val = hsv[2] / 100
        
        C = val * sat
        X = C * (1 - abs((hue / 60) % 2 - 1))

        if hue < 60:
            red, green, blue = C, X, 0
        elif hue < 120:
            red, green, blue = X, C, 0
        elif hue < 180:
            red, green, blue = 0, C, X
        elif hue < 240:
            red, green, blue = 0, X, C
        elif hue < 300:
            red, green, blue = X, 0, C
        else:
            red, green, blue = C, 0, X
        
        red = int(round((red + val - C) * 255, 0))
        green = int(round((green + val - C) * 255, 0))
        blue = int(round((blue + val - C) * 255, 0))
        return (red, green, blue)

class ColorSlider:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.color = Color()
        self.setup()

    def updateColor(self):
        self.changing = False
        self.hex.set(self.color.hex)
        self.red.set(self.color.red)
        self.green.set(self.color.green)
        self.blue.set(self.color.blue)
        self.hue.set(self.color.hue)
        self.sat.set(self.color.sat)
        self.val.set(self.color.val)

        self.red_slider.config(troughcolor=self.color.getHexRed())
        self.green_slider.config(troughcolor=self.color.getHexGreen())
        self.blue_slider.config(troughcolor=self.color.getHexBlue())

        self.preview_color.config(bg=self.color.hex)

    def updateHex(self, val):
        self.color.updateHex(hex=val)
        self.updateColor()

    def updateRedSlider(self, val):
        self.color.updateRGB(red=int(val))
        self.updateColor()

    def updateGreenSlider(self, val):
        self.color.updateRGB(green=int(val))
        self.updateColor()

    def updateBlueSlider(self, val):
        self.color.updateRGB(blue=int(val))
        self.updateColor()

    def updateHueSlider(self, val):
        self.color.updateHsv(hue=int(val))
        self.updateColor()

    def updateSatSlider(self, val):
        self.color.updateHsv(sat=int(val))
        self.updateColor()

    def updateValSlider(self, val):
        self.color.updateHsv(val=int(val))
        self.updateColor()

    def validate(self, val, min, max):
        try:
            i = int(val)
            return len(val) <= len(max) and not (i < int(min) or i > int(max))
        except ValueError:
            return False

    def setup(self):
        self.root.title("Color Slider")
        self.root.resizable(0,0)
        
        self.hex = tk.StringVar()
        self.red = tk.IntVar()
        self.green = tk.IntVar()
        self.blue = tk.IntVar()
        self.hue = tk.IntVar()
        self.sat = tk.IntVar()
        self.val = tk.IntVar()

        """ LabelFrames """
        left_frame = tk.Frame(self.root)
        preview_frame = tk.LabelFrame(left_frame, text="Color")
        hex_labelframe = tk.LabelFrame(left_frame, text="Hex")
        red_labelframe = tk.LabelFrame(self.root, text="Red")
        green_labelframe = tk.LabelFrame(self.root, text="Green")
        blue_labelframe = tk.LabelFrame(self.root, text="Blue")
        hue_labelframe = tk.LabelFrame(self.root, text="Hue")
        sat_labelframe = tk.LabelFrame(self.root, text="Sat")
        val_labelframe = tk.LabelFrame(self.root, text="Val")

        """ Placing down LabelFrames """ 
        left_frame.grid(column=0, rowspan=3)
        preview_frame.grid(column=0, row=1, rowspan=2)
        hex_labelframe.grid(column = 0, row=0)
        red_labelframe.grid(column=1, row=0)
        green_labelframe.grid(column=1, row=1)
        blue_labelframe.grid(column=1, row=2)
        hue_labelframe.grid(column=2, row=0)
        sat_labelframe.grid(column=2, row=1)
        val_labelframe.grid(column=2, row=2)

        # Verifying command
        validate = self.root.register(self.validate)

        """ Defining Entities """
        self.preview_color = tk.Frame(preview_frame, bg=self.color.hex, height=189, width=60)
        # Red 
        self.red_box = tk.Entry(red_labelframe, textvariable=self.red, width=5, justify="center")
        self.red_box.configure(state="readonly", validate="all", vcmd=(validate, "%P", "0", "255"))
        red_info = tk.Label(red_labelframe, text="[0, 255]")
        self.red_slider = tk.Scale(red_labelframe, from_=0, to=255, orient=tk.HORIZONTAL)
        self.red_slider.configure(variable = self.red, command=self.updateRedSlider)
        # Green
        self.green_box = tk.Entry(green_labelframe, textvariable=self.green, width=5, justify="center")
        self.green_box.configure(state="readonly", validate="all", vcmd=(validate, "%P", "0", "255"))
        green_info = tk.Label(green_labelframe, text="[0, 255]")
        self.green_slider = tk.Scale(green_labelframe, from_=0, to=255, orient=tk.HORIZONTAL)
        self.green_slider.configure(variable = self.green, command=self.updateGreenSlider)
        # Blue
        self.blue_box = tk.Entry(blue_labelframe, textvariable=self.blue, width=5, justify="center")
        self.blue_box.configure(state="readonly", validate="all", vcmd=(validate, "%P", "0", "255"))
        blue_info = tk.Label(blue_labelframe, text="[0, 255]")
        self.blue_slider = tk.Scale(blue_labelframe, from_=0, to=255, orient=tk.HORIZONTAL)
        self.blue_slider.configure(variable = self.blue, command=self.updateBlueSlider)
        # Hue
        self.hue_box = tk.Entry(hue_labelframe, textvariable=self.hue, width=5, justify="center")
        self.hue_box.configure(state="readonly", validate="all", vcmd=(validate, "%P", "0", "359"))
        hue_info = tk.Label(hue_labelframe, text="° [0, 359]")
        self.hue_slider = tk.Scale(hue_labelframe, from_=0, to=359, orient=tk.HORIZONTAL) 
        self.hue_slider.configure(variable = self.hue, command=self.updateHueSlider)
        # Sat
        self.sat_box = tk.Entry(sat_labelframe, textvariable=self.sat, width=5, justify="center")
        self.sat_box.configure(state="readonly", validate="all", vcmd=(validate, "%P", "0", "100"))
        sat_info = tk.Label(sat_labelframe, text="% [0, 100]")
        self.sat_slider = tk.Scale(sat_labelframe, from_=0, to=100, orient=tk.HORIZONTAL)
        self.sat_slider.configure(variable = self.sat, command=self.updateSatSlider)
        # Val
        self.val_box = tk.Entry(val_labelframe, textvariable=self.val, width=5, justify="center")
        self.val_box.configure(state="readonly", validate="all", vcmd=(validate, "%P", "0", "100"))
        val_info = tk.Label(val_labelframe, text="% [0, 100]")
        self.val_slider = tk.Scale(val_labelframe, from_=0, to=100, orient=tk.HORIZONTAL) 
        self.val_slider.configure(variable = self.val, command=self.updateValSlider)
        # Hex
        self.hex_box = tk.Entry(hex_labelframe, textvariable=self.hex, width=9, justify="center", state="readonly")

        """ Placing down Entities """
        self.preview_color.grid()
        # Input Text Boxes
        self.hex_box.grid()
        self.red_box.grid(row=0, column=0)
        red_info.grid(row=0, column=1)
        self.green_box.grid(row=0, column=0)
        green_info.grid(row=0, column=1)
        self.blue_box.grid(row=0, column=0)
        blue_info.grid(row=0, column=1)
        self.hue_box.grid(row=0, column=0)
        hue_info.grid(row=0, column=1)
        self.sat_box.grid(row=0, column=0)
        sat_info.grid(row=0, column=1)
        self.val_box.grid(row=0, column=0)
        val_info.grid(row=0, column=1)
        # Color Sliders
        self.red_slider.grid(row=1, columnspan=2)
        self.green_slider.grid(row=1, columnspan=2)
        self.blue_slider.grid(row=1, columnspan=2)
        self.hue_slider.grid(row=1, columnspan=2)
        self.sat_slider.grid(row=1, columnspan=2)
        self.val_slider.grid(row=1, columnspan=2)

        """ Updating Colors """
        self.updateColor()

def main():
    root = tk.Tk()
    ColorSlider(root)
    root.mainloop()

if __name__ == "__main__":
    main()