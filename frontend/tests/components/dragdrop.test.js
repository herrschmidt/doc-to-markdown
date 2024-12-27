/**
 * @jest-environment jsdom
 */

describe('FileDropZone', () => {
    let container;
    let fileInput;
    let onFilesReceived;

    beforeEach(() => {
        // Set up DOM elements
        container = document.createElement('div');
        container.id = 'dropZone';
        document.body.appendChild(container);

        fileInput = document.createElement('input');
        fileInput.id = 'fileInput';
        fileInput.type = 'file';
        document.body.appendChild(fileInput);

        // Mock the onFilesReceived callback
        onFilesReceived = jest.fn();

        // Import the FileDropZone class
        global.FileDropZone = require('../../src/components/dragdrop/dragdrop.js');
    });

    afterEach(() => {
        document.body.innerHTML = '';
        jest.clearAllMocks();
    });

    test('initializes with default options', () => {
        const dropZone = new FileDropZone();
        expect(dropZone.options.containerId).toBe('dropZone');
        expect(dropZone.options.inputId).toBe('fileInput');
        expect(dropZone.options.accept).toBe('*/*');
        expect(dropZone.options.multiple).toBe(true);
    });

    test('initializes with custom options', () => {
        const customOptions = {
            containerId: 'customZone',
            inputId: 'customInput',
            accept: 'image/*',
            multiple: false,
            onFilesReceived: onFilesReceived
        };

        // Create custom elements
        const customContainer = document.createElement('div');
        customContainer.id = 'customZone';
        document.body.appendChild(customContainer);

        const dropZone = new FileDropZone(customOptions);
        expect(dropZone.options.containerId).toBe('customZone');
        expect(dropZone.options.inputId).toBe('customInput');
        expect(dropZone.options.accept).toBe('image/*');
        expect(dropZone.options.multiple).toBe(false);
    });

    test('throws error when container is not found', () => {
        document.body.innerHTML = ''; // Clear the DOM
        expect(() => new FileDropZone()).toThrow('Container with id "dropZone" not found');
    });

    test('creates file input if it does not exist', () => {
        document.body.innerHTML = '<div id="dropZone"></div>'; // Only create container
        const dropZone = new FileDropZone();
        const createdInput = document.getElementById('fileInput');
        
        expect(createdInput).toBeTruthy();
        expect(createdInput.type).toBe('file');
        expect(createdInput.className).toBe('hidden');
    });

    test('handles drag events correctly', () => {
        const dropZone = new FileDropZone({ onFilesReceived });
        
        // Test dragenter
        container.dispatchEvent(new Event('dragenter'));
        expect(container.classList.contains('border-primary')).toBe(true);

        // Test dragleave
        container.dispatchEvent(new Event('dragleave'));
        expect(container.classList.contains('border-primary')).toBe(false);
    });

    test('handles file drop correctly', () => {
        const dropZone = new FileDropZone({ onFilesReceived });
        const mockFiles = [new File([''], 'test.txt')];
        
        const dropEvent = new Event('drop');
        dropEvent.dataTransfer = { files: mockFiles };
        
        container.dispatchEvent(dropEvent);
        expect(onFilesReceived).toHaveBeenCalledWith(mockFiles);
        expect(container.classList.contains('border-primary')).toBe(false);
    });

    test('handles file selection through input correctly', () => {
        const dropZone = new FileDropZone({ onFilesReceived });
        const mockFiles = [new File([''], 'test.txt')];
        
        const changeEvent = new Event('change');
        Object.defineProperty(changeEvent, 'target', { value: { files: mockFiles } });
        
        fileInput.dispatchEvent(changeEvent);
        expect(onFilesReceived).toHaveBeenCalledWith(mockFiles);
    });

    test('creates drop zone HTML with custom text', () => {
        const customText = {
            mainText: 'Custom Drop Text',
            subText: 'Custom Sub Text'
        };
        
        // Test default text
        FileDropZone.createDropZone('dropZone');
        expect(container.innerHTML).toContain('Drag and drop files here');
        
        // Test with custom text
        FileDropZone.createDropZone('dropZone', customText);
        expect(container.innerHTML).toContain(customText.mainText);
        expect(container.innerHTML).toContain(customText.subText);
    });

    test('integrates with the API correctly', async () => {
        // Mock fetch
        global.fetch = jest.fn(() =>
            Promise.resolve({
                ok: true,
                text: () => Promise.resolve('# Test Document\n\nThis is a test document.')
            })
        );

        // Create a mock file
        const mockFile = new File(['test content'], 'test.docx', { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });

        // Initialize FileDropZone with a mock callback
        const mockCallback = jest.fn();
        const dropZone = new FileDropZone({
            onFilesReceived: (files) => {
                const formData = new FormData();
                const file = Array.from(files)[0];
                formData.append('file', file);

                return fetch('http://localhost:8001/api/v1/convert', {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.text();
                })
                .then(markdown => {
                    mockCallback(markdown);
                });
            }
        });

        // Simulate file drop
        const dropEvent = new Event('drop');
        dropEvent.dataTransfer = { files: [mockFile] };
        container.dispatchEvent(dropEvent);

        // Wait for the API call to complete
        await new Promise(resolve => setTimeout(resolve, 100));

        // Verify the API call
        expect(global.fetch).toHaveBeenCalledWith('http://localhost:8001/api/v1/convert', {
            method: 'POST',
            body: expect.any(FormData)
        });

        // Verify the callback was called with the markdown
        expect(mockCallback).toHaveBeenCalledWith('# Test Document\n\nThis is a test document.');
    });
});