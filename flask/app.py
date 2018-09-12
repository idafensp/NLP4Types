#https://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972

from flask import Flask, render_template, request, current_app
app = Flask(__name__)

import logging as logger
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


import utils.args as uarg
import utils.features as feat
import utils.preprocess as pp
import utils.spotlight as sl
import utils.stringutils as su

import json
import pickle
import pymongo
from pymongo import MongoClient

classifier = None
confidence = 0
support = 0
slservice = None
mgclient = None
modelname = ""
collectionname = ""

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/process',methods=['POST'])
def process():
    _description = request.form['description']

    logger.info("Got description=%s" % _description)

    ne_desc = ""
    if use_ne:
        # GET NER
        logger.info("Getting NEs...")
        ne_desc = su.to_string(slservice.get_annotations(_description, confidence, support, True), " ")
        logger.info("Got NEs=%s" % ne_desc)

    logger.info("Getting Preprocess...")
    pp_desc = pp.process_text(_description, use_sw, use_lemma, use_stemm)
    logger.info("Got Preprocess=%s" % pp_desc)

    _text = pp_desc + " " + ne_desc

    logger.info("Getting Vec data...")
    prediction_data = vectorizer.transform([_text])
    logger.info("Got Vec data")


    logger.info("Getting Predictions...")
    predictions = []
    try:
        predictions = classifier.predict(prediction_data)
    except Exception as e:
        logger.error('Failed to classify: ' + str(e))
        logger.error('Exiting')
        return ""
    logger.info("*******\n\nGot Predictions=%s\n\n******" % predictions)


    res_data = {}
    res_data['predictions'] = predictions[0]
    #res_data['predictions_list'] = predictions
    res_data['processed_text'] = pp_desc
    res_data['raw_text'] = _description
    res_data['named_entities'] = ne_desc
    res_data['confidence'] = confidence
    res_data['support'] = support
    res_data['use_sw'] = use_sw
    res_data['use_lemma'] = use_lemma
    res_data['use_stemm'] = use_stemm
    res_data['use_ne'] = use_ne
    res_data['dbonly'] = dbonly
    res_data['model'] = modelname


    json_data = json.dumps(res_data)


    return json_data

@app.route('/feedback',methods=['POST'])
def feedback():

    logger.info("Getting feedback")
    _debug = request.get_json()

    # http://api.mongodb.com/python/current/tutorial.html

    # get mongo db
    db = mgclient.nlp4types
    #get collection
    collection = db[collectionname] # db.feedback

    feed_id = ""
    try:
        feed_id = collection.insert_one(_debug).inserted_id
    except Exception as e:
        logger.error('Failed to insert in mongo: ' + str(e))
        logger.error('Exiting')
        return


    logger.info("Got id=%s, feedback=%s, _debug=%s" %  (feed_id, _debug['feedback'], _debug))

    # empty feed id -> error
    if not feed_id:
        return "error"

    return "success"


if __name__ == "__main__":


    ps = uarg.Args()
    args = ps.get_args()

    logfile = 'log_flask.log'
    if args.log:
        logfile = args.log

    import logging.config
    logging.basicConfig(filename=logfile, format='%(asctime)s %(levelname)s %(message)s',
                        level=logger.DEBUG)

    file_classifier = args.classifier
    file_vectorizer = args.vect

    # un-pickle classifier
    logger.debug("Loading classifier from %s" % file_classifier)
    classifier = joblib.load(file_classifier)
    logger.debug("Classifier loaded from %s" % file_classifier)

    # un-pickle vec_data
    logger.debug("Loading vecrtorizer from %s" % file_vectorizer)
    vectorizer = pickle.load(open(file_vectorizer, "rb"))
    logger.debug("Vecrtorizer loaded from %s" % file_classifier)

    # NER parameters
    confidence = args.confidence
    support = args.support

    # Preprocess parameters
    use_sw = args.sw
    use_lemma = args.lemma
    use_stemm = args.stemm
    use_ne = args.ner
    dbonly = args.dbonly


    # feedback data
    modelname = args.model
    collectionname = args.collection

    logger.info("**** Arguments *** \n %s\n\n **********" % args)

    # Create the NER service
    slservice = sl.SpotLightNER()

    mgclient = MongoClient()

    app.run(host= '0.0.0.0', debug=True)

