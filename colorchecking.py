import imageprocess2 as ip2, cv2, numpy as np

BOUNDARIES_WHITE = ((80, 80, 80), (255, 255, 255))
BOUNDARIES_RED = ([17, 15, 70], [50, 56, 255])
BOUNDARIES_BLACK = ([0, 0, 0], [50, 50, 50])

THRESH_BLACK = (30, 30, 30)
THRESH_YELLOW = (210, 255, 255)
MAX_RANGE = 8


# def inRangeOf(colorWBY,colorBGR):
#     bPo, bNe = colorBGR[0]+MAX_RANGE, colorBGR[0]-MAX_RANGE
#     gPo, gNe = colorBGR[1]+MAX_RANGE, colorBGR[1]-MAX_RANGE
#     rPo, rNe = colorBGR[2]+MAX_RANGE, colorBGR[2]-MAX_RANGE
#     pass

def newInRangeOfWhite(img):
    assert len(img.shape) == 3, 'BGR Image is needed'
    lower = BOUNDARIES_WHITE[0]
    upper = BOUNDARIES_WHITE[1]
    newimg = np.zeros(img.shape, dtype=np.uint8)
    for y in xrange(len(img)):
        for x in xrange(len(img[y])):
            bgr = img[y, x]
            b = int(bgr[0])
            g = int(bgr[1])
            r = int(bgr[2])
            if lower[0] <= b and b <= upper[0]:
                if lower[1] <= g and g <= upper[1]:
                    if lower[2] <= r and r <= upper[2]:
                        if nearColor(bgr, 25):
                            newimg[y, x] = bgr
    return newimg


def newInRangeOfBlack(img):
    lower = BOUNDARIES_BLACK[0]
    upper = BOUNDARIES_BLACK[1]
    newimg = np.zeros(img.shape, dtype=np.uint8)
    for y in xrange(len(img)):
        for x in xrange(len(img[y])):
            bgr = img[y, x]
            b = int(bgr[0])
            g = int(bgr[1])
            r = int(bgr[2])
            if lower[0] <= b and b <= upper[0]:
                if lower[1] <= g and g <= upper[1]:
                    if lower[2] <= r and r <= upper[2]:
                        if nearColor(bgr, 40):
                            newimg[y, x] = bgr
    return newimg


def invertColor(img):
    newimg = np.zeros(img.shape, dtype=np.uint8)
    for y in xrange(len(img)):
        for x in xrange(len(img[y])):
            newimg[y, x, 0] = 255-int(img[y, x, 0])
            newimg[y, x, 1] = 255-int(img[y, x, 1])
            newimg[y, x, 2] = 255-int(img[y, x, 2])
    return newimg


def nearColor(bgr, errorValue):
    b = int(bgr[0])
    g = int(bgr[1])
    r = int(bgr[2])
    # print b, g, b-g
    if abs(b-g) <= errorValue:
        if abs(b-r) <= errorValue:
            if abs(g-r) <= errorValue:
                return True
    return False


def inRangeOfWhite(img):
    lower = BOUNDARIES_WHITE[0]
    upper = BOUNDARIES_WHITE[1]
    lower = np.array(lower, dtype=np.uint8)
    upper = np.array(upper, dtype=np.uint8)

    mask = cv2.inRange(img, lower, upper)
    output = cv2.bitwise_and(img, img, mask=mask)
    return output


def inRangeOfBlack(img):
    lower, upper = boundary(BOUNDARIES_BLACK)
    mask = cv2.inRange(img, lower, upper)
    output = cv2.bitwise_and(img, img, mask=mask)
    return output


def inRangeOfRed(img):
    lower = BOUNDARIES_RED[0]
    upper = BOUNDARIES_RED[1]
    lower = np.array(lower, dtype=np.uint8)
    upper = np.array(upper, dtype=np.uint8)

    mask = cv2.inRange(img, lower, upper)
    output = cv2.bitwise_and(img, img, mask=mask)
    return output


def inRangeOfGreyScale(img, min, max):
    mask = cv2.inRange(img, min, max)
    output = cv2.bitwise_and(img, img, mask=mask)
    return output


def boundary(boundary_color):
    lower = boundary_color[0]
    upper = boundary_color[1]
    lower = np.array(lower, dtype=np.uint8)
    upper = np.array(upper, dtype=np.uint8)
    return lower, upper
