import tensorflow as tf

class NeuralNetwork:

    def __init__(self, input_nodes, output_nodes):
        self.buildModel(input_nodes, output_nodes)
        
    def buildModel(self, input_nodes, output_nodes):
        x = tf.placeholder(tf.float32, shape=[None, 784])
        y_ = tf.placeholder(tf.float32, shape=[None, 10])

        W = tf.Variable(tf.zeros([784,10]))
        b = tf.Variable(tf.zeros([10]))

        y = tf.matmul(x,W) + b

        cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y, y_))
        train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

    def train(self, trainX, trainY):
        sess = tf.InteractiveSession()
        sess.run(tf.initialize_all_variables())

        for i in range(1000):
            batch = mnist.train.next_batch(100)
            train_step.run(feed_dict={x: batch[0], y_: batch[1]})

    def test(self, testX, testY):
        correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        print(accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels}))

