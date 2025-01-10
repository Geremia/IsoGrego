#!/usr/bin/python3

# 🎩 tip: https://stackoverflow.com/a/8897648/1429450
# cf.: https://gregobase.selapa.net/?page_id=18#comment-66831
#   and 'Top 49 chants most similar to the Requiem's gradual, sorted by cosine TF-IDF similarity of the GABC files.': https://forum.musicasacra.com/forum/discussion/comment/246225#Comment_246225

from sklearn.feature_extraction.text import TfidfVectorizer
import os, sys
import numpy as np

npz_basename = 'lower_triangular'

def generateAndSaveSimilarityMatrix():
    os.chdir('GABCs')
    text_files = os.listdir()

    documents = [open(f).read() for f in text_files]

    vectorizer = TfidfVectorizer()  # http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html#sklearn.feature_extraction.text.TfidfTransformer
    tfidf = vectorizer.fit_transform(documents)

    pairwise_similarity = tfidf * tfidf.T

    # Extract the elements of the lower triangular part including the diagonal
    lower_triangular = pairwise_similarity.toarray()[np.tril_indices(pairwise_similarity.shape[0])]
    # Save it.
    os.chdir('..')
    np.savez(npz_basename, lower_triangular)

def loadNpyFilesIntoSHM():
    from multiprocessing import shared_memory, resource_tracker  # https://docs.python.org/3.9/library/multiprocessing.shared_memory.html#multiprocessing.shared_memory.SharedMemory.size

    npzfile = np.load(npz_basename+'.npz')
    loaded_matrix = npzfile['arr_0.npy']
    shm = shared_memory.SharedMemory(create=True, size=loaded_matrix.nbytes)
    # Copy the data into the shared memory block
    shared_array = np.ndarray(loaded_matrix.shape, dtype=loaded_matrix.dtype, buffer=shm.buf)
    np.copyto(shared_array, loaded_matrix)

    with open('shm.name.txt', 'w') as f:
        print('shm name:', shm.name)
        print('matrix.shape:', loaded_matrix.shape)
        print(shm.name, file=f)

    print('Hit enter to exit and cleanup shared memory.')
    sys.stdin.readline()

    #cleanup
    shm.close()
    shm.unlink()

if not os.path.exists(npz_basename+'.npz'):
    print('Generating similarity matrix and saving it as ' + npz_basename + '.npz…')
    generateAndSaveSimilarityMatrix()

print('Loading ' + npz_basename + '.npz into shared memory (shm)…')
loadNpyFilesIntoSHM()
