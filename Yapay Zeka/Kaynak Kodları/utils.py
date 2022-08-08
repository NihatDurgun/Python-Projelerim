import scipy.misc
import string
import imageio

##oluşturulan .npz uzantılı dosyaları modeli tekrar çalıştırmak için kullanılır.
def load_and_assign_npz(sess=None, name="", model=None):
    assert model is not None
    assert sess is not None
    if not os.path.exists(name):
        print("[!] Loading {} model failed!".format(name))
        return False
    else:
        params = tl.files.load_npz(name=name)
        tl.files.assign_params(sess, params, model)
        print("[*] Loading {} model SUCCESS!".format(name))
        return model


#verilen klasördeki klasör listesini döndürür.
def load_folder_list(path=""):
    return [os.path.join(path,o) for o in os.listdir(path) if os.path.isdir(os.path.join(path,o))]

#dictinary yapısında bütün anahtarları ve itemları yazdırır.
def print_dict(dictionary={}):
    for key, value in dictionary.iteritems():
        print("key: %s  value: %s" % (str(key), str(value)))

#random bir liste döndürür.
def get_random_int(min=0, max=10, number=5):
    return [random.randint(min,max) for p in range(0,number)]

#verilen caption hakkında öndüzenlemeye yapar.
def preprocess_caption(line):
    prep_line = re.sub('[%s]' % re.escape(string.punctuation), ' ', line.rstrip())
    prep_line = prep_line.replace('-', ' ')
    return prep_line

## resimleri belirtilen boyut içerisinde boyutlandırıp bir array haline getirir
def merge(images, size):
    h, w = images.shape[1], images.shape[2]
    img = np.zeros((h * size[0], w * size[1], 3))
    for idx, image in enumerate(images):
        i = idx % size[1]
        j = idx // size[1]
        img[j*h:j*h+h, i*w:i*w+w, :] = image
    return img

##resimleri mergeleyerek kaydeder
def imsave(images, size, path):
    return imageio.imwrite(path, merge(images, size))

## resimleri kaydetmesi için imsave fonksiyonuna yönlendirir
def save_images(images, size, image_path):
    return imsave(images, size, image_path)

##verilen resim verilen mode tipine göre çeşitli değişikliklere uğrar. Bu değişiklikler genelde yönünü değiştirme, yeniden boyutlandırma kırpma vb eylemlerdir.
from tensorlayer.prepro import *
def prepro_img(x, mode=None):
    if mode=='train':
        x = flip_axis(x, axis=1, is_random=True)
        x = rotation(x, rg=16, is_random=True, fill_mode='nearest')
        x = imresize(x, size=[64+15, 64+15], interp='bilinear', mode=None)
        x = crop(x, wrg=64, hrg=64, is_random=True)
        x = x / (255. / 2.)
        x = x - 1.
    elif mode=='train_stackGAN':
        x = flip_axis(x, axis=1, is_random=True)
        x = rotation(x, rg=16, is_random=True, fill_mode='nearest')
        x = imresize(x, size=[316, 316], interp='bilinear', mode=None)
        x = crop(x, wrg=256, hrg=256, is_random=True)
        x = x / (255. / 2.)
        x = x - 1.
    elif mode=='rescale':
        x = (x + 1.) / 2.
    elif mode=='debug':
        x = flip_axis(x, axis=1, is_random=False)
        x = x / 255.
    elif mode=='translation':
        x = x / (255. / 2.)
        x = x - 1.
    else:
        raise Exception("Not support : %s" % mode)
    return x

##
def combine_and_save_image_sets(image_sets, directory):
    for i in range(len(image_sets[0])):
        combined_image = []
        for set_no in range(len(image_sets)):
            combined_image.append( image_sets[set_no][i] )
            combined_image.append( np.zeros((image_sets[set_no][i].shape[0], 5, 3)) )
        combined_image = np.concatenate( combined_image, axis = 1 )

        scipy.misc.imsave( os.path.join( directory,  'combined_{}.jpg'.format(i) ), combined_image)