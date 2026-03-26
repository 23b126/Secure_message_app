document.getElementById("encryptForm").onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const res = await fetch("/encrypt", { method: "POST", body: formData });
    const data = await res.json();
    if (data.error) {
        document.getElementById("encryptResult").innerText = data.error;
    } else {
        document.getElementById("encryptResult").innerHTML = `
            <strong>Nonce:</strong> ${data.nonce}<br>
            <strong>Ciphertext:</strong> ${data.ciphertext}
        `;
    }
};

document.getElementById("decryptForm").onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const res = await fetch("/decrypt", { method: "POST", body: formData });
    const data = await res.json();
    if (data.error) {
        document.getElementById("decryptResult").innerText = data.error;
    } else {
        document.getElementById("decryptResult").innerText = "Decrypted Message: " + data.plaintext;
    }
};
