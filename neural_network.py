import numpy as np


class NeuralNetwork(object):
    def __init__(self, no_inputs, no_outputs, no_hidden_layers, hidden_layers_sizes):
        self.input_layer_size = no_inputs
        self.output_layer_size = no_outputs
        self.no_hidden_layers = no_hidden_layers
        self.W = []
        self.learning_rate = 0.001

        w0 = np.random.randn(self.input_layer_size, hidden_layers_sizes[0])
        self.W.append(w0)

        for i in range(1, no_hidden_layers):
            w = np.random.randn(hidden_layers_sizes[i - 1], hidden_layers_sizes[i])
            self.W.append(w)

        wn = np.random.randn(hidden_layers_sizes[-1], self.output_layer_size)
        self.W.append(wn)

    def forward(self, X):
        self.Z = []
        self.A = []

        z0 = np.dot(X, self.W[0])
        self.Z.append(z0)

        a0 = self.sigmoid_func(z0)
        self.A.append(a0)

        for i in range(1, self.W.__len__()):
            z = np.dot(self.A[i - 1], self.W[i])
            self.Z.append(z)
            a = self.sigmoid_func(z)
            self.A.append(a)

        return self.A[-1]

    def cost_function(self, X, y):
        predicted_values = self.forward(X)
        m = y.shape[0]
        cost = (1 / 2 * m) * sum((y - predicted_values) ** 2)
        return cost

    def train(self, X, y):
        gradients = self.compute_gradients(X, y)

        gradients_index = 0
        for i in range(0, self.W.__len__()):
            self.W[i] = np.subtract(self.W[i], self.learning_rate * gradients[i])
            gradients_index = gradients_index + 1

    def compute_gradients(self, X, y):
        y_predicted = self.forward(X)
        gradients = []
        deltas = []
        z_reversed_index = 0
        a_reversed_index = 1
        w_reversed_index = 0

        last_delta = np.multiply(-(y - y_predicted), self.sigmoid_func_prime(self.Z[-1]))
        deltas.append(last_delta)
        z_reversed_index = z_reversed_index + 1

        last_gradient = np.dot(self.A[-1 - a_reversed_index].T, last_delta)
        gradients.append(last_gradient)
        a_reversed_index = a_reversed_index + 1

        for i in range(1, self.no_hidden_layers):
            delta = np.dot(deltas[-1], self.W[-1 - w_reversed_index].T) * self.sigmoid_func_prime(
                self.Z[-1 - z_reversed_index])
            w_reversed_index = w_reversed_index + 1
            z_reversed_index = z_reversed_index + 1
            deltas.append(delta)
            gradient = np.dot(self.A[-1 - a_reversed_index].T, deltas[-1])
            a_reversed_index = a_reversed_index + 1
            gradients.append(gradient)

        first_delta = np.dot(deltas[-1], self.W[-1 - w_reversed_index].T) * self.sigmoid_func_prime(
            self.Z[-1 - z_reversed_index])

        first_gradient = np.dot(X.T, first_delta)
        gradients.append(first_gradient)

        gradients.reverse()
        return gradients

    def sigmoid_func(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_func_prime(self, x):
        return self.sigmoid_func(x) * (1 - self.sigmoid_func(x))

    def identical_func(self, x):
        return x

    def identical_func_prime(self, x):
        return 1

    def get_parameters(self):
        return self.W

    def set_parameters(self, W):
        self.W = W

    def mean_absolute_percentage_error(self, X, y):
        y_predicted = self.forward(X)
        return np.average(np.divide(np.absolute(y - y_predicted), y))

    def set_learning_rate(self, rate):
        self.learning_rate = rate

