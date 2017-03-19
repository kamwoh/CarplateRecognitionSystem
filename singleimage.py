import caffe
import numpy as np
import cv2


def convertIndex(index):
    string = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZ'
    return string[index]


def defineNewScore(image_name, scores, maxOnly=True, getIndex=False, display=True):
    if maxOnly:
        maxIndex = maxNumberIndex(scores)
        if display:
            print str(image_name)+' is '+convertIndex(maxIndex)+ \
                  ' with score '+str(float(scores[maxIndex]*100))+'%'
        if getIndex:
            return maxIndex
        else:
            return scores[maxIndex]
    else:
        if getIndex:
            print 'when maxOnly is False, getIndex cant be true'
        else:
            count = 0
            for score in scores:
                print str(image_name)+' is number '+str(count)+ \
                      ' with score '+"{0:.2f}".format(score*100)+'%'
                count += 1


def defineIndexScore(image_path, predicted_index):
    return convertIndex(predicted_index)

def defineScore(image_name, scores, maxOnly=True, getIndex=False, display=True):
    if maxOnly:
        maxIndex = maxNumberIndex(scores)
        if display:
            print str(image_name)+' is number '+str(maxIndex)+ \
                  ' with score '+str(float(scores[maxIndex]*100))+'%'
        if getIndex:
            return maxIndex
        else:
            return scores[maxIndex]
    else:
        if getIndex:
            print 'when maxOnly is False, getIndex cant be true'
        else:
            count = 0
            for score in scores:
                print str(image_name)+' is number '+str(count)+ \
                      ' with score '+"{0:.2f}".format(score*100)+'%'
                count += 1


def maxNumberIndex(array):
    maxNumber = array[0]
    maxIndex = 0
    count = 0
    for a in array:
        if a > maxNumber:
            maxNumber = a
            maxIndex = count
            # print str(maxNumber) +' max number at index '+str(maxIndex)
        count += 1
    return maxIndex

# deprecated
'''
def process(image_path,invert=False):
	image = PIL.Image.open(image_path)
	image = imageProcess.greyscaleImageObj(image)
	if invert is True:
		image = imageProcess.invertImageObj(image)	
	image = imageProcess.adjustContrast(image,2)
	image = imageProcess.removeNoise(image)
	image = imageProcess.addPadding(image)
	image = imageProcess.resize(image,(28,28))
	image.save(image_path)
	return image_path
'''

def initNet(model, pretrained):
    caffe.set_device(0)
    caffe.set_mode_gpu()
    net = caffe.Net(model, pretrained, caffe.TEST)
    return net


def initTransformer(net):
    transformer = caffe.io.Transformer({'data':net.blobs['data'].data.shape})
    transformer.set_raw_scale('data', 255)
    transformer.set_transpose('data', (2, 0, 1))
    return transformer


def newinputimage(image):
    imarray = np.float32(image)
    imarray = imarray/255
    b, g, r = cv2.split(imarray)
    caffe_image = cv2.merge([r, g, b])
    return caffe_image


def cv2caffe(cv_image):
    if len(cv_image.shape) == 3:
        # caffe_image = np.transpose(cv_image,(2,0,1))
        caffe_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    else:
        caffe_image = cv_image

    caffe_image = caffe_image[np.newaxis, np.newaxis, :, :]
    return caffe_image


def newinputimagegrey(image, transformer):
    cv2.imwrite('temp.png', image)
    caffe_image = inputimage('temp.png', transformer, color=False)
    return caffe_image


def inputimage(image_path, transformer, color=False):
    caffe_image = transformer.preprocess('data', caffe.io.load_image(image_path, color))
    return caffe_image
#
# def initConvertTransformer(net):
#     transformer = caffe.io.Transformer({})

def getProb(net, caffe_image):
    # net.blobs['data'].data[...] = caffe_image
    # cv2.imshow('', net.blobs['conv1'].data[...][0])
    output = net.forward(data=caffe_image)
    # print net.blobs,'sdfdf'
    # print net.blobs['conv1'].data[0]
    # print net.blobs['conv1'].data[0][0].shape
    # print net.blobs
    # for b in net.blobs['conv1'].data[0][0]:
    #     b *= 255
    #
    # for i in xrange(20):
    #     cv2.imshow('b',net.blobs['conv1'].data[0][i])
    #     cv2.waitKey(0)
    # print net.blobs['conv1'].data[0] == net.blobs['conv1'].data[1]
    # print net.blobs['conv1'].data[0]
    # print len(net.blobs)
    # print len(net.blobs['conv1'].data)
    # print len(net.blobs['conv2'])
    return int(output['prob'].argmax()), output['prob']
