import sys
import xbmcvfs
from PIL import Image, ImageDraw

SKIN_PATH = 'special://skin'


def interpolate(f_co, t_co, interval):
    det_co = [(t - f) / interval for f, t in zip(f_co, t_co)]
    for i in range(interval):
        yield [round(f + det * i) for f, det in zip(f_co, det_co)]


def hex_to_rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


class Main:
    def __init__(self):
        self.handle = sys.argv
        self.skin_path = xbmcvfs.translatePath(SKIN_PATH)
        self.gradient_path = self.skin_path + 'media/common/button_texture.png'

    def init(self):
        success = xbmcvfs.exists(self.skin_path)

        if not success:
            return False

        for h in self.handle:
            if h == 'gradient=true':
                self.generate_gradient()
            if h == 'monochrome=true':
                self.generate_monochrome()

    def generate_gradient(self):
        c1, c2 = None, None
        for h in self.handle:
            if 'highlight' in h:
                c1 = h.split('=')[1][2:]
            if 'gradient' in h:
                c2 = h.split('=')[1][2:]

        imgsize = (64, 64)
        gradient = Image.new('RGBA', imgsize, color=0)
        draw = ImageDraw.Draw(gradient)

        f_co = hex_to_rgb(c1)
        t_co = hex_to_rgb(c2)
        for i, color in enumerate(interpolate(f_co, t_co, gradient.width)):
            draw.line([(i, 0), (i, gradient.height)], tuple(color), width=1)
        gradient.save(self.gradient_path, 'png')

    def generate_monochrome(self):
        c1 = None
        for h in self.handle:
            if 'highlight' in h:
                c1 = h.split('=')[1][2:]

        imgsize = (64, 64)
        gradient = Image.new('RGBA', imgsize, color=hex_to_rgb(c1))
        gradient.save(self.gradient_path, 'png')


if __name__ == '__main__':
    Main().init()
