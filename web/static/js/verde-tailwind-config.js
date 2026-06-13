// Inicialización nativa del objeto de configuración de Tailwind CSS - TEMA VERDE
window.tailwind = window.tailwind || {};
window.tailwind.config = {
    theme: {
        extend: {
            colors: {
                brand: {
                    claro: '#34d399',   // 🟢 Verde esmeralda brillante para textos destacados y enfoques (emerald-400)
                    base: '#059669',    // 🟢 Verde esmeralda base para los botones principales (emerald-600)
                    oscuro: '#047857',  // 🟢 Verde esmeralda oscuro para efectos Hover al pasar el mouse (emerald-700)
                }
            }
        }
    }
}