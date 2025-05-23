function clearClientData() {
    document.getElementById("entry_client_name").value = "";
    document.getElementById("entry_client_cnpj").value = "";
    document.getElementById("entry_client_address").value = "";
    document.getElementById("entry_client_phone").value = "";
}
document.addEventListener("DOMContentLoaded", function () {
    window.maskCNPJ = function (cnpj) {
        var value = cnpj.value.replace(/\D/g, ""); // Remove tudo que não for número
        if (value.length <= 14) {
            value = value.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/, "$1.$2.$3/$4-$5");
        }
        cnpj.value = value;

        // Adiciona um valor sem formatação (somente números) para enviar ao servidor
        var cleanCNPJ = cnpj.value.replace(/\D/g, '');  // Remove a formatação
        document.getElementById('clean_cnpj').value = cleanCNPJ;  // Coloca o CNPJ limpo em um campo escondido
    };
});

document.addEventListener("DOMContentLoaded", () => {
    const menuToggle = document.getElementById("menu-toggle");
    const menu = document.getElementById("menu");

    // Menu Toggle para Dispositivos Móveis
    menuToggle.addEventListener("click", () => {
        menu.classList.toggle("hidden");
    });

    // Ativa Dark Mode Automático se configurado no sistema
    if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
        document.documentElement.classList.add("dark");
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const menuToggle = document.getElementById("menu-toggle");
    const menu = document.getElementById("menu");

    menuToggle.addEventListener("click", () => {
        menu.classList.toggle("hidden");
    });
});

// Máscara para o Telefone (Formato: (55) 99960-5600)
function maskPhone(event) {
    var phone = event.target.value.replace(/\D/g, ''); // Remove todos os caracteres não numéricos
    if (phone.length <= 11) {
        phone = phone.replace(/^(\d{2})(\d{5})(\d{4})$/, '($1) $2-$3');
    }
    event.target.value = phone;
}


function validateForm() {
    const cpf = document.getElementById("cpf").value.trim();
    const cnpj = document.getElementById("cnpj").value.trim();
    const cpfCnpjRegex = /^[0-9]{11}$|^[0-9]{14}$|^[0-9]{2}\.[0-9]{3}\.[0-9]{3}\/[0-9]{4}\-[0-9]{2}$|^[0-9]{3}\.[0-9]{3}\.[0-9]{3}\-[0-9]{2}$/;

    if (cpf && !cpfCnpjRegex.test(cpf)) {
        alert("CPF inválido. Verifique a formatação.");
        return false;
    }

    if (cnpj && !cpfCnpjRegex.test(cnpj)) {
        alert("CNPJ inválido. Verifique a formatação.");
        return false;
    }

    return true;
}