#!/usr/bin/python3

# 🎩 tip: https://stackoverflow.com/a/8897648/1429450
# cf.: https://gregobase.selapa.net/?page_id=18#comment-66831
#   and "Top 49 chants most similar to the Requiem's gradual, sorted by cosine TF-IDF similarity of the GABC files.": https://forum.musicasacra.com/forum/discussion/comment/246225#Comment_246225


from sklearn.feature_extraction.text import TfidfVectorizer
import glob, re, sys
import numpy as np

text_files = glob.glob("GABCs/*.gabc")
documents = [open(f).read() for f in text_files]

# http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html#sklearn.feature_extraction.text.TfidfTransformer
vectorizer = TfidfVectorizer()
#feature_names = vectorizer.get_feature_names_out()
tfidf = vectorizer.fit_transform(documents)

pairwise_similarity = tfidf * tfidf.T

data = pairwise_similarity.toarray()
#np.fill_diagonal(data, np.nan)

# https://docs.python.org/3.9/library/multiprocessing.shared_memory.html#multiprocessing.shared_memory.SharedMemory.size
from multiprocessing import shared_memory
shm = shared_memory.SharedMemory(create=True, size=data.nbytes)
b = np.ndarray(data.shape, dtype=data.dtype, buffer=shm.buf)
b[:] = data[:]

with open('shm.name.txt', 'w') as f:
    print(shm.name, file=f)

print("Hit enter to exit and cleanup shared memory.")
sys.stdin.readline()

#cleanup
del b # Unnecessary; merely emphasizing the array is no longer used
shm.close()
shm.unlink()
