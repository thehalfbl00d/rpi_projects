from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
from luma.core.legacy import text
import datetime
import time
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT
from PIL import ImageFont

font=ImageFont.load_default()

serial = spi(port=0, device=0, gpio=noop())  
device = max7219(serial,
                 cascaded=4,
                 rotate=0,
                 block_orientation = -90,
                 blocks_arranged_in_reverse_order=False)

while 1:
    time1 = datetime.datetime.now()
    time1 = time1.strftime('%H:%M')
    with canvas(device) as draw:
        draw.text((2,-2),str(time1),font=font, fill="white")
    time.sleep(1)
