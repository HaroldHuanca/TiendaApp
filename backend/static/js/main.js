document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.sidebar');
    const main = document.querySelector('.main');
    const footer = document.querySelector('.footer');
    const navLinks = document.querySelectorAll('.nav-link');

    // Función para actualizar el estado del layout
    function updateLayout() {
        const isCollapsed = sidebar.classList.contains('sidebar-collapsed');
        
        // Aplicar clases y estilos
        if (isCollapsed) {
            main.style.marginLeft = '0';
            footer.style.left = '0';
            footer.style.width = '100%';
        } else {
            main.style.marginLeft = 'var(--sidebar-width)';
            footer.style.left = 'var(--sidebar-width)';
            footer.style.width = 'calc(100% - var(--sidebar-width))';
        }
        
        // Guardar estado
        localStorage.setItem('sidebarCollapsed', isCollapsed);
    }

    // Evento para alternar el sidebar
    sidebarToggle.addEventListener('click', function() {
        sidebar.classList.toggle('sidebar-collapsed');
        updateLayout();
    });

    // Cerrar sidebar en móviles al hacer clic en enlaces
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                sidebar.classList.add('sidebar-collapsed');
                updateLayout();
            }
        });
    });

    // Cargar estado inicial
    if (localStorage.getItem('sidebarCollapsed') === 'true') {
        sidebar.classList.add('sidebar-collapsed');
    }
    updateLayout();

    // Manejar cambios de tamaño de pantalla
    window.addEventListener('resize', function() {
        updateLayout();
        
        // En móviles, forzar sidebar colapsado
        if (window.innerWidth <= 768) {
            if (!sidebar.classList.contains('sidebar-collapsed')) {
                sidebar.classList.add('sidebar-collapsed');
                updateLayout();
            }
        }
    });

    // Inicializar tooltips de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});