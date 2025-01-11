class MarkdownDisplay {
    constructor(options) {
        // Validate required options
        if (!options.containerId) {
            throw new Error('containerId is required');
        }

        // Store options with defaults
        this.options = {
            downloadFileName: 'document.md',
            enableCopy: true,
            enableDownload: true,
            enableRawToggle: true,
            ...options
        };

        // Initialize state
        this.isShowingRaw = false;
        this.content = options.content || '';

        // Create DOM structure
        this.createDOMStructure();
        
        // Initialize features
        this.initializeScrolling();
        this.initializeEventListeners();
    }

    createDOMStructure() {
        // Get container
        this.container = document.getElementById(this.options.containerId);
        if (!this.container) {
            throw new Error(`Container with id "${this.options.containerId}" not found`);
        }

        // Add main class
        this.container.classList.add('markdown-display');

        // Create HTML structure
        this.container.innerHTML = `
            ${this.options.enableCopy ? `
                <button class="markdown-display__copy-button btn btn-ghost btn-sm" title="Copy to clipboard">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                </button>
            ` : ''}
            <div class="markdown-display__content">
                <div class="markdown-display__rendered"></div>
                <pre class="markdown-display__raw hidden"></pre>
            </div>
            ${this.options.enableRawToggle || this.options.enableDownload ? `
                <div class="markdown-display__controls">
                    ${this.options.enableRawToggle ? `
                        <button class="btn btn-primary toggle-view-btn">
                            Show Raw Markdown
                        </button>
                    ` : '<div></div>'}
                    ${this.options.enableDownload ? `
                        <button class="btn btn-primary download-btn">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                            </svg>
                            Download Markdown
                        </button>
                    ` : ''}
                </div>
            ` : ''}
        `;

        // Store element references
        this.renderedView = this.container.querySelector('.markdown-display__rendered');
        this.rawView = this.container.querySelector('.markdown-display__raw');
        this.copyButton = this.container.querySelector('.markdown-display__copy-button');
        this.toggleButton = this.container.querySelector('.toggle-view-btn');
        this.downloadButton = this.container.querySelector('.download-btn');
    }

    initializeScrolling() {
        const addMiddleMouseScrolling = (element) => {
            if (!element) return;
            
            let isScrolling = false;
            let startX;
            let scrollLeft;

            element.addEventListener('mousedown', (e) => {
                // Middle mouse button (button 1)
                if (e.button === 1) {
                    isScrolling = true;
                    startX = e.pageX - element.offsetLeft;
                    scrollLeft = element.scrollLeft;
                    e.preventDefault();
                }
            });

            element.addEventListener('mousemove', (e) => {
                if (!isScrolling) return;
                const x = e.pageX - element.offsetLeft;
                const walk = (x - startX) * 2;
                element.scrollLeft = scrollLeft - walk;
            });

            const stopScrolling = () => {
                if (isScrolling) {
                    isScrolling = false;
                }
            };

            element.addEventListener('mouseup', stopScrolling);
            element.addEventListener('mouseleave', stopScrolling);
            document.addEventListener('mouseup', stopScrolling);
        };

        // Add scrolling to both views
        addMiddleMouseScrolling(this.renderedView);
        addMiddleMouseScrolling(this.rawView);
    }

    initializeEventListeners() {
        // Toggle view
        if (this.toggleButton) {
            this.toggleButton.addEventListener('click', () => {
                this.showRaw(!this.isShowingRaw);
            });
        }

        // Copy to clipboard
        if (this.copyButton) {
            this.copyButton.addEventListener('click', async () => {
                try {
                    await navigator.clipboard.writeText(this.content);
                    this.copyButton.classList.add('btn-success');
                    setTimeout(() => {
                        this.copyButton.classList.remove('btn-success');
                    }, 1000);
                } catch (err) {
                    console.error('Failed to copy text:', err);
                    this.copyButton.classList.add('btn-error');
                    setTimeout(() => {
                        this.copyButton.classList.remove('btn-error');
                    }, 1000);
                }
            });
        }

        // Download
        if (this.downloadButton) {
            this.downloadButton.addEventListener('click', () => {
                const blob = new Blob([this.content], { type: 'text/markdown' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = this.options.downloadFileName;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            });
        }
    }

    setContent(markdown) {
        this.content = markdown;
        this.rawView.textContent = markdown;
        this.renderedView.innerHTML = marked.parse(markdown);
    }

    getContent() {
        return this.content;
    }

    showRaw(show) {
        this.isShowingRaw = show;
        if (show) {
            this.rawView.classList.remove('hidden');
            this.renderedView.classList.add('hidden');
            this.toggleButton?.textContent = 'Show Rendered Markdown';
        } else {
            this.rawView.classList.add('hidden');
            this.renderedView.classList.remove('hidden');
            this.toggleButton?.textContent = 'Show Raw Markdown';
        }
    }

    destroy() {
        // Remove all event listeners and clean up
        this.container.innerHTML = '';
        this.container.classList.remove('markdown-display');
    }
}

// Export the class
export default MarkdownDisplay;