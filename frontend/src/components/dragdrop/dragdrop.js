// @ts-check

class FileDropZone {
    constructor(options = {}) {
        this.options = {
            containerId: 'dropZone',
            inputId: 'fileInput',
            accept: '*/*',
            multiple: true,
            icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>`,
            mainText: 'Drag and drop files here',
            subText: 'or click to select files',
            onFilesReceived: (files) => console.log('Files received:', files),
            ...options
        };

        this.init();
    }

    init() {
        this.container = document.getElementById(this.options.containerId);
        if (!this.container) {
            throw new Error(`Container with id "${this.options.containerId}" not found`);
        }

        this.createFileInput();
        this.setupEventListeners();
    }

    createFileInput() {
        // Create hidden file input if it doesn't exist
        this.fileInput = document.getElementById(this.options.inputId);
        if (!this.fileInput) {
            this.fileInput = document.createElement('input');
            this.fileInput.type = 'file';
            this.fileInput.id = this.options.inputId;
            this.fileInput.className = 'hidden';
            this.fileInput.accept = this.options.accept;
            this.fileInput.multiple = this.options.multiple;
            document.body.appendChild(this.fileInput);
        }
    }

    setupEventListeners() {
        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            this.container.addEventListener(eventName, this.preventDefaults.bind(this), false);
            document.body.addEventListener(eventName, this.preventDefaults.bind(this), false);
        });

        // Highlight drop zone when dragging over it
        ['dragenter', 'dragover'].forEach(eventName => {
            this.container.addEventListener(eventName, this.highlight.bind(this), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            this.container.addEventListener(eventName, this.unhighlight.bind(this), false);
        });

        // Handle file selection
        this.container.addEventListener('drop', this.handleDrop.bind(this), false);
        this.container.addEventListener('click', () => this.fileInput.click());
        this.fileInput.addEventListener('change', this.handleFileSelect.bind(this));
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    highlight() {
        this.container.classList.add('border-primary');
    }

    unhighlight() {
        this.container.classList.remove('border-primary');
    }

    handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        this.handleFiles(files);
    }

    handleFileSelect(e) {
        const files = e.target.files;
        this.handleFiles(files);
    }

    handleFiles(files) {
        this.options.onFilesReceived(files);
    }

    static createDropZone(containerId, options = {}) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <div class="border-4 border-dashed border-base-300 rounded-lg p-8 text-center cursor-pointer hover:border-primary transition-colors">
                <div class="flex flex-col items-center gap-4">
                    ${options.icon || `
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>`}
                    <div>
                        <p class="text-lg font-semibold">${options.mainText || 'Drag and drop files here'}</p>
                        <p class="text-sm text-base-content/70">${options.subText || 'or click to select files'}</p>
                    </div>
                </div>
            </div>
        `;
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = FileDropZone;
}