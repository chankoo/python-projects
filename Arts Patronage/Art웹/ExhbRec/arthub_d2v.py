import pandas as pd
import numpy as np

from gensim.models.ldamodel import LdaModel
from gensim.models.doc2vec import Doc2Vec

import pickle
import re

western_data = pd.read_csv('static/data/western_preprocessed.csv')

with open('static/data/nouns_refined_final.dic','rb') as file:
    dic = pickle.load(file)
ldamodel = LdaModel.load('static/data/lda_exhb_10.model')
d2vmodel = Doc2Vec.load('static/data/d2v_exhb_100.model')


def lda_sim(query_tokens,data_final):
    query_bow = dic.doc2bow(query_tokens)
    query_topics = ldamodel.get_document_topics(query_bow)
    query_topic_weights = [(query_topic[0], query_topic[1] / np.max(query_topics, axis=0)[1]) for query_topic in
                           query_topics]
    query_topic_weights_dic = dict.fromkeys(range(10))
    query_topic_weights_dic.fromkeys(range(10))
    for topic, weight in query_topic_weights:
        query_topic_weights_dic[topic] = weight

    new_vector = d2vmodel.infer_vector(query_tokens, steps=100)
    sims = d2vmodel.docvecs.most_similar([new_vector], topn=30)

    recs = []
    for sim in sims:
        doc_topics = []
        for topic in re.sub('[^0-9]', '', data_final.iloc[sim[0], 9]):  # ex '89'
            doc_topics.append(int(topic))
        if doc_topics == []:  # topic 지정 안된 doc의 경우
            recs.append((sim[0], sim[1]))  # sim을 그대로 저장
            continue
        else:
            tmp = []
            for doc_topic in doc_topics:  # topic 지정된 doc의 경우
                weight = query_topic_weights_dic[doc_topic]
                if weight == None:
                    weight = 0

                tmp.append(sim[1] + sim[1] * weight * 0.3)  # 가중치 더해 저장

            recs.append((sim[0], np.max(tmp)))

    result = {}
    for tpl in sorted(recs, key=lambda tpl: tpl[1], reverse=True)[:12]:
        exhbn_id = tpl[0]
        result[exhbn_id] = tpl[1]
    return result


