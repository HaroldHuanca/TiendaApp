document.addEventListener('DOMContentLoaded', function () {
    // Elementos del DOM
    const sidebar = document.querySelector('.sidebar');
    const main = document.querySelector('.main');
    const footer = document.querySelector('.footer');
    const toggleBtn = document.getElementById('sidebarToggle');
    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    document.body.appendChild(overlay);

    // Variables de configuración
    const mobileBreakpoint = 768;
    const sidebarWidth = '280px'; // Ajusta según tu variable CSS

    // Función principal para actualizar el layout
    function updateLayout() {
        const isCollapsed = sidebar.classList.contains('sidebar-collapsed');
        const isMobile = window.innerWidth <= mobileBreakpoint;

        // Comportamiento para móviles
        if (isMobile) {
            sidebar.style.transform = isCollapsed ? 'translateX(-100%)' : 'translateX(0)';
            overlay.style.display = isCollapsed ? 'none' : 'block';
            main.style.marginLeft = '0';
            footer.style.left = '0';
        }
        // Comportamiento para desktop
        else {
            overlay.style.display = 'none';
            sidebar.style.transform = isCollapsed ? 'translateX(-100%)' : 'translateX(0)';
            main.style.marginLeft = isCollapsed ? '0' : sidebarWidth;
            footer.style.left = isCollapsed ? '0' : sidebarWidth;
        }

        // Ajuste del ancho del footer
        footer.style.width = isCollapsed ? '100%' : `calc(100% - ${sidebarWidth})`;
    }
    function setActiveLink() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.sidebar .nav-link');

        navLinks.forEach(link => {
            link.classList.remove('active');

            // Obtiene la ruta del enlace (compatible con Flask)
            const linkPath = link.getAttribute('href');

            // Comparación más flexible para rutas de Flask
            if (linkPath === currentPath ||
                (linkPath !== '/' && currentPath.startsWith(linkPath))) {
                link.classList.add('active');
            }
        });
    }
    // Función para alternar el sidebar
    function toggleSidebar() {
        sidebar.classList.toggle('sidebar-collapsed');
        localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('sidebar-collapsed'));
        updateLayout();
    }

    // Gestión de eventos en enlaces del sidebar
    function setupSidebarLinks() {
        document.querySelectorAll('.sidebar .nav-link').forEach(link => {
            link.addEventListener('click', function () {
                if (window.innerWidth <= mobileBreakpoint) {
                    sidebar.classList.add('sidebar-collapsed');
                    localStorage.setItem('sidebarCollapsed', 'true');
                    updateLayout();
                }
            });
        });
    }

    // Configuración de swipe para móviles
    function setupSwipe() {
        let touchStartX = 0;

        sidebar.addEventListener('touchstart', function (e) {
            touchStartX = e.touches[0].clientX;
        }, { passive: true });

        sidebar.addEventListener('touchend', function (e) {
            const touchEndX = e.changedTouches[0].clientX;
            const diff = touchStartX - touchEndX;

            if (Math.abs(diff) > 50) { // Umbral de 50px para swipe
                if (diff > 0) {
                    sidebar.classList.add('sidebar-collapsed'); // Swipe izquierdo
                } else {
                    sidebar.classList.remove('sidebar-collapsed'); // Swipe derecho
                }
                localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('sidebar-collapsed'));
                updateLayout();
            }
        }, { passive: true });
    }

    // Inicialización
    function init() {
        const isMobile = window.innerWidth <= mobileBreakpoint;
        const savedState = localStorage.getItem('sidebarCollapsed');

        // Configuración inicial del sidebar
        if (isMobile) {
            sidebar.classList.add('sidebar-collapsed');
        } else if (savedState === 'true') {
            sidebar.classList.add('sidebar-collapsed');
        } else {
            sidebar.classList.remove('sidebar-collapsed'); // Asegura visibilidad en desktop
        }

        setupSidebarLinks();
        setupSwipe();
        updateLayout();
    }

    // Event listeners
    toggleBtn.addEventListener('click', toggleSidebar);
    overlay.addEventListener('click', toggleSidebar);
    window.addEventListener('resize', updateLayout);
    window.addEventListener('popstate', setActiveLink); // Para manejar navegación adelante/atrás
    // Inicializar
    init();
    setActiveLink(); 
});