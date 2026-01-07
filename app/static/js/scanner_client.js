class ScannerClient {
    constructor() {
        this.eventSource = null;
        this.isConnected = false;
        this.init();
    }

    init() {
        this.connect();
    }

    connect() {
        if (this.eventSource) {
            this.eventSource.close();
        }

        console.log("Connecting to scanner stream...");
        this.eventSource = new EventSource('/scanner/stream');

        this.eventSource.onopen = () => {
            console.log("Scanner stream connected");
            this.isConnected = true;
        };

        this.eventSource.onmessage = (event) => {
            const barcode = event.data;
            console.log("Received barcode:", barcode);

            // Dispatch a custom event that pages can listen to
            const customEvent = new CustomEvent('scan', {
                detail: { barcode: barcode }
            });
            document.dispatchEvent(customEvent);
        };

        this.eventSource.onerror = (error) => {
            console.error("Scanner stream error:", error);
            this.isConnected = false;
            if (this.eventSource.readyState === EventSource.CLOSED) {
                // Try to reconnect in 5 seconds
                setTimeout(() => this.connect(), 5000);
            }
        };
    }
}

// Initialize on page load
const scannerClient = new ScannerClient();
