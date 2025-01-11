# Markdown Display Component

A reusable component for displaying, copying, and downloading markdown content with support for rendered and raw views.

## Features

- Rendered markdown view with proper styling
- Raw markdown view with monospace font
- Toggle between rendered and raw views
- Copy to clipboard functionality
- Download markdown file
- Middle mouse button horizontal scrolling
- Table formatting and styling
- Visual feedback for actions

## Installation

1. Include the required files:
```html
<link rel="stylesheet" href="./components/markdown-display/markdown-display.css">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script src="./components/markdown-display/markdown-display.js"></script>
```

2. Create a container element:
```html
<div id="markdownContainer"></div>
```

3. Initialize the component:
```javascript
const display = new MarkdownDisplay({
    containerId: 'markdownContainer'
});
```

## Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| containerId | string | required | ID of the container element |
| content | string | '' | Initial markdown content |
| downloadFileName | string | 'document.md' | Name of the downloaded file |
| enableCopy | boolean | true | Show copy button |
| enableDownload | boolean | true | Show download button |
| enableRawToggle | boolean | true | Show toggle button |

## Methods

### setContent(markdown)
Set the markdown content to display.
```javascript
display.setContent('# Hello\nThis is markdown');
```

### getContent()
Get the current markdown content.
```javascript
const markdown = display.getContent();
```

### showRaw(show)
Toggle between raw and rendered views.
```javascript
display.showRaw(true);  // Show raw markdown
display.showRaw(false); // Show rendered markdown
```

### destroy()
Clean up the component.
```javascript
display.destroy();
```

## Example Usage

```javascript
// Initialize with options
const display = new MarkdownDisplay({
    containerId: 'markdownContainer',
    downloadFileName: 'converted.md',
    enableCopy: true,
    enableDownload: true,
    enableRawToggle: true
});

// Set content
display.setContent('# Hello\nThis is markdown');

// Toggle view
document.getElementById('toggleBtn').addEventListener('click', () => {
    display.showRaw(true);
});
```

## Styling

The component uses BEM naming convention and is compatible with DaisyUI. All styles are scoped to the `.markdown-display` class.

You can override styles by targeting the following classes:
- `.markdown-display`
- `.markdown-display__copy-button`
- `.markdown-display__content`
- `.markdown-display__rendered`
- `.markdown-display__raw`
- `.markdown-display__controls`