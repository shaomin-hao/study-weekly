import numpy as np

# 激活函数
class ReluActivator:
    def forward(self, x):
        return max(0, x)
    def backward(self, x):
        return 1 if x > 0 else 0

class IdentityActivator:
    def forward(self, x):
        return x
    def backward(self, x):
        return 1

# 工具函数
def get_patch(input_array, i, j, filter_width, filter_height, stride):
    start_i = i * stride
    start_j = j * stride
    if input_array.ndim == 2:
        return input_array[start_i:start_i+filter_height, start_j:start_j+filter_width]
    elif input_array.ndim == 3:
        return input_array[:, start_i:start_i+filter_height, start_j:start_j+filter_width]

def get_max_index(array):
    max_i = max_j = 0
    max_val = array[0,0]
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if array[i,j] > max_val:
                max_val = array[i,j]
                max_i, max_j = i, j
    return max_i, max_j

def conv(input_array, kernel_array, output_array, stride, bias):
    out_h, out_w = output_array.shape
    k_h, k_w = kernel_array.shape[-2:]
    for i in range(out_h):
        for j in range(out_w):
            patch = get_patch(input_array, i, j, k_w, k_h, stride)
            output_array[i,j] = (patch * kernel_array).sum() + bias

def padding(input_array, zp):
    if zp == 0:
        return input_array
    if input_array.ndim == 3:
        c, h, w = input_array.shape
        padded = np.zeros((c, h+2*zp, w+2*zp))
        padded[:, zp:zp+h, zp:zp+w] = input_array
        return padded
    else:
        h, w = input_array.shape
        padded = np.zeros((h+2*zp, w+2*zp))
        padded[zp:zp+h, zp:zp+w] = input_array
        return padded

def element_wise_op(array, op):
    for i in np.nditer(array, op_flags=['readwrite']):
        i[...] = op(i)

# Filter类
class Filter:
    def __init__(self, width, height, depth):
        self.weights = np.random.uniform(-1e-4, 1e-4, (depth, height, width))
        self.bias = 0
        self.weights_grad = np.zeros_like(self.weights)
        self.bias_grad = 0

    def update(self, lr):
        self.weights -= lr * self.weights_grad
        self.bias -= lr * self.bias_grad

# 卷积层
class ConvLayer:
    def __init__(self, input_width, input_height, channel_number,
                 filter_width, filter_height, filter_number,
                 zero_padding, stride, activator, learning_rate):
        self.input_width = input_width
        self.input_height = input_height
        self.channel_number = channel_number
        self.filter_width = filter_width
        self.filter_height = filter_height
        self.filter_number = filter_number
        self.zero_padding = zero_padding
        self.stride = stride
        self.output_width = self.calc_out_size(input_width, filter_width, zero_padding, stride)
        self.output_height = self.calc_out_size(input_height, filter_height, zero_padding, stride)
        self.output_array = np.zeros((filter_number, self.output_height, self.output_width))
        self.filters = [Filter(filter_width, filter_height, channel_number) for _ in range(filter_number)]
        self.activator = activator
        self.learning_rate = learning_rate

    def calc_out_size(self, in_size, f_size, pad, stride):
        return (in_size - f_size + 2*pad) // stride + 1

    def forward(self, input_array):
        self.input_array = input_array
        self.padded_input_array = padding(input_array, self.zero_padding)
        for f in range(self.filter_number):
            flt = self.filters[f]
            conv(self.padded_input_array, flt.weights, self.output_array[f], self.stride, flt.bias)
        element_wise_op(self.output_array, self.activator.forward)

    def backward(self, input_array, sensitivity_array, activator):
        self.forward(input_array)
        self.bp_sensitivity_map(sensitivity_array, activator)
        self.bp_gradient(sensitivity_array)

    def expand_sensitivity_map(self, delta):
        c, h, w = delta.shape
        exp_h = self.input_height - self.filter_height + 2*self.zero_padding + 1
        exp_w = self.input_width - self.filter_width + 2*self.zero_padding + 1
        expand = np.zeros((c, exp_h, exp_w))
        for i in range(self.output_height):
            for j in range(self.output_width):
                expand[:, i*self.stride, j*self.stride] = delta[:,i,j]
        return expand

    def bp_sensitivity_map(self, delta, activator):
        expanded = self.expand_sensitivity_map(delta)
        zp = (self.input_width + self.filter_width - 1 - expanded.shape[2]) // 2
        padded = padding(expanded, zp)
        self.delta_array = np.zeros((self.channel_number, self.input_height, self.input_width))

        for f in range(self.filter_number):
            w = self.filters[f].weights
            flipped = np.array([np.rot90(weight, 2) for weight in w])
            tmp = np.zeros_like(self.delta_array)
            for d in range(self.channel_number):
                conv(padded[f], flipped[d], tmp[d], 1, 0)
            self.delta_array += tmp

        deriv = np.array(self.input_array)
        element_wise_op(deriv, activator.backward)
        self.delta_array *= deriv

    def bp_gradient(self, delta):
        expanded = self.expand_sensitivity_map(delta)
        for f in range(self.filter_number):
            flt = self.filters[f]
            for d in range(flt.weights.shape[0]):
                conv(self.padded_input_array[d], expanded[f], flt.weights_grad[d], 1, 0)
            flt.bias_grad = expanded[f].sum()

    def update(self):
        for f in self.filters:
            f.update(self.learning_rate)

