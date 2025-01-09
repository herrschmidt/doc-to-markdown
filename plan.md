# Plan: Fix Frontend JSON Response Handling

## Current Issue
- The frontend is not properly parsing the JSON response from the backend
- Currently in `index.html`, the code uses `response.text()` which treats the response as plain text
- This causes the raw JSON (including curly braces and escaped newlines) to be displayed
- Example of what user sees:
  ```
  {"content": "Raumkapsel Schmidt & Stein-Schomburg GbR\nUniversitätsplatz 12 34127 Kassel\n\nRechnung 1/24\n\n## Dramaturgische Beratung 'Beihai'"}
  ```

## Analysis
- The backend is working correctly, returning a proper JSON response
- The issue is in the frontend's handling of the response
- We need to:
  1. Parse the JSON response properly
  2. Extract the 'content' field
  3. Display the content with proper line breaks

## Solution Plan

### Most Concise Fix
1. Modify the fetch response handling in `index.html`:
   ```javascript
   // Change from:
   .then(response => response.text())
   
   // To:
   .then(response => response.json())
   .then(data => data.content)
   ```

### Benefits
- Minimal code change required
- Properly handles JSON response
- Preserves all markdown formatting
- No changes needed in backend
- No changes to API contract

## Implementation Steps
1. Update the fetch response handling in frontend code
2. Test with various document types
3. Verify markdown formatting is preserved
4. Update frontend documentation to clarify JSON handling

## Testing
- Test with various document types
- Verify line breaks are displayed correctly
- Test markdown formatting preservation
- Test special characters handling