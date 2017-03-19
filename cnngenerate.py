import caffe
from caffe import layers as L, params as P


def lenetData(lmdb_train, lmdb_test, batch_size_train, batch_size_test):
	n = caffe.NetSpec()
	temp_n = caffe.NetSpec()
	temp_n.data, temp_n.label = L.Data(batch_size=batch_size_train, backend=P.Data.LMDB, source=lmdb_train,
	                                   transform_param=dict(scale=1./255), ntop=2, include=dict(phase=caffe.TRAIN))
	n.data, n.label = L.Data(batch_size=batch_size_test, backend=P.Data.LMDB, source=lmdb_test,
	                         transform_param=dict(scale=1./255), ntop=2, include=dict(phase=caffe.TEST))
	return n, temp_n


def conv(input_blob, kernel_size, num_output):
	return L.Convolution(input_blob, kernel_size=kernel_size, num_output=num_output, weight_filler=dict(type='xavier'),
	                     bias_filler=dict(type='constant'), param=[dict(lr_mult=1), dict(lr_mult=2)])


def pooling(input_blob, kernel_size, stride, method=P.Pooling.MAX):
	return L.Pooling(input_blob, kernel_size=kernel_size, stride=stride, pool=method)


def ip(input_blob, num_output):
	return L.InnerProduct(input_blob, num_output=num_output, weight_filler=dict(type='xavier'),
	                      bias_filler=dict(type='constant'), param=[dict(lr_mult=1), dict(lr_mult=2)])

def relu(input_blob):
	return L.ReLU(input_blob, in_place=True)

def accuracy(input_blob, label_blob):
	return L.Accuracy(input_blob, label_blob, include=dict(phase=caffe.TEST))

def loss(input_blob, label_blob):
	return L.SoftmaxWithLoss(input_blob, label_blob)

def lenetV2(*args):
	if len(args) != 4:
		raise Exception('wrong param')
	n, temp_n = lenetData(*args)
	n.conv1 = conv(n.data, 3, 30)
	n.conv2 = conv(n.conv1, 3, 60)
	n.pool2 = pooling(n.conv2, 2, 2)
	n.conv3 = conv(n.pool2, 3, 90)
	n.pool3 = pooling(n.conv3, 2, 2)
	n.conv4 = conv(n.pool3, 3, 120)
	n.ip1 = ip(n.conv4,750)
	n.relu1 = relu(n.ip1)
	n.ip2 = ip(n.relu1,34)
	n.accuracy = accuracy(n.ip2, n.label)
	n.loss = loss(n.ip2, n.label)
	return str(temp_n.to_proto())+str(n.to_proto())

def inputLenetV2():
	n = caffe.NetSpec()
	n.data = L.Input(input_param=dict(shape=[dict(dim=[1,1,32,32])]))
	n.conv1 = conv(n.data, 3, 30)
	n.conv2 = conv(n.conv1, 3, 60)
	n.pool2 = pooling(n.conv2, 2, 2)
	n.conv3 = conv(n.pool2, 3, 90)
	n.pool3 = pooling(n.conv3, 2, 2)
	n.conv4 = conv(n.pool3, 3, 120)
	n.ip1 = ip(n.conv4, 750)
	n.relu1 = relu(n.ip1)
	n.ip2 = ip(n.relu1, 34)
	n.prob = L.Softmax(n.ip2)
	return str(n.to_proto())

def lenet(lmdb_train, lmdb_test, batch_size_train, batch_size_test):
	n = caffe.NetSpec()
	temp_n = caffe.NetSpec()
	temp_n.data, temp_n.label = L.Data(batch_size=batch_size_train, backend=P.Data.LMDB, source=lmdb_train,
	                                   transform_param=dict(scale=1./255), ntop=2, include=dict(phase=caffe.TRAIN))
	n.data, n.label = L.Data(batch_size=batch_size_test, backend=P.Data.LMDB, source=lmdb_test,
	                         transform_param=dict(scale=1./255), ntop=2, include=dict(phase=caffe.TEST))
	n.conv1 = L.Convolution(n.data, kernel_size=5, num_output=30, weight_filler=dict(type='xavier'),
	                        bias_filler=dict(type='constant'), param=[dict(lr_mult=1), dict(lr_mult=2)])
	n.pool1 = L.Pooling(n.conv1, kernel_size=2, stride=2, pool=P.Pooling.MAX)
	n.conv2 = L.Convolution(n.pool1, kernel_size=5, num_output=70, weight_filler=dict(type='xavier'),
	                        bias_filler=dict(type='constant'), param=[dict(lr_mult=1), dict(lr_mult=2)])
	n.pool2 = L.Pooling(n.conv2, kernel_size=2, stride=2, pool=P.Pooling.MAX)
	n.conv3 = L.Convolution(n.pool2, kernel_size=5, num_output=100, weight_filler=dict(type='xavier'),
	                        bias_filler=dict(type='constant'), param=[dict(lr_mult=1), dict(lr_mult=2)])
	n.ip1 = L.InnerProduct(n.conv3, num_output=750, weight_filler=dict(type='xavier'),
	                       bias_filler=dict(type='constant'), param=[dict(lr_mult=1), dict(lr_mult=2)])
	n.relu1 = L.ReLU(n.ip1, in_place=True)
	n.ip2 = L.InnerProduct(n.relu1, num_output=34, weight_filler=dict(type='xavier'), bias_filler=dict(type='constant'),
	                       param=[dict(lr_mult=1), dict(lr_mult=2)])
	n.accuracy = L.Accuracy(n.ip2, n.label, include=dict(phase=caffe.TEST))
	n.loss = L.SoftmaxWithLoss(n.ip2, n.label)
	return str(temp_n.to_proto())+str(n.to_proto())


