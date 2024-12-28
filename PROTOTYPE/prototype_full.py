from dotenv import load_dotenv
import json
import google.generativeai as genAI
from google.generativeai.protos import FunctionCall
from load_creds import load_creds
from PROTOTYPE.tools_defined import TOOLS
from PROTOTYPE.executions import EXECUTIONS

load_dotenv()

creds = load_creds()

# with open("./PROTOTYPE/conversation.jsonl", 'w') as writer:
#         writer.write('')

# ------ insert LLM 
genAI.configure(credentials=creds)
fc_model_name = 'gemini-1.5-flash'
generation_config_fc = {
    'candidate_count': 1,
    'temperature': 0,
    'top_k': 1,
    'top_p': 1,
    'max_output_tokens': 2048,
}
safety_settings = []
tool_config = {
  "function_calling_config": {
    "mode": "AUTO",
  },
}
fc_model = genAI.GenerativeModel(model_name=fc_model_name, generation_config=generation_config_fc, safety_settings=safety_settings, tools=TOOLS, tool_config=tool_config)
chat = fc_model.start_chat()

def get_fc_response(query):
    conversation_line = {}

    if not query:
        conversation_line['system'] = "Bitte eine gültige Eingabe"
        writeConv(conversation_line)
        return [{"text": conversation_line['system']}, readConv()]
    
    prompt = """
        Du bist in der Rolle eines Assistenzsystems und kannst mit den mitgegebenen Tools bestimmen, welche Funktion ein Nutzer ausführen möchte. Benutze immer das Du. Du sollst nicht sagen, welches Tool du verwendest.

        Du erhältst eine Frage und entscheidest, welches Tool dafür infrage kommt. Trifft kein anderes Tool für die Nutzeranfrage zu, wähle immer das Tool use_RAG!

        Hier die Frage: {query}
    """
    llm_prompt = prompt.format(query = query)
    response = chat.send_message(llm_prompt)
    conversation_line['user'] = query
    print(response)
    for part in response.parts:
        if part.function_call:
            fn_call = part.function_call
            print(fn_call.name)
            return [execute_function(fn_call, conversation_line, query), readConv()]
    conversation_line['system'] = response.parts[0].text
    writeConv(conversation_line)
    return [response, readConv()]

def execute_function(fn_call: FunctionCall, conversation_line: dict, query: str ):
    fn_name = fn_call.name
    fn_index = 0
    for i, tool in enumerate(EXECUTIONS):
        if tool.__name__ == fn_name:
            fn_index = i
    if fn_name == 'use_RAG':
        response = EXECUTIONS[fn_index](query)
        conversation_line['system'] = response.text
        writeConv(conversation_line)
        return response
    args = fn_call.args
    result = EXECUTIONS[fn_index](**args)
    return give_feedback(fn_name, result, conversation_line)

def give_feedback(fn_name, result, conversation_line: dict):
    result_info = f"""
    Du als Assistenzsystem hast gerade die Funktion {fn_name} ausgeführt.
    Das Ergebnis dieser Funktion ist:
    {result}

    Übermittle dem Nutzer das Ergebnis, aber gib keine Informationen zur ausgeführten Funktion.
    """
    response = chat.send_message(result_info)
    conversation_line['system'] = response.parts[0].text
    writeConv(conversation_line)
    return response

def writeConv(conv_line):
    with open("./PROTOTYPE/conversation.jsonl", 'a') as writer:
        writer.write(json.dumps(conv_line, ensure_ascii=False) + '\n')

def readConv():
    with open("./PROTOTYPE/conversation.jsonl", 'r') as reader:
        lines = reader.readlines()
        conv = []
        for line in lines:
            conv.append(json.loads(line))
        return conv