# 最大池化层
class MaxPoolingLayer:
    def __init__(self, input_width, input_height, channel_number,
                 filter_width, filter_height, stride):
        self.input_width = input_width
        self.input_height = input_height
        self.channel_number = channel_number
        self.filter_width = filter_width
        self.filter_height = filter_height
        self.stride = stride
        self.output_width = (input_width - filter_width) // stride + 1
        self.output_height = (input_height - filter_height) // stride + 1
        self.output_array = np.zeros((channel_number, self.output_height, self.output_width))

    def forward(self, input_array):
        for c in range(self.channel_number):
            for i in range(self.output_height):
                for j in range(self.output_width):
                    p = get_patch(input_array[c], i, j, self.filter_width, self.filter_height, self.stride)
                    self.output_array[c,i,j] = np.max(p)

    def backward(self, input_array, sensitivity_array):
        self.delta_array = np.zeros_like(input_array)
        for c in range(self.channel_number):
            for i in range(self.output_height):
                for j in range(self.output_width):
                    p = get_patch(input_array[c], i, j, self.filter_width, self.filter_height, self.stride)
                    k, l = get_max_index(p)
                    self.delta_array[c, i*self.stride+k, j*self.stride+l] = sensitivity_array[c,i,j]

# ------------------- 测试代码（原文） -------------------
def init_test():
    a = np.array([[[0,1,1,0,2],[2,2,2,2,1],[1,0,0,2,0],[0,1,1,0,0],[1,2,0,0,2]],
                  [[1,0,2,2,0],[0,0,0,2,0],[1,2,1,2,1],[1,0,0,0,0],[1,2,1,1,1]],
                  [[2,1,2,0,0],[1,0,0,1,0],[0,2,1,0,1],[0,1,2,2,2],[2,1,0,0,1]]])
    b = np.array([[[0,1,1],[2,2,2],[1,0,0]],[[1,0,2],[0,0,0],[1,2,1]]])
    cl = ConvLayer(5,5,3,3,3,2,1,2,IdentityActivator(),0.001)
    cl.filters[0].weights = np.array([[[-1,1,0],[0,1,0],[0,1,1]],
                                     [[-1,-1,0],[0,0,0],[0,-1,0]],
                                     [[0,0,-1],[0,1,0],[1,-1,-1]]], dtype=np.float64)
    cl.filters[0].bias = 1
    cl.filters[1].weights = np.array([[[1,1,-1],[-1,-1,1],[0,-1,1]],
                                      [[0,1,0],[-1,0,-1],[-1,1,0]],
                                      [[-1,0,0],[-1,0,1],[-1,0,0]]], dtype=np.float64)
    return a, b, cl

def gradient_check():
    error_func = lambda o: o.sum()
    a, b, cl = init_test()
    cl.forward(a)
    delta = np.ones_like(cl.output_array)
    cl.backward(a, delta, IdentityActivator())
    eps = 10e-4
    for d in range(cl.filters[0].weights_grad.shape[0]):
        for i in range(cl.filters[0].weights_grad.shape[1]):
            for j in range(cl.filters[0].weights_grad.shape[2]):
                w = cl.filters[0].weights[d,i,j]
                cl.filters[0].weights[d,i,j] = w + eps
                cl.forward(a)
                e1 = error_func(cl.output_array)
                cl.filters[0].weights[d,i,j] = w - eps
                cl.forward(a)
                e2 = error_func(cl.output_array)
                expect = (e1 - e2) / (2*eps)
                cl.filters[0].weights[d,i,j] = w
                print(f'weights({d},{i},{j}): expected - actual {expect:.6f} - {cl.filters[0].weights_grad[d,i,j]:.6f}')

def test_pool():
    a = np.array([[[1,1,2,4],[5,6,7,8],[3,2,1,0],[1,2,3,4]],
                  [[0,1,2,3],[4,5,6,7],[8,9,0,1],[3,4,5,6]]], dtype=np.float32)
    delta = np.array([[[1,2],[2,4]],[[3,5],[8,2]]], dtype=np.float32)
    pool = MaxPoolingLayer(4,4,2,2,2,2)
    pool.forward(a)
    print('=== 池化前向 ===')
    print(pool.output_array)
    pool.backward(a, delta)
    print('=== 池化反向 ===')
    print(pool.delta_array)

# 运行测试
gradient_check()
# test_pool()
