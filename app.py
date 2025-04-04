# importing from flask module the Flask class, the render_template function, the request function, url_for 
# and redirect function to redirect to home home page after updating the app database
from flask import Flask, render_template, request, url_for, redirect, flash 
# Mongoclient is used to create a mongodb client, so we can connect on the localhost 
# with the default port
from pymongo import MongoClient
# ObjectId function is used to convert the id string to an objectid that MongoDB can understand
from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_pymongo import PyMongo
# Instantiate the Flask class by creating a flask application
app = Flask(__name__)
app.secret_key = "super secret key"
# Create the mongodb client

uri = "mongodb+srv://raffafer97:raffafer97DB@cluster0.bqvzj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

#Database su cloud
app.config['MONGO_URI'] = 'mongodb+srv://raffafer97:raffafer97DB@cluster0.bqvzj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
mongo = PyMongo(app)
db = client.pharmaCenter


@app.route("/")
def home():
    return render_template('home.html') # render home page template

#funzione per la creazione di un farmaco
#nello specefico la parte front end scatena una chiamata post al backend
#recupero tutti i dati inseriti dall'utente
#vado ad inserire il farmaco a DB nella tabella farmaci
#alla fine sfruttando il tempoto render_template di Flask reindizzo alla pagina stessa passandogli tutti i farmaci a DB
@app.route("/farmaco/", methods=('GET', 'POST'))
def farmaco():
    if request.method == "POST":
        nome = request.form.get('nome')
        tipologia = request.form.get('tipologia')
        tempoElaborazione = request.form.get('tempoElaborazione')
        db.farmaci.insert_one({'nome': nome, 'tipologia': tipologia, 'tempoElaborazione': int(tempoElaborazione)})
        return redirect(url_for('farmaco'))
    all_farmaci = db.farmaci.find()    
    return render_template('farmaco.html', farmaci = all_farmaci) # reindirizzo alla pagina crea farmaco

#funzione che mi recupera tutti i farmaci disponibili a DB e li passa al front-end
#il front-end poi li gestirà sotto forma tabellare
@app.route("/farmacoView/", methods=('GET', 'POST'))
def farmacoView():
    all_farmaci = db.farmaci.find()    
    return render_template('farmacoView.html', farmaci = all_farmaci) # reindirizzo alla pagina visualizza e modifica farmaci

#funzione che recupera l'id dal front-end e tramite chiamata a db sfruttando PyMongo elimina il record
#infine rendirizza al metodo farmacoView
@app.route('/eliminaFarmaco/<oid>', methods=('POST',))
def eliminaFarmaco(oid):
    db.farmaci.delete_one({"_id": ObjectId(oid)})
    return redirect('/farmacoView/')

#funzione che dato l'id del farmaco dal front-end effettua le modifiche del farmaco
@app.route('/modificaFarmaco/<oid>', methods=('POST',))
def modificaFarmaco(oid):
    if request.method == "POST":
        nome = request.form.get('nome')
        tipologia = request.form.get('tipologia')
        tempoElaborazione = request.form.get('tempoElaborazione')
        db.farmaci.update_one({"_id" : ObjectId(oid)}, {"$set": {"nome": nome, "tipologia": tipologia, "tempoElaborazione": tempoElaborazione}})
    print(nome)
    print(tipologia)
    print(tempoElaborazione)
    return redirect('/farmacoView/')

@app.route("/parametriProduzione/", methods=('GET', 'POST'))
def parametriProduzione():
    if request.method == "POST":
        tipologia = request.form.get('tipologia')
        tempoElaborazione = request.form.get('tempoElaborazione')
        db.parametriProduzione.insert_one({'tipologia': tipologia, 'tempoElaborazione': int(tempoElaborazione)})
        return redirect(url_for('parametriProduzione'))
    all_parametriProduzione = db.parametriProduzione.find()  
    return render_template('parametriProduzione.html', parametriProduzione = all_parametriProduzione) # reindirizzo alla pagina crea parametri di produzione


@app.route("/parametriProduzioneView/", methods=('GET', 'POST'))
def parametriProduzioneView():
    all_parametriProduzioneView = db.parametriProduzione.find()    
    all_parametriManutenzioneView = db.manutenzione.find() 
    return render_template('parametriProduzioneView.html', parametriProduzione = all_parametriProduzioneView, parametriManutenzione = all_parametriManutenzioneView) # reindirizzo alla pagina visualizza e modifica parametri di produzione

@app.route('/eliminaParametriProduzione/<oid>', methods=('POST',))
def eliminaParametriProduzione(oid):
    db.parametriProduzione.delete_one({"_id": ObjectId(oid)})
    return redirect('/parametriProduzioneView/')

