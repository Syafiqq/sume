import pdftotext
import nltk
from celery import shared_task
from django.shortcuts import get_object_or_404
from .models import Dokumen, Data
from spellchecker import SpellChecker
from .metode import levenshtein
from django.conf import settings
from nltk.corpus import stopwords
import re

@shared_task
def simulate_sleep(length=5):
    import time
    time.sleep(length)
    return 'Finishing simulate sleep in {} second[s]'.format(length)


@shared_task(ignore_result=True)
def proceed_document(dokumen_id):
    import numpy
    import random
    from dlnn.Dlnn import Dlnn
    from dlnn.Dlnn import DLNN_DEFAULT_CONFIG
    dlnn = Dlnn(**DLNN_DEFAULT_CONFIG)
    # Todo : Load Dokumen by id (doc_id) [Dokumen.objects.filter(id=doc_id).first()]
    dokumen = get_object_or_404(Dokumen, pk=dokumen_id)
    dokumen.state = "Process"
    dokumen.save()
    # Todo : Load pdf
    spell = SpellChecker()
    with open(dokumen.filenya.path, "rb") as f:
        pdf = pdftotext.PDF(f)
        text = "".join(pdf)

    # pecah kalimat menjadi kata kata
    text = text.lower() # Converting to lowercase
    cleanr = re.compile('<.*?>')
    sentence = re.sub(cleanr, ' ', text)        #Removing HTML tags
    sentence = re.sub(r'[?|!|\'|"|#]',r'',sentence)
    sentence = re.sub(r'[.|,|)|(|\|/]',r' ',sentence) #Removing Punctuations

    tokens = nltk.word_tokenize(sentence, preserve_line=True)

    # Fitur 1 - cek salah ketik Bahasa Indonesia
    salah_ketik_indo = 0
    salah_ketik_english = 0
    url_stopword = set(stopwords.words('indonesian'))
    url_katadasar = settings.STATIC_ROOT+'/admin/db_text/kata-dasar-all.txt'
    url_stopword_en = set(stopwords.words('english'))

    # db_stopword = open(url_stopword,"r")
    db_katadasar = open(url_katadasar,"r")
    # db_stopword_en = open(url_stopword_en,"r")

    # stopword = db_stopword.read().split('\n')
    katadasar = db_katadasar.read().split('\n')
    # stopword_en = db_stopword_en.read().split('\n')

    for token in tokens:
        salah = True
        if(token in url_stopword):
            salah = False
        else:
            if token in katadasar:
                salah = False
        if salah:
            print("kata \""+token+"\" salah")
            salah_ketik_indo += 1
        else:
            print("kata \""+token+"\" betul")

    f1 = salah_ketik_indo
    dokumen.fitur1 = f1
    dokumen.save()

    # Todo : f2 = cari fitur 2 [calculate_feature_2()]
    for token in tokens:
        salah = True
        if(token in url_stopword_en):
            salah = False
        if salah:
            print("kata \""+token+"\" salah")
            salah_ketik_english += 1
        else:
            print("kata \""+token+"\" betul")

    # misspelled = spell.unknown(tokens)
    # jumlah = len(misspelled)
    f2 = salah_ketik_english
    dokumen.fitur2 = f2
    # for word in misspelled:
    #     print("misspelled : " + word)
    #     # Get the one `most likely` answer
    #     print("most likely : " + spell.correction(word))
    #     # Get a list of `likely` options
    #     print("likely options : ")
    #     print(spell.candidates(word))

    dokumen.save()

    f3 = random.randint(50, 250)  # Todo : f3 = cari fitur 3 [calculate_feature_3()]
    dokumen.fitur3 = f3
    dokumen.save()

    f4 = random.randint(50, 250)  # Todo : f4 = cari fitur 4 [calculate_feature_4()]
    dokumen.fitur4 = f4
    dokumen.save()

    # Todo : masukkan fitur f[1..4] ke database
    network = dlnn.get_model()
    result = network.predict(numpy.array([[f1, f2, f3, f4]]), batch_size=1)
    class_data = result.argmax(axis=1)[0]
    # print("Class Data {}".format(class_data))
    # Todo : masukkan class_data sebagai hasil kelas data [mappingkan dengan kelas seharusnya] [zero based indexing]

    dokumen.kualitas = class_data
    dokumen.state = "Done"
    dokumen.save()

@shared_task(ignore_result=True)
def testing_apps(jml_pengujian, gap_data):
    f1 = [[]]
    for x in range(jml_pengujian):
        jml_uji = (100 - 50) / gap_data
        dlatih = 100
        duji = 0
        for y in range(jml_uji):
            dlatih -= gap_data
            duji += gap_data

            dataset = Data.objects.filter(is_dataset=True)
            jml_dataset = Data.objects.filter(is_dataset=True).count()
            jml_data_latih = int(jml_dataset * dlatih / 100)
            i = 0
            for data in dataset:
                i += 1
                # Todo : Load pdf
                with open(data.url_file.path, "rb") as f:
                    pdf = pdftotext.PDF(f)
                    text = "".join(pdf)

                # Todo : Normalisasi
                # pecah kalimat menjadi kata kata
                text = text.lower() # Converting to lowercase
                cleanr = re.compile('<.*?>')
                sentence = re.sub(cleanr, ' ', text)        #Removing HTML tags
                sentence = re.sub(r'[?|!|\'|"|#]',r'',sentence)
                sentence = re.sub(r'[.|,|)|(|\|/]',r' ',sentence) #Removing Punctuations

                if i <= jml_data_latih:
                    datalatih = "".join(sentence)
                else:
                    datauji = "".join(sentence)

            token_datalatih = nltk.word_tokenize(datauji, preserve_line=True)
            token_datauji = nltk.word_tokenize(datauji, preserve_line=True)

            # Fitur 1 - cek salah ketik Bahasa Indonesia
            salah_ketik_indo = 0
            salah_ketik_english = 0

            for token in token_datauji:
                salah = True
                if(token in token_datalatih):
                    salah = False
                if salah:
                    print("kata \""+token+"\" salah")
                    salah_ketik_indo += 1
                else:
                    print("kata \""+token+"\" betul")

            f1[x][y] = salah_ketik_indo

    # Todo : f2 = cari fitur 2 [calculate_feature_2()]

    for x in f1:
        for y in x:
            print(str(y))
        print("\n")
