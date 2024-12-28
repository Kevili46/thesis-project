import google.generativeai as genai
import textwrap

create_dataobject_defined = genai.protos.FunctionDeclaration(
    name = 'create_dataobject',
    description = textwrap.dedent("""\
        Erstellt ein Datenobjekt mit einer definierten Struktur. Ganz wichtig: prüfe erst mit dem Tool get_dataobjects, ob bereits eines mit diesem Namen exisitiert, da der Name einzigartig sein muss!
                                  
        Die Property 'content' muss unbedingt als JSON-String formuliert sein!
        Wenn für den Slug keine Angabe besteht, dann wird auch hier die Angabe für den Namen eingetragen!
        """),
    parameters = genai.protos.Schema(
        type = genai.protos.Type.OBJECT,
        properties = {
            'name':  genai.protos.Schema(type=genai.protos.Type.STRING),
            'public':  genai.protos.Schema(type=genai.protos.Type.BOOLEAN),
            'slug': genai.protos.Schema(type=genai.protos.Type.STRING),
            'content': genai.protos.Schema(type = genai.protos.Type.STRING),
            'metaDescription': genai.protos.Schema(type=genai.protos.Type.STRING),
        },
    required=['name', 'public', 'content']
    )
)

def create_dataobject(name:str, public: bool, content:str, slug:str, **kwargs) -> dict:
    """ Erstellt ein Datenobjekt und prüft erst, ob bereits eines mit diesem Namen exisitiert, da der Name einzigartig sein muss.
    Einige der Parameter sind unbedingt notwendig!

    Args:
        name (str, required): einzigartiger Name des Datenobjekts
        public (bool, required): Datenobjektsoll öffentlich sein oder nicht
        slug (str, required): slug hinter einer Domain, um eine einzigartige URL zu formen. Wenn keine gestellt wird, dann wird immer der Wert von 'name' verwendet
        content (str, required): ein JSON-String, das die gewünschten Inhalte des Datenobjekts enthält. Der content string wird in ein JSON-Format gebracht, das für jedes Element ein Key-Value-Paar enthält.
        metaDescription (str, optional): eine kurze Beschreibung des Inhalts des Datenobjekts.
        
    Returns:
        Ein dictionary, das alle Args beinhaltet
    """
    return {
        "name": name,
        "public": public,
        "slug": slug,
        "content": content,
        "metaDescription": kwargs.get("metaDesription", None)
    }

def edit_dataobject(dataobject: str, **kwargs):
    """ Ändert eine oder mehrere Werte eines Datenobjekts

    Args:
        dataobject (str, required): der Name des Datenobjekts, an dem Veränderungen vorgenommen werden
        name (str, optional): Name des Datenobjekts
        public (bool, optional): Datenobjektsoll öffentlich sein oder nicht
        slug (str, optional): slug hinter einer Domain, um eine einzigartige URL zu formen. Wenn keine angegeben ist, dann den Wert von 'name' verwenden
        content (str, optional): ein JSON-String, das die gewünschten Inhalte des Datenobjekts enthält. Der content string wird von dir in ein JSON-Format gebracht, das für jedes Element ein Key-Value-Paar enthält.
        metaDescription (str, optional): eine kurze Beschreibung des Inhalts des Datenobjekts.
        
    Returns:
        Ein dictionary, das die veränderten Werte beinhaltet
    """
    changes = {
        "dataobject": dataobject,
        "name": kwargs.get("name"),
        "public": kwargs.get("public"),
        "slug": kwargs.get("slug"),
        "content": kwargs.get("content"),
        "metaDescription": kwargs.get("metaDesription", None)
    }

    return changes

def delete_dataobject(name: str):
    """ Löscht ein Datenobjekt

    Args:
        dataobject (str, required): der Name des Datenobjekts, das gelöscht werden soll
    
    Returns:
        Den Namen des zu löschenden Datenobjekt
    """

    return {
        "name": name
    }

def get_dataobjects():
    """ Gibt eine Liste von Namen bereits bestehender Datenobjekte aus """


def use_RAG():
    """ Diese Funktion wird ausnahmslos dann ausgeführt, wenn andere Funktionen nicht in Frage kommen. Dann wird durch diese Funktion ein RAG-System angesteuert.

    """

TOOLS = [create_dataobject_defined, edit_dataobject, delete_dataobject, get_dataobjects, use_RAG]