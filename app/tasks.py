import pdftotext
import nltk
from celery import shared_task
from django.shortcuts import get_object_or_404
from .models import Dokumen
from spellchecker import SpellChecker


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

    f1 = random.randint(50, 250)  # Todo : f1 = cari fitur 1 [calculate_feature_1()]
    dokumen.fitur1 = f1
    dokumen.save()

    # Todo : f2 = cari fitur 2 [calculate_feature_2()]
    tokens = nltk.word_tokenize(text, preserve_line=True)
    misspelled = spell.unknown(tokens)
    jumlah = len(misspelled)
    dokumen.fitur2 = jumlah
    f2 = jumlah
    for word in misspelled:
        print("misspelled : " + word)
        # Get the one `most likely` answer
        print("most likely : " + spell.correction(word))
        # Get a list of `likely` options
        print("likely options : ")
        print(spell.candidates(word))

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
