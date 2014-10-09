from pyfiglet import Figlet

class ASCIIArt(object):
    def __init__(self):
        self.figlet = Figlet()
        self.font_list = (
            '6x10', 'acrobatic', 'banner3', 'banner3-D', 'basic', 'big',
            'block', 'broadway', 'char3___', 'chunky', 'clb6x10', 'clr6x10',
            'clr8x8', 'cyberlarge', 'doh', 'doom', 'epic', 'f15_____',
            'georgia11', 'gothic', 'graceful', 'larry3d', 'pebbles', 'puffy',
            'rectangles', 'roman', 'rounded', 'serifcap', 'slant', 'standard',
            'starwars', 'univers'
        )

    def render(self, text, font=None):
        if not font:
            font = random.choice(self.font_list)
        self.figlet.setFont(font=font)
        return self.figlet.renderText(text)

    def render_all(self, text):
        for font in self.font_list:
            print '\n\n\n%s\n' % font
            print self.render(text, font)

if __name__ == '__main__':
    aa = ASCIIArt()
    print aa.render_all('Verily this vichysoisse of verbiage veers most verbose')
