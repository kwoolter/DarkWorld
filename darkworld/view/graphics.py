import pygame


class Colours:
    # set up the colours
    BLACK = (0, 0, 0)
    BROWN = (128, 64, 0)
    WHITE = (255, 255, 255)
    RED = (237, 28, 36)
    DARK_RED = (100, 0, 0)
    GREEN = (34, 177, 76)
    DARK_GREEN = (0, 100, 0)
    BLUE = (63, 72, 204)
    DARK_GREY = (40, 40, 40)
    GREY = (128, 128, 128)
    GOLD = (255, 201, 14)
    YELLOW = (255, 255, 0)
    TRANSPARENT = (255, 1, 1)


def draw_text(surface, msg, x, y, size=32, fg_colour=Colours.WHITE, bg_colour=Colours.BLACK, alpha: int = 255,
              centre: bool = True):
    font = pygame.font.Font(None, size)
    if bg_colour is not None:
        text = font.render(msg, 1, fg_colour, bg_colour)
    else:
        text = font.render(msg, 1, fg_colour)
    textpos = text.get_rect()

    if centre is True:
        textpos.centerx = x
    else:
        textpos.x = x

    textpos.centery = y
    surface.blit(text, textpos)
    surface.set_alpha(alpha)


# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = 2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        textpos = image.get_rect()
        textpos.centerx = rect.centerx
        textpos.y = y

        surface.blit(image, (textpos))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text


class CollisionDetection:
    def __init__(self):
        pass

    @staticmethod
    def line_line_intersection(a1, a2, b1, b2):
        x1, y1 = a1
        x2, y2 = a2

        x3, y3 = b1
        x4, y4 = b2

        uA = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
        uB = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))

        if (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1):
            return True
        else:
            return False

    @staticmethod
    def line_rectangle_intersection(a1, a2, rectangle_xywh):
        x1, y1 = a1
        x2, y2 = a2
        rx, ry, rw, rh = rectangle_xywh

        left = CollisionDetection.line_line_intersection(x1, y1, x2, y2, rx, ry, rx, ry + rh)
        right = CollisionDetection.line_line_intersection(x1, y1, x2, y2, rx + rw, ry, rx + rw, ry + rh)
        top = CollisionDetection.line_line_intersection(x1, y1, x2, y2, rx, ry, rx + rw, ry)
        bottom = CollisionDetection.line_line_intersection(x1, y1, x2, y2, rx, ry + rh, rx + rw, ry + rh)

        if left or right or top or bottom:
            return True
        else:
            return False


'''
    boolean
    lineLine(float
    x1, float
    y1, float
    x2, float
    y2, float
    x3, float
    y3, float
    x4, float
    y4) {

        // calculate
    the
    distance
    to
    intersection
    point
    float
    uA = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1));
    float
    uB = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1));

    // if uA and uB are between 0-1, lines are colliding
    if (uA >= 0 & & uA <= 1 & & uB >= 0 & & uB <= 1) {

    // optionally, draw a circle where the lines meet
    float intersectionX = x1 + (uA * (x2-x1));
    float intersectionY = y1 + (uA * (y2-y1));
    fill(255, 0, 0);
    noStroke();
    ellipse(intersectionX, intersectionY, 20, 20);

    return true;
    }
    return false;

}

boolean lineRect(float x1, float y1, float x2, float y2, float rx, float ry, float rw, float rh) {

  // check if the line has hit any of the rectangle's sides
  // uses the Line/Line function below
  boolean left =   lineLine(x1,y1,x2,y2, rx,ry,rx, ry+rh);
  boolean right =  lineLine(x1,y1,x2,y2, rx+rw,ry, rx+rw,ry+rh);
  boolean top =    lineLine(x1,y1,x2,y2, rx,ry, rx+rw,ry);
  boolean bottom = lineLine(x1,y1,x2,y2, rx,ry+rh, rx+rw,ry+rh);

  // if ANY of the above are true, the line
  // has hit the rectangle
  if (left || right || top || bottom) {
    return true;
  }
  return false;
}
'''


class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename)
        except Exception as err:
            print('Unable to load spritesheet image:', filename)
            raise err

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle=None, colorkey=None):
        if rectangle is None:
            rectangle = self.sheet.get_rect()
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, depth=24)
        key = (0, 255, 0)
        image.fill(key)
        image.set_colorkey(key)
        image.blit(self.sheet, (0, 0), rect)

        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey=None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey=None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)
