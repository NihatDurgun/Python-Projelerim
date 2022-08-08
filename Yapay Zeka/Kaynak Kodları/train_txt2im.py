#! /usr/bin/python
# -*- coding: utf8 -*-

""" GAN-CLS """
import tensorflow.compat.v1 as tf
tf.compat.v1.disable_eager_execution()
from tensorlayer.cost import *
import nltk

from utils import *
from model import *
import model

###Önişlemlerinin tamamlandığı verilerin train edilmesi için çekildiği yer
print("Loading data from pickle ...")
import pickle
with open("_vocab.pickle", 'rb') as f:
    vocab = pickle.load(f)
with open("_image_train.pickle", 'rb') as f:
    _, images_train = pickle.load(f)
with open("_image_test.pickle", 'rb') as f:
    _, images_test = pickle.load(f)
with open("_n.pickle", 'rb') as f:
    n_captions_train, n_captions_test, n_captions_per_image, n_images_train, n_images_test = pickle.load(f)
with open("_caption.pickle", 'rb') as f:
    captions_ids_train, captions_ids_test = pickle.load(f)

#train edebilmek amacıyla numpy arraye çevirilir.
images_train = np.array(images_train)
images_test = np.array(images_test)

#Gerekli dizinlerin oluşturulması
ni = int(np.ceil(np.sqrt(batch_size)))
tl.files.exists_or_mkdir("samples/step1_gan-cls")
tl.files.exists_or_mkdir("samples/step_pretrain_encoder")
tl.files.exists_or_mkdir("checkpoint")
save_dir = "checkpoint"


