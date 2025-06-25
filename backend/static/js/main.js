document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const sidebar = document.querySelector('.sidebar');
    const main = document.querySelector('.main');
    const footer = document.querySelector('.footer');
    const toggleBtn = document.getElementById('sidebarToggle');
    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    document.body.appendChild(overlay);

    // Inicialización
    function init() {
        // Verificar si es móvil
        const isMobile = window.innerWidth <= 768;
        
        // Cargar estado guardado o configurar por defecto para móviles
        const savedState = localStorage.getItem('sidebarCollapsed');
        
        if (isMobile || savedState === 'true') {
            sidebar.classList.add('sidebar-collapsed');
        }
        
        updateLayout();
    }

    // Actualizar el layout
    function updateLayout() {
        const isCollapsed = sidebar.classList.contains('sidebar-collapsed');
        const isMobile = window.innerWidth <= 768;
        
        if (isMobile) {
            if (isCollapsed) {
                overlay.style.display = 'none';
            } else {
                overlay.style.display = 'block';
            }
        } else {
            overlay.style.display = 'none';
        }
    }

    // Evento del botón toggle
    toggleBtn.addEventListener('click', function() {
        sidebar.classList.toggle('sidebar-collapsed');
        localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('sidebar-collapsed'));
        updateLayout();
    });

    // Cerrar sidebar al hacer clic en el overlay
    overlay.addEventListener('click', function() {
        sidebar.classList.add('sidebar-collapsed');
        localStorage.setItem('sidebarCollapsed', true);
        updateLayout();
    });

    // Cerrar sidebar al seleccionar un enlace (en móviles)
    document.querySelectorAll('.sidebar .nav-link').forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                sidebar.classList.add('sidebar-collapsed');
                localStorage.setItem('sidebarCollapsed', true);
                updateLayout();
            }
        });
    });

    // Swipe para móviles
    let touchStartX = 0;
    
    sidebar.addEventListener('touchstart', function(e) {
        touchStartX = e.touches[0].clientX;
    }, {passive: true});

    sidebar.addEventListener('touchend', function(e) {
        const touchEndX = e.changedTouches[0].clientX;
        const diff = touchStartX - touchEndX;
        
        // Swipe izquierdo (ocultar)
        if (diff > 50) {
            sidebar.classList.add('sidebar-collapsed');
            localStorage.setItem('sidebarCollapsed', true);
            updateLayout();
        }
        // Swipe derecho (mostrar)
        else if (diff < -50) {
            sidebar.classList.remove('sidebar-collapsed');
            localStorage.setItem('sidebarCollapsed', false);
            updateLayout();
        }
    }, {passive: true});

    // Redimensionamiento de ventana
    window.addEventListener('resize', function() {
        updateLayout();
    });

    // Inicializar
    init();
});