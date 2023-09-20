from sentence_transformers import util, SentenceTransformer
#pip install sentence-transformers -q

def similarity(word1, word2):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    copy_word1 = word1.split(' ')
    copy_word2 = word2.split(' ')
    copy_word1.append(word1)
    copy_word2.append(word2)

    # Compute cosine-similarities
    #cosine_scores = util.cos_sim(embeddings1, embeddings2)
    output = max([util.cos_sim(model.encode(i, convert_to_tensor=True),
                               model.encode(j, convert_to_tensor=True))[0][0] for i in copy_word1 for j in copy_word2])
    # Output the pairs with their score
    return output
