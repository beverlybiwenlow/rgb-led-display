# -*- coding: utf-8 -*-
#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import fileinput


class RunText(SampleBase):
    
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
  
  
    def run(self):
        font_size_word = "7x13"
        font_size_num = "9x15B"
        font_size_small = "6x10"
        
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font_keys = graphics.Font()
        font_keys.LoadFont("../../../fonts/" + font_size_word + ".bdf")
        font_values = graphics.Font()
        
        font_small = graphics.Font()
        font_small.LoadFont("../../../fonts/" + font_size_small + ".bdf")
        textColor_keys = graphics.Color(255, 255, 255)
        textColor_values = graphics.Color(110, 255, 255)
        x_pos_keys = 2
        x_pos_values = offscreen_canvas.width
                                                        
        while True:
            with open("data-files/data-keys.txt", 'r') as f:
                keys_text = f.readline()
##                keys_text = f.readlines()
           
            with open("data-files/data-values.txt", 'r') as f:
                values_text = f.readline()
##                values_text = f.readlines()
            
##            for key in keys_text:
##                key = key.replace("\n", "")
##            for value in values_text:
##                value = value.replace("\n", "")
            keys_text = keys_text.replace("\n", "")            
            values_text = values_text.replace("\n", "")
            
            font_values.LoadFont("../../../fonts/" + font_size_num + ".bdf")
            
            # Data LEDs
            offscreen_canvas.Clear()
            len_values = graphics.DrawText(offscreen_canvas, font_values, x_pos_values, 0, textColor_values, values_text)
            offscreen_canvas.Clear()
            x_pos_values = offscreen_canvas.width - 1 - len_values

            # light up keys, values and borders
            len_keys = self.light_keys(offscreen_canvas, keys_text, font_keys, font_small, x_pos_keys, textColor_keys)
            len_values = graphics.DrawText(offscreen_canvas, font_values, x_pos_values, 13, textColor_values, values_text)
            self.light_borders(offscreen_canvas)
            
            
            # if number becomes too big
            values_boundary = x_pos_keys + len_keys
            if len_values + values_boundary >= offscreen_canvas.width:
                
                # DECREASE FONT SIZE
                fonts = ['8x13B','7x13B', '6x13', '6x12', '6x10', '6x9']
                for font in fonts:
##                    font_changed = graphics.Font()
                    font_values.LoadFont("../../../fonts/" + font + ".bdf")
                    offscreen_canvas.Clear()
                    len_values = graphics.DrawText(offscreen_canvas, font_values, 0, 0, textColor_values, values_text)
                    if len_values + values_boundary < offscreen_canvas.width:
                        x_pos_values = offscreen_canvas.width - 1 - len_values
                        len_values = graphics.DrawText(offscreen_canvas, font_values, x_pos_values, 13, textColor_values, values_text)
                        self.light_borders(offscreen_canvas)
                        len_keys = self.light_keys(offscreen_canvas, keys_text, font_keys, font_small, x_pos_keys, textColor_keys)
                        break
                    else:
                        # if smallest font is still too big, split number into 2 rows
                        if font == fonts[-1]:
                            num = len(values_text) / 2
                            values_array = []
                            values_array.append(values_text[:num])
                            values_array.append(values_text.replace(values_array[0], ''))
                            height1 = offscreen_canvas.height / 2
                            height2 = offscreen_canvas.height -1
                            offscreen_canvas.Clear()
                            len_values1 = graphics.DrawText(offscreen_canvas, font_small, 0, 0, textColor_values, values_array[0])
                            len_values2 = graphics.DrawText(offscreen_canvas, font_small, 0, 0, textColor_values, values_array[1])
                            if len_values1 > len_values2:
                                max_len_values = len_values1
                            else:
                                max_len_values = len_values2
                            new_x_pos_values = offscreen_canvas.width - 6 - max_len_values
                            len_values1 = graphics.DrawText(offscreen_canvas, font_small, new_x_pos_values, height1, textColor_values, values_array[0])
                            len_values2 = graphics.DrawText(offscreen_canvas, font_small, new_x_pos_values, height2, textColor_values, values_array[1])
                            self.light_borders(offscreen_canvas)
                            len_keys = self.light_keys(offscreen_canvas, keys_text, font_keys, font_small, x_pos_keys, textColor_keys)
                            break

                
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            time.sleep(0.05)

    def light_keys(self, offscreen_canvas, keys_text, font_keys, font_small, x_pos_keys, textColor_keys):
        if " " in keys_text:
            keys_text = keys_text.split()
            height1 = offscreen_canvas.height / 2
            height2 = offscreen_canvas.height -1
            len_keys1 = graphics.DrawText(offscreen_canvas, font_small, x_pos_keys, height1, textColor_keys, keys_text[0])
            len_keys2 = graphics.DrawText(offscreen_canvas, font_small, x_pos_keys, height2, textColor_keys, keys_text[1])
            if len_keys1 > len_keys2:
                len_keys = len_keys1
            else:
                len_keys = len_keys2
        else: 
            len_keys = graphics.DrawText(offscreen_canvas, font_keys, x_pos_keys, 13, textColor_keys, keys_text)
        return len_keys

    def light_borders(self, offscreen_canvas):
        for x in range(0, offscreen_canvas.width):
            offscreen_canvas.SetPixel(x, 0, 47, 86, 233)
            offscreen_canvas.SetPixel(x, offscreen_canvas.height - 1, 47, 86, 233)

        for y in range(0, offscreen_canvas.height):
            offscreen_canvas.SetPixel(0, y, 47, 86, 233)
            offscreen_canvas.SetPixel(offscreen_canvas.width - 1, y, 47, 86, 233)

# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
