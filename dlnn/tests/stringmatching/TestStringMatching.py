import re

import numpy as np
import pandas as pd
import sparse_dot_topn.sparse_dot_topn as ct
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from nltk import word_tokenize
from scipy.sparse import csr_matrix

from dlnn.tests.ml.testcase import TestCase


def awesome_cossim_top(A, B, ntop, lower_bound=0):
    # force A and B as a CSR matrix.
    # If they have already been CSR, there is no overhead
    A = A.tocsr()
    B = B.tocsr()
    M, _ = A.shape
    _, N = B.shape

    idx_dtype = np.int32

    nnz_max = M * ntop

    indptr = np.zeros(M + 1, dtype=idx_dtype)
    indices = np.zeros(nnz_max, dtype=idx_dtype)
    data = np.zeros(nnz_max, dtype=A.dtype)

    ct.sparse_dot_topn(
        M, N, np.asarray(A.indptr, dtype=idx_dtype),
        np.asarray(A.indices, dtype=idx_dtype),
        A.data,
        np.asarray(B.indptr, dtype=idx_dtype),
        np.asarray(B.indices, dtype=idx_dtype),
        B.data,
        ntop,
        lower_bound,
        indptr, indices, data)

    return csr_matrix((data, indices, indptr), shape=(M, N))


def get_matches_df(sparse_matrix, name_vector, top=100):
    non_zeros = sparse_matrix.nonzero()

    sparserows = non_zeros[0]
    sparsecols = non_zeros[1]

    nr_matches = min(len(name_vector), sparsecols.size, sparserows.size)
    print(nr_matches)

    left_side = np.empty([nr_matches], dtype=object)
    right_side = np.empty([nr_matches], dtype=object)
    similairity = np.zeros(nr_matches)

    for index in range(0, nr_matches):
        left_side[index] = name_vector[sparserows[index]]
        right_side[index] = name_vector[sparsecols[index]]
        similairity[index] = sparse_matrix.data[index]

    return pd.DataFrame({'left_side': left_side,
                         'right_side': right_side,
                         'similairity': similairity})


def ngrams(string, n=3):
    string = re.sub(r'[,-./]|\sBD', r'', string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]


def tokenize(d1):
    # split into words
    from nltk.tokenize import word_tokenize
    tokens = word_tokenize(d1)
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove punctuation from each word
    import string
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # filter out stop words
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]

    # stemming of words
    from nltk.stem.porter import PorterStemmer
    porter = PorterStemmer()
    stemmed = [porter.stem(word) for word in words]
    return stemmed


def make_words(doc, x):
    res = [' '.join(doc[y - x:y]) for y in range(x, len(doc) + x, x)]
    return res


class TestStringMatching(TestCase):
    def test_string_matching(self):
        d1 = """With Django, you can take Web applications from concept to launch in a matter
of hours. Django takes care of much of the hassle of Web development, so you
can focus on writing your app without needing to reinvent the wheel. It’s free
and open source."""

        d2 = """Django includes dozens of extras you can use to handle common Web
development tasks. Django takes care of user authentication, content
administration, site maps, RSS feeds, and many more tasks — right out of the
box."""

        d1t = tokenize(d1)
        d2t = tokenize(d2)

        d1tt = make_words(d1t, 3)
        d2tt = make_words(d2t, 3)
        print(d1tt, d2tt)
        from sklearn.feature_extraction.text import TfidfVectorizer

        vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams)
        tf_idf_matrix = vectorizer.fit_transform(d2tt)
        print(tf_idf_matrix)

        import time
        t1 = time.time()
        matches = awesome_cossim_top(tf_idf_matrix, tf_idf_matrix.transpose(), 10000)
        t = time.time() - t1
        print("SELFTIMED:", t)
        matches_df = get_matches_df(matches, d1tt)
        print(matches_df.sort_values(['similairity'], ascending=False))

    def test_doc_2_vec_train(self):
        d1 = """With Django, you can take Web applications from concept to launch in a matter
    of hours. Django takes care of much of the hassle of Web development, so you
    can focus on writing your app without needing to reinvent the wheel. It’s free
    and open source."""

        d1t = tokenize(d1)
        d1tt = make_words(d1t, 3)
        tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(d1tt)]
        max_epochs = 1000
        vec_size = 200
        alpha = 0.025
        model = Doc2Vec(size=vec_size,
                        alpha=alpha,
                        min_alpha=0.00025,
                        min_count=1,
                        dbow_words=1,
                        dm=1)
        model.build_vocab(tagged_data)
        for epoch in range(max_epochs):
            print('iteration {0}'.format(epoch))
            model.train(tagged_data,
                        total_examples=model.corpus_count,
                        epochs=model.iter)
            model.alpha -= 0.0002
            model.min_alpha = model.alpha
        model.save("d2v.model")

    def test_doc_2_vec_test(self):
        d1 = """With Django, you can take Web applications from concept to launch in a matter
        of hours. Django takes care of much of the hassle of Web development, so you
        can focus on writing your app without needing to reinvent the wheel. It’s free
        and open source."""

        d2 = """Django includes dozens of extras you can use to handle common Web
        development tasks. Django takes care of user authentication, content
        administration, site maps, RSS feeds, and many more tasks — right out of the
        box. Django includes dozens of extras you can use to handle common Web
development tasks. Django takes care of user authentication, content
administration, site maps, RSS feeds, and many more tasks — right out of the
box."""

        d1t = tokenize(d1)
        d2t = tokenize(d2)

        d1tt = make_words(d1t, 3)
        d2tt = make_words(d2t, 3)

        model = Doc2Vec.load("d2v.model")
        # to find the vector of a document which is not in training data
        # test_data = word_tokenize(d1tt[0].lower())
        # v1 = model.infer_vector(test_data)
        # print("V1_infer", v1)

        # tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(d1tt)]
        # for tag in tagged_data:
        #    print(tag)
        #    v1 = model.infer_vector(tagged_data)
        # print("V1_infer", v1)

        # to find most similar doc using tags
        # similar_doc = model.docvecs.most_similar([model.infer_vector(test_data)])

        # test_data = word_tokenize(d1tt[0].lower())
        # similar_doc = model.docvecs.most_similar(positive=[model.infer_vector('testing'.split(' '))])
        # print(list(filter(lambda x: x[1], similar_doc)))

        # to find vector of doc in training data using tags or in other words, printing the vector of document at index 1 in training data
        # print(model.docvecs['1'])
        count = 0
        for x in d2tt:
            sim = model.docvecs.most_similar(positive=[model.infer_vector(word_tokenize(x.lower()))])
            xy = max(sim, key=lambda z: z[1])
            count += 1 if xy[1] > 0.5 else 0
        print('%d of %d' % (count, len(d2tt)))
