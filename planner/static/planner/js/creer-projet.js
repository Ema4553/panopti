const container = document.getElementById("pieces-container");
const addButton = document.getElementById("add-piece");
const template = document.getElementById("empty-piece-form");
const totalForms = document.getElementById("id_form-TOTAL_FORMS");

function renumberForms() {
    const forms = container.querySelectorAll(".piece-form");

    forms.forEach((form, index) => {
        form.querySelectorAll("input, select, textarea, label").forEach((element) => {
            if (element.name) {
                element.name = element.name.replace(
                    /form-\d+-/,
                    `form-${index}-`
                );
            }

            if (element.id) {
                element.id = element.id.replace(
                    /form-\d+-/,
                    `form-${index}-`
                );
            }

            if (element.htmlFor) {
                element.htmlFor = element.htmlFor.replace(
                    /form-\d+-/,
                    `form-${index}-`
                );
            }
        });
    });

    totalForms.value = forms.length;
}

addButton.addEventListener("click", () => {
    const formIndex = Number(totalForms.value);
    const templateContent = template.innerHTML.replaceAll(
        "__prefix__",
        formIndex
    );

    container.insertAdjacentHTML("beforeend", templateContent);
    totalForms.value = formIndex + 1;
});


container.addEventListener("click", (event) => {
    if (!event.target.classList.contains("remove-piece")) {
        return;
    }

    const pieceForm = event.target.closest(".piece-form");
    
    if (!pieceForm) {
        return;
    }

    pieceForm.remove();
    renumberForms();
});