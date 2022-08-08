import nltk
from utils import *

dataset = '102flowers' # Veri Setimizin ismi
need_256 = True # stackGAN için True olması gerekiyor. StackGAN projesi yazıyı görsele dönüştürüyor.

if dataset == '102flowers':
    cwd = os.getcwd()
    #102flowers ve text_c10 klasörünün yolunu bulmaktadır.
    img_dir = os.path.join(cwd, '102flowers')
    caption_dir = os.path.join(cwd, 'text_c10')
    #vocab metin belgesinin oluşturacağı yeri belirler.
    VOC_FIR = cwd + '/vocab.txt'

    # her bir resmin captions dosyası içerisinde 10 tane cümlesi mevcut, burada her bir klasörü açıp içindekleri txt dosyalarını bulunuyor
    # txt dosyasındaki metinleri tensorflow cümle işleme fonksiyonuna sokuyor. Cümlede başlama(<S>) ve bitirme(</S>) kalıplarını ekliyor ve bunu processed_capts değişkenine entegre ediyor.
    caption_sub_dir = load_folder_list( caption_dir )
    captions_dict = {}
    processed_capts = []
    for sub_dir in caption_sub_dir: # get caption file list
        with tl.ops.suppress_stdout():
            files = tl.files.load_file_list(path=sub_dir, regx='^image_[0-9]+\.txt')
            for i, f in enumerate(files):
                file_dir = os.path.join(sub_dir, f)
                key = int(re.findall('\d+', f)[0])
                t = open(file_dir,'r')
                lines = []
                for line in t:
                    line = preprocess_caption(line)
                    lines.append(line)
                    processed_capts.append(tl.nlp.process_sentence(line, start_word="<S>", end_word="</S>"))
                assert len(lines) == 10, "Every flower image have 10 captions"
                captions_dict[key] = lines
    print(" * %d x %d captions found " % (len(captions_dict), len(lines)))

    # Vocab tensorflow txt dosyasına göre processed_capts arrayindeki captionlardan metin belgesini oluşturuyor eğer dosya varsa uyarı yapıyor
    if not os.path.isfile('vocab.txt'):
        _ = tl.nlp.create_vocab(processed_capts, word_counts_output_file=VOC_FIR, min_word_count=1)
    else:
        print("WARNING: vocab.txt already exists")
    #kelimeleri vocab dosyasından almak
    vocab = tl.nlp.Vocabulary(VOC_FIR, start_word="<S>", end_word="</S>", unk_word="<UNK>")

    ## bütün captionları nltk tokenizer vasıtasıyla parçalara ayırıp bunları captions_ids arrayine ekliyor
    captions_ids = []
    try: # python3
        tmp = captions_dict.items()
    except: # python3
        tmp = captions_dict.iteritems()
    for key, value in tmp:
        for v in value:
            captions_ids.append( [vocab.word_to_id(word) for word in nltk.tokenize.word_tokenize(v)] + [vocab.end_id])  # add END_ID
    captions_ids = np.asarray(captions_ids)
    print(" * tokenized %d captions" % len(captions_ids))

    ## kontrol örnek bir resmin cümlesini, cümlesinin parçalanmış halini amaçlı parçalanmış kelimelerin idsini yazmaktadır.
    img_capt = captions_dict[1][1]
    print("img_capt: %s" % img_capt)
    print("nltk.tokenize.word_tokenize(img_capt): %s" % nltk.tokenize.word_tokenize(img_capt))
    img_capt_ids = [vocab.word_to_id(word) for word in nltk.tokenize.word_tokenize(img_capt)]
    print("img_capt_ids: %s" % img_capt_ids)
    print("id_to_word: %s" % [vocab.id_to_word(id) for id in img_capt_ids])

    ## resimlerin olduğunu belirtilen klasörüden bütün resimleri alıyor kaç tane olduğunu yazdırıyor ve bu resimleri yeniden boyutlandırmaya başlıyor.
    with tl.ops.suppress_stdout():  # get image files list
        imgs_title_list = sorted(tl.files.load_file_list(path=img_dir, regx='^image_[0-9]+\.jpg'))
    print(" * %d images found, start loading and resizing ..." % len(imgs_title_list))
    s = time.time()

    ## resimleri tek tek boyutlandırıp float32 tipine çeviriyor. Eğer stackGAN kullanımı için need_256 boolunu true yapıyorsak 256'ya 256 olarak tekrar boyutlandırıp images ve images_256 arrayine atıyor.
    images = []
    images_256 = []
    for name in imgs_title_list:
        # print(name)
        img_raw = scipy.misc.imread( os.path.join(img_dir, name) )
        img = tl.prepro.imresize(img_raw, size=[64, 64])    # (64, 64, 3)
        img = img.astype(np.float32)
        images.append(img)
        if need_256:
            img = tl.prepro.imresize(img_raw, size=[256, 256]) # (256, 256, 3)
            img = img.astype(np.float32)

            images_256.append(img)
    print(" * loading and resizing took %ss" % (time.time()-s))

    ##Toplam resim ve caption sayısını yazdırıyor, her bir resim için 10 caption var.
    n_images = len(captions_dict)
    n_captions = len(captions_ids)
    n_captions_per_image = len(lines) # 10

    print("n_captions: %d n_images: %d n_captions_per_image: %d" % (n_captions, n_images, n_captions_per_image))

    ##train ve test için resimleri ve captionları parçalıyor. 8000 train görseli - 80000 train caption, 189 test görseli - 1890 test caption bulumaktadır.
    captions_ids_train, captions_ids_test = captions_ids[: 8000*n_captions_per_image], captions_ids[8000*n_captions_per_image :]
    images_train, images_test = images[:8000], images[8000:]
    if need_256:
        images_train_256, images_test_256 = images_256[:8000], images_256[8000:]
    n_images_train = len(images_train)
    n_images_test = len(images_test)
    n_captions_train = len(captions_ids_train)
    n_captions_test = len(captions_ids_test)
    print("n_images_train:%d n_captions_train:%d" % (n_images_train, n_captions_train))
    print("n_images_test:%d  n_captions_test:%d" % (n_images_test, n_captions_test))

##pickle uygulamanın oluşturduğu verileri dosyaya kaydedip tekrardan kullanmayı sağlar.
import pickle
def save_all(targets, file):
    with open(file, 'wb') as f:
        pickle.dump(targets, f)

##olusturulan veriler kaydedilir.
save_all(vocab, '_vocab.pickle')
save_all((images_train_256, images_train), '_image_train.pickle')
save_all((images_test_256, images_test), '_image_test.pickle')
save_all((n_captions_train, n_captions_test, n_captions_per_image, n_images_train, n_images_test), '_n.pickle')
save_all((captions_ids_train, captions_ids_test), '_caption.pickle')
