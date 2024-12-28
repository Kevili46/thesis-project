const suggsDiv = document.getElementsByClassName("suggestions")[0];
const textArea = document.getElementById("question");

const suggs = [
  "Welche Möglichkeiten gibt es, ein Datenobjekt zu verändern?",
  "Wann ist Tag der Deutschen Einheit?",
  "Was ist ein Datenobjekt?",
  "Wie kann ich einen Link testen?",
  "Für wwas snd Sektonen?",
  "Wie erstelle ich ein Element?",
  "Wie heißen die genauen Inhaltstypen?",
  "Wie erstelle ich ein Datenobjekt?",
  "Brauche ich eine Vorlage, um ein Datenobjekt zu erstellen?",
  "Kennst du den Unterschied zwischen Datenobjekten und Datentypen?",
  "Wie erstelle ich ein Datenobjekt, das auf einem Datentypen basiert?",
  "Erstelle mir einen Datentyp für ein Produkt mit Name, Preis, Bild und Kategorie",
];

for (let i = 0; i < suggs.length; i++) {
  let suggP = createSugg(suggs[i]);
  suggsDiv.appendChild(suggP);
}

function createSugg(q) {
  const sugg = document.createElement("p");
  sugg.innerHTML = q;
  sugg.addEventListener("click", () => {
    textArea.value = q;
    console.log();
  });
  return sugg;
}
