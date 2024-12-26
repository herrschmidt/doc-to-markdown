import pytest
from pathlib import Path
from app.core.converter import DocumentConverter

@pytest.fixture
def sample_html_file(tmp_path):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Document</title>
    </head>
    <body>
        <h1>Sample HTML Document</h1>
        <p>This is a test paragraph with some <strong>bold</strong> and <em>italic</em> text.</p>
        <ul>
            <li>List item 1</li>
            <li>List item 2</li>
            <li>List item 3</li>
        </ul>
        <table>
            <tr>
                <th>Header 1</th>
                <th>Header 2</th>
            </tr>
            <tr>
                <td>Cell 1</td>
                <td>Cell 2</td>
            </tr>
        </table>
    </body>
    </html>
    """
    file_path = tmp_path / "sample.html"
    file_path.write_text(html_content)
    return file_path

async def test_html_conversion(sample_html_file):
    converter = DocumentConverter()
    
    # Create a mock UploadFile
    class MockUploadFile:
        def __init__(self, path):
            self.filename = path.name
            self._path = path
        
        async def read(self):
            return self._path.read_bytes()
    
    mock_file = MockUploadFile(sample_html_file)
    save_path = Path(sample_html_file).parent / "temp.html"
    
    try:
        result = await converter.convert(mock_file, save_path)
        
        # Verify the conversion result
        assert result["content"] is not None
        assert "Sample HTML Document" in result["content"]
        assert "List item" in result["content"]
        assert "Header 1" in result["content"]
        assert "Cell 1" in result["content"]
        
        # Verify metadata
        assert result["metadata"]["mime_type"] == "text/html"
        assert result["metadata"]["original_file"] == "sample.html"
        assert result["metadata"]["file_size"] > 0
        
    finally:
        # Clean up
        if save_path.exists():
            save_path.unlink()