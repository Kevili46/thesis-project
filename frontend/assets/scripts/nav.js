const navItems = {
  "PROTOTYPE": "/pt-full",
  "Prototype RAG": "/",
  "Prototype FT": "/pt-ft",
  "Dataset Creator": "/dataset-creator",
  "Converting Files": "/convert-txt",
};

const nav = document.querySelector("#main-nav ul");

for (const [key, value] of Object.entries(navItems)) {
  const li = document.createElement("li");
  const a = document.createElement("a");
  a.href = value;
  a.innerHTML = key;
  if (window.location.pathname == value) {
    a.setAttribute("active", "");
  }
  li.appendChild(a);
  nav.appendChild(li);
}

const forms = document.querySelectorAll("form");

for (let form of forms) {
  form.addEventListener("submit", () => {
    if (window.location.href.includes("pt-full")) {
      return
    }
    document.getElementById("loader").classList.add("loading");
  });
}
