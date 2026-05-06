// static/js/main.js
document.addEventListener('DOMContentLoaded', function () {
    // --- Auto-cerrar alertas flash despues de 5 segundos ---
    // (complementa la animación CSS del styles.css)
    setTimeout(function () {
        document.querySelectorAll('.alert').forEach(function (alertElement) {
            // Usa getOrCreateInstance para compatibilidad con Bootstrap 5
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alertElement);
            bsAlert.close();
        });
    }, 5000); // Cierra las alertas después de 5 segundos

    // --- Confirmacion antes de eliminar ---
    // Uso en el template: <button onclick="return confirmar('¿Eliminar este registro?')" ...>Eliminar</button>
    window.confirmar = function (mensaje) {
        return confirm(mensaje || '¿Estás seguro?');
    };

    // --- Resaltar fila al hacer clic (navegación intuitiva para listas) ---
    // Uso: <tr class="fila-link" data-href="{% url 'encomienda_detalle' enc.pk %}">
    document.querySelectorAll('.fila-link').forEach(function (fila) {
        fila.addEventListener('click', function () {
            const url = this.dataset.href;
            if (url) {
                window.location = url;
            }
        });
    });

    // --- Inicializar tooltips de Bootstrap (opcional si los usas) ---
    // const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    // tooltips.forEach(el => new bootstrap.Tooltip(el));
});