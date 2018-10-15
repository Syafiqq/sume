from celery import shared_task


@shared_task
def simulate_sleep(length=5):
    import time
    time.sleep(length)
    return 'Finishing simulate sleep in {} second[s]'.format(length)


@shared_task(ignore_result=True)
def proceed_document(doc_id):
    import numpy
    import random
    from dlnn.Dlnn import Dlnn
    from dlnn.Dlnn import DLNN_DEFAULT_CONFIG
    dlnn = Dlnn(**DLNN_DEFAULT_CONFIG)
    # Todo : Load Dokumen by id (doc_id) [Dokumen.objects.filter(id=doc_id).first()]
    # Todo : Load pdf
    f1 = random.randint(50, 250)  # Todo : f1 = cari fitur 1 [calculate_feature_1()]
    f2 = random.randint(50, 250)  # Todo : f2 = cari fitur 2 [calculate_feature_2()]
    f3 = random.randint(50, 250)  # Todo : f3 = cari fitur 3 [calculate_feature_3()]
    f4 = random.randint(50, 250)  # Todo : f4 = cari fitur 4 [calculate_feature_4()]
    # Todo : masukkan fitur f[1..4] ke database
    network = dlnn.get_model()
    result = network.predict(numpy.array([[f1, f2, f3, f4]]), batch_size=1)
    class_data = result.argmax(axis=1)[0]
    # print("Class Data {}".format(class_data))
    # Todo : masukkan class_data sebagai hasil kelas data [mappingkan dengan kelas seharusnya] [zero based indexing]
