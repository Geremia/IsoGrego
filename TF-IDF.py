#!/usr/bin/python3

# 🎩 tip: https://stackoverflow.com/a/8897648/1429450
# cf.: https://gregobase.selapa.net/?page_id=18#comment-66831
#   and "Top 49 chants most similar to the Requiem's gradual, sorted by cosine TF-IDF similarity of the GABC files.": https://forum.musicasacra.com/forum/discussion/comment/246225#Comment_246225

# NEED TO RUN load.py FIRST

import sys
if len(sys.argv) != 4:
    print("Two args required: similarity matrix shared memory ID, GregoBase ID, number of results")
    sys.exit(1)

import glob, re
import numpy as np

text_files = glob.glob("GABCs/*.gabc")
documents = [open(f).read() for f in text_files]

from multiprocessing import shared_memory, resource_tracker
existing_shm = shared_memory.SharedMemory(name=sys.argv[1])
resource_tracker.unregister(existing_shm._name, 'shared_memory') # https://stackoverflow.com/a/64916180/1429450
data = np.ndarray((19315, 19315), dtype=np.float64, buffer=existing_shm.buf)

#top n similar files for document
filename=sys.argv[2]+'.gabc'
n = int(sys.argv[3])
data_idx = text_files.index('GABCs/'+filename)
topn = np.argsort(data[data_idx])[::-1][:n+1]
for i in topn:
    gabc = documents[i]
    name = re.findall("name:[^;]*", gabc)[0]
    name = name.replace("name:", "")
    gabc_id = re.sub('GABCs/','',text_files[i])
    gabc_id = int(re.sub(".gabc", "", gabc_id))
    print('<li><details><summary><a href="?id=%d">🔍</a> '%(gabc_id)+str(round(data[data_idx][i]*100))+'% '+'%s</summary><a href="https://gregobase.selapa.net/chant.php?id=%d" target="_blank"><img src="https://gregobase.selapa.net/chant_img.php?id=%d" alt="%s" loading="lazy"/></a></details></li>'%(name, gabc_id, gabc_id, name))

