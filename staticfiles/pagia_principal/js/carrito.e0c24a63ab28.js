function agregarCarrito(id, nombre, precio) {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];

    carrito.push({ id, nombre, precio });

    localStorage.setItem('carrito', JSON.stringify(carrito));

    // Notificación simple
    const aviso = document.createElement("div");
    aviso.className = "fixed bottom-6 right-6 bg-[var(--accent)] text-black px-4 py-2 rounded shadow-lg";
    aviso.innerText = `${nombre} añadido al carrito ✅`;
    document.body.appendChild(aviso);

    setTimeout(() => aviso.remove(), 2200);
}
