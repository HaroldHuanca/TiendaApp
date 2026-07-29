class ScannerClient {
    constructor() {
        this.eventSource = null;
        this.isConnected = false;
        this.selectedDeviceId = null;
        this.deviceSelect = null;
        this.init();
    }

    init() {
        this.deviceSelect = document.getElementById('scannerDeviceSelect') || document.querySelector('[data-scanner-select]');
        this.bindScannerSelector();
        this.loadAvailableDevices();
        this.connect();
    }

    bindScannerSelector() {
        if (!this.deviceSelect) {
            return;
        }

        const storageKey = `scanner:selected:${window.location.pathname}`;
        const savedSelection = localStorage.getItem(storageKey);
        if (savedSelection) {
            this.selectedDeviceId = savedSelection;
        }

        this.deviceSelect.addEventListener('change', async (event) => {
            this.selectedDeviceId = event.target.value || null;
            if (this.selectedDeviceId) {
                localStorage.setItem(storageKey, this.selectedDeviceId);
            } else {
                localStorage.removeItem(storageKey);
            }

            try {
                await fetch('/scanner/connect', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ device_id: this.selectedDeviceId })
                });
            } catch (error) {
                console.error('No se pudo conectar el lector seleccionado:', error);
            }

            this.connect();
        });
    }

    async loadAvailableDevices() {
        if (!this.deviceSelect) {
            return;
        }

        try {
            const response = await fetch('/scanner/list_devices?only_connected=1');
            const data = await response.json();
            const devices = data.devices || [];
            const currentValue = this.deviceSelect.value;

            this.deviceSelect.innerHTML = '<option value="">Seleccionar lector...</option>';
            devices.forEach((device) => {
                const option = document.createElement('option');
                option.value = device.id;
                option.textContent = `${device.name} (${device.path || 'sin ruta'})`;
                this.deviceSelect.appendChild(option);
            });

            const selectedValue = this.selectedDeviceId || currentValue || '';
            if (selectedValue) {
                this.deviceSelect.value = selectedValue;
            }
        } catch (error) {
            console.error('No se pudieron cargar los lectores:', error);
        }
    }

    connect() {
        if (this.eventSource) {
            this.eventSource.close();
        }

        const query = this.selectedDeviceId ? `?device_id=${encodeURIComponent(this.selectedDeviceId)}` : '';
        console.log(`Connecting to scanner stream${query || '...'}`);
        this.eventSource = new EventSource(`/scanner/stream${query}`);

        this.eventSource.onopen = () => {
            console.log('Scanner stream connected');
            this.isConnected = true;
        };

        this.eventSource.onmessage = (event) => {
            const barcode = event.data;
            console.log('Received barcode:', barcode);

            const customEvent = new CustomEvent('scan', {
                detail: { barcode: barcode }
            });
            document.dispatchEvent(customEvent);
        };

        this.eventSource.onerror = (error) => {
            console.error('Scanner stream error:', error);
            this.isConnected = false;
            if (this.eventSource.readyState === EventSource.CLOSED) {
                setTimeout(() => this.connect(), 5000);
            }
        };
    }
}

window.scannerClient = new ScannerClient();