@app.route('/modificaParametriProduzione/<oid>', methods=('POST',))
def modificaParametriProduzione(oid):
    if request.method == "POST":
        tipologia = request.form.get('tipologia')
        tempoElaborazione = request.form.get('tempoElaborazione')
        db.parametriProduzione.update_one({"_id" : ObjectId(oid)}, {"$set": {"tipologia": tipologia, "tempoElaborazione": int(tempoElaborazione)}})
    return redirect('/parametriProduzioneView/')

@app.route("/inserisciManutenzione/", methods=('GET', 'POST'))
def inserisciManutenzione():
    if request.method == "POST":
        tipologia = request.form.get('tipologia')
        tempoElaborazione = request.form.get('tempoElaborazione')
        db.manutenzione.insert_one({'tipologia': tipologia, 'tempoElaborazione': int(tempoElaborazione), 'tempoRestante': int(tempoElaborazione)})
        return redirect(url_for('parametriProduzione'))
    all_farmaci = db.farmaci.find()  
    return render_template('parametriProduzione.html', farmaci = all_farmaci) # reindirizzo alla pagina crea parametri di produzione

@app.route('/eliminaParametriManutenzione/<oid>', methods=('POST',))
def eliminaParametriManutenzione(oid):
    db.manutenzione.delete_one({"_id": ObjectId(oid)})
    return redirect('/parametriProduzioneView/')

@app.route('/modificaParametriManutenzione/<oid>', methods=('POST',))
def modificaParametriManutenzione(oid):
    if request.method == "POST":
        tipologia = request.form.get('tipologia')
        tempoElaborazione = request.form.get('tempoElaborazione')
        db.manutenzione.update_one({"_id" : ObjectId(oid)}, {"$set": {"tipologia": tipologia, "tempoElaborazione": int(tempoElaborazione)}})
    return redirect('/parametriProduzioneView/')

@app.route('/effettuaManutenzione/<oid>', methods=('POST',))
def effettuaManutenzione(oid):
    if request.method == "POST":
        manutenzione = db.manutenzione.find_one({'_id': ObjectId(oid)})
        tempoManutenzioneReset = manutenzione['tempoElaborazione']
        db.manutenzione.update_one({"_id" : ObjectId(oid)}, {"$set": {"tempoRestante": tempoManutenzioneReset}})
    return redirect('/parametriProduzioneView/')

@app.route("/creaLotto/", methods=('GET', 'POST'))
def creaLotto():
    all_farmaci = db.farmaci.find()   
    listFarmaci = list(all_farmaci)
    for farmaco in listFarmaci:
        farmaco['quantita'] = 0
    return render_template('creaLotto.html', farmaci = listFarmaci) # reindirizzo alla pagina crea lotto

@app.route("/lottoView/", methods=('GET', 'POST'))
def lottoView():
    all_lottiView = db.lotti.find()    #
    return render_template('lottoView.html', lotti = all_lottiView) # reindirizzo alla pagina visualizzza lotti

@app.route('/eliminaLotto/<oid>', methods=('POST',))
def eliminaLotto(oid):
    db.lotti.delete_one({"_id": ObjectId(oid)})
    return redirect('/lottoView/')

@app.route('/modificaLotto/<oid>,<numeroLotto>', methods=('POST',))
def modificaLotto(oid, numeroLotto):
    if request.method == "POST":
        all_lottiView = db.lotti.find()
        lotti = list(all_lottiView)
        for lotto in lotti:
            if int(lotto['numeroLotto']) == int(numeroLotto):
                db.lotti.update_one({"_id" : ObjectId(lotto['_id'])}, {"$set": {"completato": "Completato"}})
    return redirect('/lottoView/')

