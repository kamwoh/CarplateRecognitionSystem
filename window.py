import cv2, numpy as np


class Window():
    def __init__(self, windowName, size=(640, 480)):
        self.windowName = windowName
        self.size = size
        self.cv_image = CvImage()
        cv2.namedWindow(windowName)

    def putComponent(self, component, position=(0, 0)):
        self.cv_image[position[0]:position[0]+component.size[0],
        position[1]:position[1]+component.size[1]] = component.cv_image

    def display(self):
        cv2.imshow(self.windowName, self.cv_image)

    def resizeWindow(self, size):
        self.size = size
        self.cv_image.resize(size)


class Component():
    def __init__(self, cv_image):
        self.size = cv_image.shape[1], cv_image.shape[0]
        self.cv_image = cv_image

    def resize(self, size):
        self.size = size
        self.cv_image = cv2.resize(self.cv_image, (size[1], size[0]))


class CvImage(Component):
    def __init__(self, cv_image=None, size=None):
        if cv_image is not None:
            if type(cv_image) is basestring:
                raise Exception('cv_image is cv2 image type, please use CvImage.initFromFile if this is a file path')
            Component.__init__(self, cv_image)
        else:
            if size is not None:
                cv_image = np.zeros((size[1], size[0]),dtype=np.uint8)
                Component.__init__(self, cv_image)
            else:
                raise Exception('please set a value for size')

    @classmethod
    def initFromFile(cls, image_path, flags=None):
        if flags is None:
            cv_image = cv2.imread(image_path)
        else:
            cv_image = cv2.imread(image_path, flags)
        return CvImage(cv_image)
