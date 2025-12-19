#!/usr/bin/python3

# 🎩 tip: https://stackoverflow.com/a/8897648/1429450
# cf.: https://gregobase.selapa.net/?page_id=18#comment-66831
#   and 'Top 49 chants most similar to the Requiem's gradual, sorted by cosine TF-IDF similarity of the GABC files.': https://forum.musicasacra.com/forum/discussion/comment/246225#Comment_246225

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from pathlib import Path

npy_basename = 'lower_triangular'
npy_path = Path(f'{npy_basename}.npy')

def generateAndSaveSimilarityMatrix():
    text_files = [f for f in Path('./GABCs').glob('*.gabc')]

    documents = [f.read_text() for f in text_files]

    vectorizer = TfidfVectorizer()  # http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html#sklearn.feature_extraction.text.TfidfTransformer
    tfidf = vectorizer.fit_transform(documents)

    pairwise_similarity = tfidf * tfidf.T

    # Extract the elements of the lower triangular part including the diagonal
    lower_triangular = pairwise_similarity.toarray()[np.tril_indices(pairwise_similarity.shape[0])]
    # Save it.
    np.save(npy_path, lower_triangular)

if not npy_path.exists():
    print(f'Generating similarity matrix and saving it as {npy_path}…')
    generateAndSaveSimilarityMatrix()