def main_train():
    ### Modelin tanımlanması
    # Dataların tutulmasını sağlayan altyapının oluşturulması
    t_real_image = tf.placeholder('float32', [batch_size, image_size, image_size, 3], name = 'real_image')
    t_wrong_image = tf.placeholder('float32', [batch_size ,image_size, image_size, 3], name = 'wrong_image')
    t_real_caption = tf.placeholder(dtype=tf.int64, shape=[batch_size, None], name='real_caption_input')
    t_wrong_caption = tf.placeholder(dtype=tf.int64, shape=[batch_size, None], name='wrong_caption_input')
    t_z = tf.placeholder(tf.float32, [batch_size, z_dim], name='z_noise')

    ## text-to-image haritalama için eğitim çıkarımları
    # Convolutional Neural Networks - CNN açılımı, Girdi olarak görse lalan bir derin öğrenme algoritması.
    # Amacı, görsellerdeki özellikleri yakalayıp sınıflandırmak.
    # RNN - Recurrent Neural Network bir sonraki adımı tahmin etmeye çalışan derin öğrenme algoritması
    # Görseller CNN ile işlenirken, metinler RNN ile işlenmektedir.
    net_cnn = cnn_encoder(t_real_image, is_train=True, reuse=False)
    x = net_cnn.outputs
    v = rnn_embed(t_real_caption, is_train=True, reuse=False).outputs
    x_w = cnn_encoder(t_wrong_image, is_train=True, reuse=True).outputs
    v_w = rnn_embed(t_wrong_caption, is_train=True, reuse=True).outputs

    # Reduce Mean = Bir tensörün boyutları boyunca öğelerin ortalamasını hesaplar.
    # RNN Loss = RNN öğrenmesi sırasında farkedilen kayıp oranını belirler.
    alpha = 0.2 # margin alpha
    rnn_loss = tf.reduce_mean(tf.maximum(0., alpha - cosine_similarity(x, v) + cosine_similarity(x, v_w))) + \
                tf.reduce_mean(tf.maximum(0., alpha - cosine_similarity(x, v) + cosine_similarity(x_w, v)))

    ## txt2img için eğitim çıkarımları
    ## Random görseller üreten model içerisindeki fonksiyon çağırılır.
    generator_txt2img = model.generator_txt2img_resnet
    
    # Generatorun oluşturduğu random görselleri gerçek/sahte diye sınıflandırır.
    discriminator_txt2img = model.discriminator_txt2img_resnet
    # Cümlelerin girdisini alarak öğrenmeyi sağlayan bir derin öğrenme algoritmasıdır.
    net_rnn = rnn_embed(t_real_caption, is_train=False, reuse=True)
    #Sahte fotoğraflar oluşturulur
    net_fake_image, _ = generator_txt2img(t_z,
                    net_rnn.outputs,
                    is_train=True, reuse=False, batch_size=batch_size)
    # Ayırma fonksiyonu ile sahte fotoğraflar ayrılır.
    net_d, disc_fake_image_logits = discriminator_txt2img(
                    net_fake_image.outputs, net_rnn.outputs, is_train=True, reuse=False)
    # Ayırma fonksiyonu ile gerçek fotoğraflar ayrılır.
    _, disc_real_image_logits = discriminator_txt2img(
                    t_real_image, net_rnn.outputs, is_train=True, reuse=True)
    # Gerçek resimdeki metinlerle olan uyuşmazlıklar bulunur.
    _, disc_mismatch_logits = discriminator_txt2img(
                    t_real_image,
                    rnn_embed(t_wrong_caption, is_train=False, reuse=True).outputs,
                    is_train=True, reuse=True)

    ## txt2img için test çıkarımları
    net_g, _ = generator_txt2img(t_z,
                    rnn_embed(t_real_caption, is_train=False, reuse=True).outputs,
                    is_train=False, reuse=True, batch_size=batch_size)

    d_loss1 = tl.cost.sigmoid_cross_entropy(disc_real_image_logits, tf.ones_like(disc_real_image_logits), name='d1')
    d_loss2 = tl.cost.sigmoid_cross_entropy(disc_mismatch_logits,  tf.zeros_like(disc_mismatch_logits), name='d2')
    d_loss3 = tl.cost.sigmoid_cross_entropy(disc_fake_image_logits, tf.zeros_like(disc_fake_image_logits), name='d3')
    d_loss = d_loss1 + (d_loss2 + d_loss3) * 0.5
    g_loss = tl.cost.sigmoid_cross_entropy(disc_fake_image_logits, tf.ones_like(disc_fake_image_logits), name='g')

    ####======================== Eğitim opsiyonlarının tanımlanması ==============================###
    lr = 0.0002 # Learning Rate
    lr_decay = 0.5 # Öğrenme oranı azalması
    decay_every = 100 # Her 100 epochta kontrol et.
    beta1 = 0.5 # İlk an tahminleri için üstel bozulma oranı
    
    # Tensorlayerlar üzerinden ilgili tensor katmanları çağırılır.
    cnn_vars = tl.layers.get_variables_with_name('cnn', True, True)
    rnn_vars = tl.layers.get_variables_with_name('rnn', True, True)
    d_vars = tl.layers.get_variables_with_name('discriminator', True, True)
    g_vars = tl.layers.get_variables_with_name('generator', True, True)
    
    # En verimli sonucu almak için kullanılan optimizasyon çeşitlerinin belirlendiği alan.
    with tf.variable_scope('learning_rate'):
        lr_v = tf.Variable(lr, trainable=False)
    d_optim = tf.train.AdamOptimizer(lr_v, beta1=beta1).minimize(d_loss, var_list=d_vars )
    g_optim = tf.train.AdamOptimizer(lr_v, beta1=beta1).minimize(g_loss, var_list=g_vars )
    grads, _ = tf.clip_by_global_norm(tf.gradients(rnn_loss, rnn_vars + cnn_vars), 10)
    optimizer = tf.train.AdamOptimizer(lr_v, beta1=beta1)
    rnn_optim = optimizer.apply_gradients(zip(grads, rnn_vars + cnn_vars))

    ###============================ Eğitim ====================================###
    sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
    tl.layers.initialize_global_variables(sess)

    # En son train edilmiş model kayıtlarını yükler.
    net_rnn_name = os.path.join(save_dir, 'net_rnn.npz')
    net_cnn_name = os.path.join(save_dir, 'net_cnn.npz')
    net_g_name = os.path.join(save_dir, 'net_g.npz')
    net_d_name = os.path.join(save_dir, 'net_d.npz')

    load_and_assign_npz(sess=sess, name=net_rnn_name, model=net_rnn)
    load_and_assign_npz(sess=sess, name=net_cnn_name, model=net_cnn)
    load_and_assign_npz(sess=sess, name=net_g_name, model=net_g)
    load_and_assign_npz(sess=sess, name=net_d_name, model=net_d)

    ## Seed argümanı, karıştırma ve dönüşümler için isteğe bağlı rastgele sayılar üretir.
    sample_size = batch_size
    sample_seed = np.random.normal(loc=0.0, scale=1.0, size=(sample_size, z_dim)).astype(np.float32)
    # ni değeri Batch Size'ın kare kökünün yuvarlanmış halidir.
    # n değişkeni ise Batch size'ın, kendi karekökünün yuvarlanmış haline bölümüdür. Ayrıca integer dönüştürmede noktalı kısım atılır.
    n = int(sample_size / ni)
    sample_sentence = ["the flower shown has yellow anther red pistil and bright red petals."] * n + \
                      ["this flower has petals that are yellow, white and purple and has dark lines"] * n + \
                      ["the petals on this flower are white with a yellow center"] * n + \
                      ["this flower has a lot of small round pink petals."] * n + \
                      ["this flower is orange in color, and has petals that are ruffled and rounded."] * n + \
                      ["the flower has yellow petals and the center of it is brown."] * n + \
                      ["this flower has petals that are blue and white."] * n +\
                      ["these white flowers have petals that start off white in color and end in a white towards the tips."] * n

    # Array içindeki örnek cümleleri preprocess_caption vasıtasıyla parçalar,
    # word tokenize ile kelimeleri parçalayıp örnek cümleler dizisinin her bir elemanına parçaladığı kelimeleri atar,
    # pad_sequences fonksiyonu ile Array boyutlarını eşit hale getirir.
    for i, sentence in enumerate(sample_sentence):
        print("seed: %s" % sentence)
        sentence = preprocess_caption(sentence)
        sample_sentence[i] = [vocab.word_to_id(word) for word in nltk.tokenize.word_tokenize(sentence)] + [vocab.end_id]    # add END_ID
    sample_sentence = tl.prepro.pad_sequences(sample_sentence, padding='post')

    # Veriseti üzerinden kaç defa geçileceği, kaç öğrenme tekrarı olacağı epoch ile belirtilir.
    n_epoch = 100 # 600
    print_freq = 1
    # Toplam train sayısının bir seferde yapılacak işlem sayısına bölümü sonucunda epoch başına düen batch sayısı belirlenir.
    n_batch_epoch = int(n_images_train / batch_size)
    # Epochları döngü ile epoch sayısı kadar uygular.
    for epoch in range(0, n_epoch+1):
        start_time = time.time()

        if epoch !=0 and (epoch % decay_every == 0):
            new_lr_decay = lr_decay ** (epoch // decay_every) # Her 100 epochta bir yeni bir öğrenme oranı hesaplanır.
            sess.run(tf.assign(lr_v, lr * new_lr_decay)) # Tensorflow a yeni öğrenme oranı atanır.
            log = " ** new learning rate: %f" % (lr * new_lr_decay)
            print(log)
        elif epoch == 0:
            log = " ** init lr: %f  decay_every_epoch: %d, lr_decay: %f" % (lr, decay_every, lr_decay)
            print(log)

        for step in range(n_batch_epoch): #Her epochta işlem yapılacak batch sayısı döner.
            step_time = time.time()
            # Gerçek ve yanlış cümleler üzerinden göresellerin eğitilmesini sağlayan kod bloğu.
            idexs = get_random_int(min=0, max=n_captions_train-1, number=batch_size)
            b_real_caption = captions_ids_train[idexs]
            b_real_caption = tl.prepro.pad_sequences(b_real_caption, padding='post')
            b_real_images = images_train[np.floor(np.asarray(idexs).astype('float')/n_captions_per_image).astype('int')]
            idexs = get_random_int(min=0, max=n_captions_train-1, number=batch_size)
            b_wrong_caption = captions_ids_train[idexs]
            b_wrong_caption = tl.prepro.pad_sequences(b_wrong_caption, padding='post')
            idexs2 = get_random_int(min=0, max=n_images_train-1, number=batch_size)
            b_wrong_images = images_train[idexs2]
            b_z = np.random.normal(loc=0.0, scale=1.0, size=(sample_size, z_dim)).astype(np.float32)
            b_real_images = threading_data(b_real_images, prepro_img, mode='train')   # [0, 255] --> [-1, 1] + augmentation
            b_wrong_images = threading_data(b_wrong_images, prepro_img, mode='train')
            ## updates text-to-image mapping
            if epoch < 50:
                errRNN, _ = sess.run([rnn_loss, rnn_optim], feed_dict={
                                                t_real_image : b_real_images,
                                                t_wrong_image : b_wrong_images,
                                                t_real_caption : b_real_caption,
                                                t_wrong_caption : b_wrong_caption})
            else:
                errRNN = 0
            # Bu aşamada Fotoğraflar ile cümleleri birbiri ile eğiterek text-to-image haritalamasını günceller.
            # Her epocha düşen batch sayısı kadar veri işlemesi yapıldıktan sonra epoch sonunda ortaya çıkan map,
            # png olarak kaydedilir.
            ## updates D
            errD, _ = sess.run([d_loss, d_optim], feed_dict={
                            t_real_image : b_real_images,
                            t_wrong_caption : b_wrong_caption,
                            t_real_caption : b_real_caption,
                            t_z : b_z})
            ## updates G
            errG, _ = sess.run([g_loss, g_optim], feed_dict={
                            t_real_caption : b_real_caption,
                            t_z : b_z})

            print("Epoch: [%2d/%2d] [%4d/%4d] time: %4.4fs, d_loss: %.8f, g_loss: %.8f, rnn_loss: %.8f" \
                        % (epoch, n_epoch, step, n_batch_epoch, time.time() - step_time, errD, errG, errRNN))

        if (epoch + 1) % print_freq == 0:
            print(" ** Epoch %d took %fs" % (epoch, time.time()-start_time))
            img_gen, rnn_out = sess.run([net_g.outputs, net_rnn.outputs], feed_dict={
                                        t_real_caption : sample_sentence,
                                        t_z : sample_seed})

            save_images(img_gen, [ni, ni], 'samples/step1_gan-cls/train_{:02d}.png'.format(epoch))

        ## save model
        # Her 10 epochta bir modeli checkpoint olarak kaydeder.
        if (epoch != 0) and (epoch % 10) == 0:
            tl.files.save_npz(net_cnn.all_params, name=net_cnn_name, sess=sess)
            tl.files.save_npz(net_rnn.all_params, name=net_rnn_name, sess=sess)
            tl.files.save_npz(net_g.all_params, name=net_g_name, sess=sess)
            tl.files.save_npz(net_d.all_params, name=net_d_name, sess=sess)
            print("[*] Save checkpoints SUCCESS!")
        # Her 100 epochta bir de ekstra train dosyası oluşturur.
        if (epoch != 0) and (epoch % 100) == 0:
            tl.files.save_npz(net_cnn.all_params, name=net_cnn_name+str(epoch), sess=sess)
            tl.files.save_npz(net_rnn.all_params, name=net_rnn_name+str(epoch), sess=sess)
            tl.files.save_npz(net_g.all_params, name=net_g_name+str(epoch), sess=sess)
            tl.files.save_npz(net_d.all_params, name=net_d_name+str(epoch), sess=sess)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('--mode', type=str, default="train", #Komut satırından argüman alarak çalıştırılabilir.
                       help='train, train_encoder, translation')

    args = parser.parse_args()

    if args.mode == "train":
        main_train() #Train argümanı ile eğitimi başlatır. Varsayılan argümandır. Diğer argümanları devre dışı bıraktık.