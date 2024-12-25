# Drag and Drop Component

A reusable drag and drop component for file uploads that works with any web project.

## Features

- Customizable appearance through options and CSS
- Support for single or multiple file uploads
- Configurable file type restrictions
- Drag and drop or click-to-select functionality
- Callback for handling uploaded files
- Built with Tailwind CSS (but works without it)

## Installation

1. Copy the `dragdrop` directory to your project's components folder
2. Include the component files in your HTML:

```html
<link rel="stylesheet" href="path/to/components/dragdrop/dragdrop.css">
<script src="path/to/components/dragdrop/dragdrop.js"></script>
```

## Usage

1. Create a container element in your HTML:
```html
<div id="myDropZone"></div>
```

2. Initialize the component:
```javascript
const dropZone = new FileDropZone({
    containerId: 'myDropZone',
    accept: '*/*',  // or specific file types like 'image/*,.pdf'
    multiple: true, // or false for single file
    onFilesReceived: (files) => {
        // Handle your files here
        console.log('Files received:', files);
    }
});

// Create the initial HTML structure
FileDropZone.createDropZone('myDropZone');
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| containerId | string | 'dropZone' | ID of the container element |
| inputId | string | 'fileInput' | ID for the hidden file input |
| accept | string | '*/*' | Accepted file types |
| multiple | boolean | true | Allow multiple file selection |
| icon | string | SVG markup | Custom icon markup |
| mainText | string | 'Drag and drop files here' | Main text display |
| subText | string | 'or click to select files' | Secondary text display |
| onFilesReceived | function | console.log | Callback for handling files |

## Styling

The component uses Tailwind CSS classes by default but can be styled using custom CSS. The main classes are:

- `.file-drop-zone` - The main container
- `.file-drop-zone.dragging` - Applied when dragging files over the zone

## Example

```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="components/dragdrop/dragdrop.css">
</head>
<body>
    <div id="uploadZone"></div>

    <script src="components/dragdrop/dragdrop.js"></script>
    <script>
        const dropZone = new FileDropZone({
            containerId: 'uploadZone',
            accept: 'image/*,.pdf',
            multiple: true,
            mainText: 'Upload your documents',
            subText: 'Images and PDFs only',
            onFilesReceived: (files) => {
                Array.from(files).forEach(file => {
                    console.log(`Received file: ${file.name}`);
                });
            }
        });

        FileDropZone.createDropZone('uploadZone');
    </script>
</body>
</html>
```