document.addEventListener('DOMContentLoaded', function () {
    // =============================================
    // Elementos del DOM y configuraciones generales
    // =============================================
    const sidebar = document.querySelector('.sidebar');
    const main = document.querySelector('.main');
    const footer = document.querySelector('.footer');
    const toggleBtn = document.getElementById('sidebarToggle');
    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    document.body.appendChild(overlay);
    
    const mobileBreakpoint = 768;
    const sidebarWidth = '280px';

    // =============================================
    // Funciones del Sidebar
    // =============================================
    function updateLayout() {
        const isCollapsed = sidebar.classList.contains('sidebar-collapsed');
        const isMobile = window.innerWidth <= mobileBreakpoint;

        if (isMobile) {
            sidebar.style.transform = isCollapsed ? 'translateX(-100%)' : 'translateX(0)';
            overlay.style.display = isCollapsed ? 'none' : 'block';
            main.style.marginLeft = '0';
            footer.style.left = '0';
        } else {
            overlay.style.display = 'none';
            sidebar.style.transform = isCollapsed ? 'translateX(-100%)' : 'translateX(0)';
            main.style.marginLeft = isCollapsed ? '0' : sidebarWidth;
            footer.style.left = isCollapsed ? '0' : sidebarWidth;
        }

        footer.style.width = isCollapsed ? '100%' : `calc(100% - ${sidebarWidth})`;
    }

    function toggleSidebar() {
        sidebar.classList.toggle('sidebar-collapsed');
        localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('sidebar-collapsed'));
        updateLayout();
    }

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

    function setupSwipe() {
        let touchStartX = 0;

        sidebar.addEventListener('touchstart', function (e) {
            touchStartX = e.touches[0].clientX;
        }, { passive: true });

        sidebar.addEventListener('touchend', function (e) {
            const touchEndX = e.changedTouches[0].clientX;
            const diff = touchStartX - touchEndX;

            if (Math.abs(diff) > 50) {
                if (diff > 0) {
                    sidebar.classList.add('sidebar-collapsed');
                } else {
                    sidebar.classList.remove('sidebar-collapsed');
                }
                localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('sidebar-collapsed'));
                updateLayout();
            }
        }, { passive: true });
    }

    function setActiveLink() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.sidebar .nav-link');

        navLinks.forEach(link => {
            link.classList.remove('active');
            const linkPath = link.getAttribute('href');

            if (linkPath === currentPath ||
                (linkPath !== '/' && currentPath.startsWith(linkPath))) {
                link.classList.add('active');
            }
        });
    }

    // =============================================
    // Funciones del Navbar (nuevas)
    // =============================================
    function setupLogout() {
        const logoutButton = document.getElementById('logoutButton');
        
        if (logoutButton) {
            logoutButton.addEventListener('click', function(e) {
                e.preventDefault();
                
                Swal.fire({
                    title: '¿Estás seguro?',
                    text: "¿Deseas cerrar tu sesión actual?",
                    icon: 'question',
                    showCancelButton: true,
                    confirmButtonColor: '#d33',
                    cancelButtonColor: '#3085d6',
                    confirmButtonText: 'Sí, cerrar sesión',
                    cancelButtonText: 'Cancelar',
                    reverseButtons: true
                }).then((result) => {
                    if (result.isConfirmed) {
                        // Eliminar todas las cookies
                        document.cookie.split(";").forEach(function(c) {
                            document.cookie = c.replace(/^ +/, "").replace(/=.*/, 
                                "=;expires=" + new Date().toUTCString() + ";path=/");
                        });
                        
                        // Redireccionar al index
                        window.location.href = "/";
                    }
                });
            });
        }
    }

    function actualizarFecha() {
        const fechaElement = document.getElementById('fechaTexto');
        if (!fechaElement) return;

        fetch('/tiempo/fecha_actual')
            .then(response => {
                if (!response.ok) throw new Error('Error en la respuesta');
                return response.json();
            })
            .then(data => {
                const [fecha, hora] = data.fecha.split(' ');
                fechaElement.innerHTML = `
                    <span class="fecha-part">${fecha}</span>
                    <span class="hora-part">${hora}</span>
                `;
            })
            .catch(error => {
                console.error('Error al obtener la fecha:', error);
                // Fallback con JavaScript puro
                const ahora = new Date();
                fechaElement.textContent = ahora.toLocaleString('es-ES', {
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit',
                    hour12: false
                }).replace(',', '');
            });
    }

    function initFecha() {
        if (document.getElementById('fechaTexto')) {
            actualizarFecha();
            setInterval(actualizarFecha, 1000);
        }
    }

    // =============================================
    // Inicialización general
    // =============================================
    function init() {
        const isMobile = window.innerWidth <= mobileBreakpoint;
        const savedState = localStorage.getItem('sidebarCollapsed');

        if (isMobile) {
            sidebar.classList.add('sidebar-collapsed');
        } else if (savedState === 'true') {
            sidebar.classList.add('sidebar-collapsed');
        } else {
            sidebar.classList.remove('sidebar-collapsed');
        }

        setupSidebarLinks();
        setupSwipe();
        setupLogout(); // Nueva función de inicialización
        updateLayout();
        initFecha();
    }

    // =============================================
    // Event Listeners
    // =============================================
    toggleBtn.addEventListener('click', toggleSidebar);
    overlay.addEventListener('click', toggleSidebar);
    window.addEventListener('resize', updateLayout);
    window.addEventListener('popstate', setActiveLink);

    // Inicialización final
    init();
    setActiveLink();
});