def inputLenet():
	n = caffe.NetSpec()
	n.data = L.Input(input_param=dict(shape=[dict(dim=[1, 1, 28, 28])]))
	n.conv1 = L.Convolution(n.data, kernel_size=5, num_output=30, weight_filler=dict(type='xavier'),
	                        bias_filler=dict(type='constant'), param=[dict(lr_mult=1), dict(lr_mult=2)])
	n.pool1 = L.Pooling(n.conv1, kernel_size=2, stride=2, pool=P.Pooling.MAX)
	n.conv2 = L.Convolution(n.pool1, kernel_size=5, num_output=70, weight_filler=dict(type='xavier'),
	                        bias_filler=dict(type='constant'), param=[dict(lr_mult=1), dict(lr_mult=2)])
	n.pool2 = L.Pooling(n.conv2, kernel_size=2, stride=2, pool=P.Pooling.MAX)
	n.conv3 = L.Convolution(n.pool2, kernel_size=5, num_output=100, weight_filler=dict(type='xavier'),
	                        bias_filler=dict(type='constant'), param=[dict(lr_mult=1), dict(lr_mult=2)])
	n.ip1 = L.InnerProduct(n.conv3, num_output=750, weight_filler=dict(type='xavier'),
	                       bias_filler=dict(type='constant'), param=[dict(lr_mult=1), dict(lr_mult=2)])
	n.relu1 = L.ReLU(n.ip1, in_place=True)
	n.ip2 = L.InnerProduct(n.relu1, num_output=34, weight_filler=dict(type='xavier'), bias_filler=dict(type='constant'),
	                       param=[dict(lr_mult=1), dict(lr_mult=2)])
	n.prob = L.Softmax(n.ip2)
	return str(n.to_proto())


def netv3(*args):
	if len(args) != 4:
		raise Exception('wrong param')
	n, temp_n = lenetData(*args)
	n.conv1 = conv(n.data, 3, 60)
	n.conv2 = conv(n.conv1, 3, 90)
	n.pool2 = pooling(n.conv2, 2, 2)
	n.conv3 = conv(n.pool2, 3, 120)
	n.pool3 = pooling(n.conv3, 2, 2)
	n.conv4 = conv(n.pool3, 3, 150)
	n.ip1 = ip(n.conv4,1000)
	n.relu1 = relu(n.ip1)
	n.ip2 = ip(n.relu1, 500)
	n.relu2 = relu(n.ip2)
	n.ip3 = ip(n.relu2,34)
	n.accuracy = accuracy(n.ip3, n.label)
	n.loss = loss(n.ip3, n.label)
	return str(temp_n.to_proto())+str(n.to_proto())

def netinputv3():
	n = caffe.NetSpec()
	n.data = L.Input(input_param=dict(shape=[dict(dim=[1,1,32,32])]))
	n.conv1 = conv(n.data, 3, 60)
	n.conv2 = conv(n.conv1, 3, 90)
	n.pool2 = pooling(n.conv2, 2, 2)
	n.conv3 = conv(n.pool2, 3, 120)
	n.pool3 = pooling(n.conv3, 2, 2)
	n.conv4 = conv(n.pool3, 3, 150)
	n.ip1 = ip(n.conv4, 1000)
	n.relu1 = relu(n.ip1)
	n.ip2 = ip(n.relu1, 500)
	n.relu2 = relu(n.ip2)
	n.ip3 = ip(n.relu2, 34)
	n.prob = L.Softmax(n.ip3)
	return str(n.to_proto())


# print dict(type='xavier')
# print str(lenetV2('C:/Users/pc/Desktop/carplate_model/carplate_lmdb_train',
#                 'C:\Users\pc\Desktop\carplate_model/carplate_lmdb_test', 64, 100))
#
# with open('C:/Users/pc/Desktop/carplate_model/carplate_train_test_0818.prototxt', 'w') as f:
# 	f.write(lenetV2('C:/Users/pc/Desktop/carplate_model/carplate_lmdb_train',
# 	              'C:/Users/pc/Desktop/carplate_model/carplate_lmdb_test', 64, 100))
#
# with open('C:/Users/pc/Desktop/carplate_model/carplate_input_0818.prototxt', 'w') as f:
# 	f.write(inputLenetV2())
#
#
# f.write(str(lenet('carplate_model/carplate_train_lmdb',64)))
#
# with open('carplate_model/lenet_carplate_test.prototxt','w') as f:
#     f.write(str(lenet('carplate_model/carplate_test_lmdb',100)))

with open('model/carplate_train_test_060317.prototxt','w') as f:
	f.write(netv3('C:/Users/pc/Desktop/carplate_model/carplate_lmdb_train_0818',
	              'C:/Users/pc/Desktop/carplate_model/carplate_lmdb_test_0818'
	              ,64
	              ,100))

with open('model/carplate_input_060317.prototxt', 'w') as f:
	f.write(netinputv3())
