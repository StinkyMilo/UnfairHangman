import matplotlib as mpl
from matplotlib import pyplot as plt
import json
data = json.loads(open("word_data_652.json","r").read())
# This has most English words and graphs the number of words that took each number of incorrect guesses.
xs = []
ys = []
# Haha I'm fancy I use the word datum
for datum in data:
    if data[datum] not in xs:
        xs.append(data[datum])
        ys.append(1)
    else:
        ys[xs.index(data[datum])]+=1
print(xs)
print(ys)
plt.bar(xs,ys)
plt.show()
# The two hardest words were vox and tres - 18 guesses
# Almost as hard were wuzzy, wuzzer, wim, luv, jazz, ior, mixy, rax, 
