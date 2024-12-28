from flask import Flask, render_template, request, session, redirect
from rag_test import getResponse
from dataset_creator import createSet, writeSetToFile, clearFile, convertTxtToJSONL, convertTxtToCSV, createFTSet, writeFTSetToFile, convertFTSetsToCSV, DATAFILE, DATAFILE_FT, DATAFILE_CSV, SRC_FILE
from write_dataobjects_in_file import fetch_convert
from upload_doc import upload_doc
from ft_test_colorchange import get_ft_response
from PROTOTYPE.prototype_full import get_fc_response

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/assets')
app.secret_key = 'A-B-C-D'

# -------------- PROTOYPE RAG ---------------
@app.route('/', methods=['GET', 'POST'])
def home():
    if not session.get('conlog'):
        session['conlog'] = ''

    if request.method == 'POST':
        data = request.form.get('question')
        res = getResponse(data, session['conlog'])
        result = res[0]
        prompt = res[1]
        context = res[2]
        session['conlog'] += ''
        return render_template('prototype_rag.html', result=result, question=data, log='', prompt=prompt, context = context)
    return render_template('prototype_rag.html')

@app.route('/clear-session', methods=['GET'])
def clear_session():
    session['conlog'] = ''
    return redirect('/')

# -------------- PROTOYPE FULL ---------------
@app.route('/pt-full', methods=['GET', 'POST'])
def pt_full():
    if request.method == 'POST':
        data = request.form.get('question')
        res = get_fc_response(data)
        return render_template('prototype_full.html', result=res[0], conversation=res[1], question=data)
    return render_template('prototype_full.html')

# -------------- PROTOYPE FT ---------------
@app.route('/pt-ft', methods=['GET', 'POST'])
def pt_ft():
    if request.method == 'POST':
        data = request.form.get('question')
        res = get_ft_response(data)
        return render_template('prototype_ft.html', result=res[0], question=data)
    return render_template('prototype_ft.html')


# -------------- DATASET CREATOR ---------------

@app.route('/dataset-creator', methods=['GET', 'POST'])
def dataset_creator():
    if not 'full_set' in session:
        session['full_set'] = ''
    return render_template('dataset_creator.html', full_set=session['full_set'], file=DATAFILE, file_ft=DATAFILE_FT)

@app.route('/dataset-creator-sum', methods=['POST'])
def dataset_creator_sum():
    if request.method == 'POST':
        sys = request.form.get('system')
        user = request.form.get('user')
        model = request.form.get('model')
        if user == '' or model == '':
            session['notice'] = 'NO SET ADDED'
            return render_template('dataset_creator.html', file=DATAFILE)
        full_set = createSet(sys, user, model)
        writeSetToFile(full_set, DATAFILE)
        session['notice'] = 'SET ADDED TO ' + DATAFILE
        return redirect('/dataset-creator')
    
@app.route('/dataset-creator-io', methods=['POST'])
def dataset_creator_io():
    if request.method == 'POST':
        input = request.form.get('input')
        action = request.form.get('action')
        output = request.form.get('output')
        if input == '' or (action == 'True' and output == ''):
            session['notice'] = 'NO SET ADDED'
            return render_template('dataset_creator.html', file=DATAFILE_FT)
        set = createFTSet(input, action, output)
        writeFTSetToFile(set)
        session['notice'] = 'SET ADDED TO ' + DATAFILE_FT
        return redirect('/dataset-creator')


# -------------- CONVERT TXT ---------------

@app.route('/fetch-convert', methods=['GET'])
def fetch_and_convert():
    fetch_convert()
    session['notice'] = 'FETCHED & CONVERTED TO ' + SRC_FILE + ' AND ' + SRC_FILE
    return redirect('/convert-txt')

@app.route('/upload-doc', methods=['GET'])
def upload_doc_to_db():
    upload_doc()
    session['notice'] = 'UPLOADED ' + SRC_FILE + ' AS EMBEDDINGS TO VECTORBASE'
    return redirect('/convert-txt')

@app.route('/convert-txt', methods=['GET'])
def convert_txt():
    return render_template('convert_txt.html', src=SRC_FILE, file_jsonl=DATAFILE, file_csv=DATAFILE_CSV, src2=SRC_FILE)

@app.route('/converting-jsonl', methods=['GET'])
def converting_jsonl():
    convertTxtToJSONL(SRC_FILE, DATAFILE)
    session['notice'] = 'CONVERTED ' + SRC_FILE + ' TO ' + DATAFILE
    return redirect('/convert-txt')

@app.route('/delete-trainingdata-jsonl', methods=['GET'])
def delete_data_jsonl():
    clearFile(DATAFILE)
    session['notice'] = 'FILE CLEARED (' + DATAFILE + ')'
    return redirect('/convert-txt')

@app.route('/converting-csv', methods=['GET'])
def converting_csv():
    convertTxtToCSV(SRC_FILE, DATAFILE_CSV)
    convertFTSetsToCSV()
    session['notice'] = 'CONVERTED ' + SRC_FILE + ' TO ' + DATAFILE_CSV
    return redirect('/convert-txt')

@app.route('/delete-trainingdata-csv', methods=['GET'])
def delete_data_csv():
    clearFile(DATAFILE_CSV)
    session['notice'] = 'FILE CLEARED (' + DATAFILE_CSV + ')'
    return redirect('/convert-txt')


if __name__ == '__main__':
    # host='192.168.178.48'
    host = '127.0.0.1'
    app.run(host=host, port=8000, debug=True)
