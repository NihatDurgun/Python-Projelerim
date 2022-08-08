import nltk

from utils import *
from model import *
import model
import pickle

ni = int(np.ceil(np.sqrt(batch_size)))
save_dir = "checkpoint"
with open("_vocab.pickle", 'rb') as f:
    vocab = pickle.load(f)

t_real_image = tf.placeholder('float32', [batch_size, image_size, image_size, 3], name = 'real_image')

t_real_caption = tf.placeholder(dtype=tf.int64, shape=[batch_size, None], name='real_caption_input')

t_z = tf.placeholder(tf.float32, [batch_size, z_dim], name='z_noise')
generator_txt2img = model.generator_txt2img_resnet

net_rnn = rnn_embed(t_real_caption, is_train=False, reuse=False)
net_g, _ = generator_txt2img(t_z,
net_rnn.outputs,
is_train=False, reuse=False, batch_size=batch_size)

sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
tl.layers.initialize_global_variables(sess)

net_rnn_name = os.path.join(save_dir, 'net_rnn.npz')
net_cnn_name = os.path.join(save_dir, 'net_cnn.npz')
net_g_name = os.path.join(save_dir, 'net_g.npz')
net_d_name = os.path.join(save_dir, 'net_d.npz')

net_rnn_res = tl.files.load_and_assign_npz(sess=sess, name=net_rnn_name, network=net_rnn)

net_g_res = tl.files.load_and_assign_npz(sess=sess, name=net_g_name, network=net_g)

    ## seed for generation, z and sentence ids
sample_size = batch_size
sample_seed = np.random.normal(loc=0.0, scale=1.0, size=(sample_size, z_dim)).astype(np.float32)
        # sample_seed = np.random.uniform(low=-1, high=1, size=(sample_size, z_dim)).astype(np.float32)]
n = int(sample_size / ni)
sample_sentence = ["the flower shown has yellow anther red pistil and bright red petals."] * n + \
                  ["this flower has petals that are yellow, white and purple and has dark lines"] * n + \
                  ["the petals on this flower are white with a yellow center"] * n + \
                  ["this flower has a lot of small round pink petals."] * n + \
                  ["this flower is orange in color, and has petals that are ruffled and rounded."] * n + \
                  ["the flower has yellow petals and the center of it is brown."] * n + \
                  ["this flower has petals that are blue and white."] * n +\
                  ["these white flowers have petals that start off white in color and end in a white towards the tips."] * n

for i, sentence in enumerate(sample_sentence):
 print("seed: %s" % sentence)
 sentence = preprocess_caption(sentence)
 sample_sentence[i] = [vocab.word_to_id(word) for word in nltk.tokenize.word_tokenize(sentence)] + [vocab.end_id] # add END_ID

sample_sentence = tl.prepro.pad_sequences(sample_sentence, padding='post')

img_gen, rnn_out = sess.run([net_g_res.outputs, net_rnn_res.outputs], feed_dict={
t_real_caption : sample_sentence,
t_z : sample_seed})

save_images(img_gen, [ni, ni], 'samples\\gen.png')
