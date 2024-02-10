import spacy
import joblib
from spacy import displacy
import pickle
import pprint

nlp = joblib.load("saved/stock_news/financial_analysis_nlp.joblib")
sentence_pipeline = joblib.load("saved/stock_news/sentence_pipeline.joblib")

def load_entities():
    entity_map = None

    with open("saved/stock_news/entity_map.pkl", "rb") as file:
        entity_map = pickle.load(file)

    return entity_map

def num_map(x):
    if(x == 'negative'):
        return -1
    elif(x == 'neutral'):
        return 0
    elif(x == 'positive'):
        return 1
    else:
        return 0

def entity_classify(text):
    doc = nlp(text)
    html = displacy.render(doc, style="ent", page=True)
    entity_map = load_entities()
    relevant_entities_keys = set()
    sentences = []
    for sent in doc.sents:
        if(sent.ents):
            sentences.append({
                "entities": sent.ents,
                "text": sent.text
            })
    classes = list(map(num_map, sentence_pipeline.predict(list(map(lambda x: x["text"], sentences)))))
    for i in range(len(classes)):
        sentences[i]["class"] = classes[i]

    # Adding to relevant_entities list 
    for sentence in sentences:
        for ent in sentence["entities"]:
            relevant_entities_keys.add(ent.text)
            if("highlights" not in entity_map[ent.text]):
                entity_map[ent.text]["highlights"] = []
            entity_map[ent.text]["highlights"].append(sentence)

    # Retrieving all entity objs 
    relevant_entities = []
    for key in relevant_entities_keys:
        relevant_entities.append(entity_map[key])
        total_class = 0
        for sentence in entity_map[key]["highlights"]:
            total_class += sentence["class"]
        
        entity_map[key]["sentiment"] = total_class/len(entity_map[key]["highlights"])
    pprint.pprint(relevant_entities)

