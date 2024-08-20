document.addEventListener("DOMContentLoaded", function () {
    const submitButton = document.getElementById("submitButton");
    const errorMessage = document.getElementById("error-message");

    const requiredInputs = document.querySelectorAll("input[required], select[required]");

    requiredInputs.forEach((input) => {
        input.addEventListener("input", validateInput);
    });

    function validateInput(event) {
        const input = event.target;
        if (input.type === "radio") {
            const radios = document.querySelectorAll(`input[name="${input.name}"]`);
            let radioValid = false;
            radios.forEach((radio) => {
                if (radio.checked) {
                    radioValid = true;
                }
            });
            if (radioValid) {
                radios.forEach((radio) => {
                    radio.classList.remove("invalid");
                    radio.classList.add("valid");
                });
            } else {
                radios.forEach((radio) => {
                    radio.classList.remove("valid");
                    radio.classList.add("invalid");
                });
            }
        } else {
            if (input.value.trim()) {
                input.classList.remove("invalid");
                input.classList.add("valid");
            } else {
                input.classList.remove("valid");
                input.classList.add("invalid");
            }
        }

        checkFormValidity();
    }

    function checkFormValidity() {
        let allValid = true;

        requiredInputs.forEach((input) => {
            if ((input.type === "radio" && !document.querySelector(`input[name="${input.name}"]:checked`)) ||
                (input.type !== "radio" && !input.value.trim())) {
                allValid = false;
            }
        });

        if (allValid) {
            submitButton.disabled = false;
            errorMessage.classList.remove("visible");
        } else {
            submitButton.disabled = true;
            errorMessage.classList.add("visible");
        }
    }

    document.querySelector("form").addEventListener("submit", function (event) {
        checkFormValidity();
        
        if (submitButton.disabled) {
            event.preventDefault();
            errorMessage.classList.add("visible");
        }
    });
});
// Mevcut kodlarınızın altına ekleyin
document.getElementById('submitButton').addEventListener('click', function(event) {
    const agreementChecked = document.getElementById('agreement').checked;
    const agreementMessage = document.getElementById('agreement-message');

    if (!agreementChecked) {
        event.preventDefault(); // Formun gönderilmesini engeller
        agreementMessage.style.display = 'block'; // Mesajı gösterir
    } else {
        agreementMessage.style.display = 'none'; // Mesajı gizler
    }
});
