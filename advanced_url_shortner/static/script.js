function copyURL() {
    const input = document.getElementById("shortUrl");
    input.select();
    document.execCommand("copy");
    showToast("✅ Copied to clipboard!");
}

function showToast(message) {
    const toast = document.getElementById("toast");
    toast.innerText = message;
    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 2000);
}
