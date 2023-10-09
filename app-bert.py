from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = [
            "Niharika is from Gurgaon.",
            "Niharika is not from Gurgaon."
            ]

embeddings = model.encode(sentences)

cos_sim = util.cos_sim(embeddings, embeddings)

all_sentence_combinations = []
for i in range(len(cos_sim)-1):
    for j in range(i+1, len(cos_sim)):
        all_sentence_combinations.append([cos_sim[i][j], i, j])

all_sentence_combinations = sorted(all_sentence_combinations, key=lambda x: x[0], reverse=True)

for score, i, j in all_sentence_combinations[:]:
    print("{} \t {} \t {:.4f}".format(sentences[i], sentences[j], cos_sim[i][j]))