@app.route('/controlli_creazione_lotto', methods=['POST'])
def controlli_creazione_lotto():
    quantitaTotale = 0
    quantitaTotaleLottoCreato = 0
    quantitaTotaleLottiInProduzione = 0
    all_farmaci = db.farmaci.find()
    listFarmaci = list(all_farmaci)
    all_parametriProduzioneView = db.parametriProduzione.find() 
    listParametriProduzione = list(all_parametriProduzioneView)
    all_manutenzioni = db.manutenzione.find()
    listManutenzioni = list(all_manutenzioni)
    all_Lotti = db.lotti.find() 
    listLotti = list(all_Lotti)
    flagError = False
    # Conversione in mappaTempiProduzione
    mappaParametriProduzione = {elemento['tipologia']: elemento['tempoElaborazione'] for elemento in listParametriProduzione}

    mappaTempiProduzione = {}
    mappaQuantitaProduzione = {}
    mappaLottiInProduzione = {}

    for farmaco in listFarmaci:
        # Recupera il valore dal form usando l'ID del farmaco
        input_name = f"quantita_{farmaco['_id']}"
        nuova_quantita = request.form.get(input_name)
        if nuova_quantita:
            farmaco['quantita'] = int(nuova_quantita)
        #Creo delle mappe che avranno come chiave la tipologia del farmaco e mi aiuteranno per l'elaborazione dei diversi controlli impostati in seguito
        #Nello specifico esse avranno come valore le seguenti informazioni:
        #mappaTempiProduzione -> Totale tempo di produzione di ciascuna tipologia di farmaco
        #mappaQuantitaProduzione -> Quantità di farmaci di ciascuna tipologia di farmaco
        if farmaco['tipologia'] not in mappaTempiProduzione:
            mappaTempiProduzione[farmaco['tipologia']] = 0  # Inizializza il valore a 0
            mappaQuantitaProduzione[farmaco['tipologia']] = 0  # Inizializza il valore a 0
        mappaTempiProduzione[farmaco['tipologia']] += int(farmaco['tempoElaborazione']) * int(farmaco['quantita'])
        mappaQuantitaProduzione[farmaco['tipologia']] += int(farmaco['quantita'])

    #mappaLottiInProduzione -> Quantità di farmaci di ciascuna tipologia di farmaco attualmente in produzione
    for lotto in listLotti:
        if lotto['completato'] == 'In corso' and lotto['tipologia'] not in mappaLottiInProduzione:
            mappaLottiInProduzione[lotto['tipologia']] = 0
        if lotto['completato'] == 'In corso':
            mappaLottiInProduzione[lotto['tipologia']] += int(lotto['tempoElaborazione'])

    #In questa parte della funzione effettuo un controllo basandomi sui tempi di produzione dei farmaci per ciascuna tipologia
    for param in mappaTempiProduzione.keys():
        quantitaTotaleLottoCreato += mappaTempiProduzione[param]
        quantitaTotaleLottiInProduzione += mappaLottiInProduzione[param]
        quantitaTotale += mappaTempiProduzione[param]
        quantitaTotale += mappaLottiInProduzione[param]
        if (mappaTempiProduzione[param] + mappaLottiInProduzione[param]) > mappaParametriProduzione[param]: 
            print("Limite superato per categoria:", param, " - Limite consentito: ", mappaParametriProduzione[param], "- Quantità inserita: ", 
                mappaTempiProduzione[param], "- Quantità lotto: ", mappaLottiInProduzione[param]) 
            errorMessage = "Limite superato per categoria: "+ str(param) + " - Quantità inserita: "+ str(mappaTempiProduzione[param]) + " - Limite consentito: "
            errorMessage += str(mappaParametriProduzione[param]) + " - Quantità attualmente in produzione: "+ str(mappaLottiInProduzione[param]) + '.'
            flash(errorMessage, 'error')
            flagError = True

    #In questa parte della funzione effettuo un controllo basandomi sui tempi di produzione generale della catena di produzione
    if quantitaTotale > mappaParametriProduzione['Generale']:
        print("Limite generale superato")
        errorMessage = 'Attenzione, il lotto che si intende creare occupa: ' + str(quantitaTotaleLottoCreato) + ' minuti. Limite generale consentito: '
        errorMessage += str(mappaParametriProduzione['Generale']) + " - Quantità attualmente in produzione: "+ str(quantitaTotaleLottiInProduzione) + '.'
        flash(errorMessage, 'error')
        flagError = True
    
    #Se il sistema non ha riscontrato nessun errore effettuo l'ultimo controllo, ovvero la manutenzione
    if flagError == False:
        for manutenzione in listManutenzioni:
            if (int(manutenzione['tempoRestante']) - quantitaTotale) < 0:
                flagError = True
                errorMessage = 'Attenzione, eseguire la seguente manutenzione: ' + str(manutenzione['tipologia']) + '.'
                flash(errorMessage, 'error')
            if (int(manutenzione['tempoRestante'])-quantitaTotale) >= 0:
                db.manutenzione.update_one({"_id" : ObjectId(manutenzione['_id'])}, {"$set": 
                                                                                {"tempoRestante": (int(manutenzione['tempoRestante'])-quantitaTotale)}})

    #Nel caso in cui il lotto ha superato tutti i controlli procedo con il suo caricamento a DB
    if flagError == False:
        allLotti = db.lotti.find()    
        listLotti = list(allLotti)
        numeroLotto = 0
        for lotto in listLotti:
            if int(lotto['numeroLotto']) > numeroLotto:
                numeroLotto = int(lotto['numeroLotto'])
        for param in mappaTempiProduzione.keys():
            db.lotti.insert_one({'numeroLotto': int(numeroLotto+1), 'tipologia': param, 'quantita': int(mappaQuantitaProduzione[param]), 
                                 'tempoElaborazione': int(mappaTempiProduzione[param]), 'completato': 'In corso'})
        flash('Lotto creato', 'success')
    return redirect('/creaLotto/')

if __name__ == "__main__":
    app.run(debug=True) 