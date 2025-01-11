# Plan: Refactor Markdown Display into Component

## Current State
- Markdown display logic is embedded in main index.html
- Includes multiple features:
  - Rendered/raw markdown toggle
  - Copy to clipboard
  - Download functionality
  - Middle mouse button horizontal scrolling
  - Table styling
  - Cursor feedback

## Component Structure

### File Organization
```
frontend/src/components/markdown-display/
├── markdown-display.js     # Main component class
├── markdown-display.css    # Component styles
└── README.md              # Documentation
```

### Class Design
```javascript
class MarkdownDisplay {
    constructor(options) {
        // Required options
        containerId: string       // ID of container element
        content: string          // Initial markdown content (optional)
        
        // Optional options
        downloadFileName: string  // Default: 'document.md'
        enableCopy: boolean      // Default: true
        enableDownload: boolean  // Default: true
        enableRawToggle: boolean // Default: true
    }
    
    // Public methods
    setContent(markdown)         // Update content
    getContent()                // Get raw markdown
    showRaw(show)              // Toggle raw view
    destroy()                  // Cleanup
}
```

### HTML Structure
```html
<div class="markdown-display">
    <!-- Copy Button -->
    <button class="copy-button">...</button>
    
    <!-- Content Area -->
    <div class="content-area">
        <div class="rendered-markdown">...</div>
        <pre class="raw-markdown">...</pre>
    </div>
    
    <!-- Controls -->
    <div class="controls">
        <button class="toggle-button">...</button>
        <button class="download-button">...</button>
    </div>
</div>
```

## Features to Extract

### 1. Core Display
- Rendered markdown view
- Raw markdown view
- Toggle functionality
- Styling for both views

### 2. Table Handling
- Table styles
- Horizontal scrolling
- Middle mouse button scrolling
- Cursor feedback

### 3. Actions
- Copy to clipboard
- Download markdown
- Success/error feedback

### 4. Styling
- Move all styles to markdown-display.css
- Use BEM naming convention
- Maintain DaisyUI compatibility

## Usage Example
```javascript
// Initialize
const display = new MarkdownDisplay({
    containerId: 'markdownContainer',
    downloadFileName: 'converted.md'
});

// Set content
display.setContent('# Hello\nThis is markdown');

// Event handling
display.on('copy', () => console.log('Content copied'));
display.on('download', () => console.log('Content downloaded'));
display.on('toggle', (isRaw) => console.log('View toggled:', isRaw));
```

## Implementation Steps

1. Component Setup
   - Create component directory structure
   - Move relevant styles to CSS file
   - Create base component class

2. Core Functionality
   - Extract markdown rendering logic
   - Implement toggle functionality
   - Add event handling

3. Features
   - Implement copy functionality
   - Add download handling
   - Add scroll handling
   - Add feedback mechanisms

4. Documentation
   - Create README with usage examples
   - Document options and methods
   - Add JSDoc comments

5. Integration
   - Update index.html to use new component
   - Test all functionality
   - Ensure backward compatibility

## Migration Strategy

1. Create Component
   - Implement all features in new files
   - Test independently

2. Parallel Implementation
   - Add new component alongside existing code
   - Test both implementations

3. Switchover
   - Replace old implementation with new component
   - Verify all functionality
   - Remove old code

4. Documentation
   - Update main README
   - Add component documentation
   - Add migration guide if needed