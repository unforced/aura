import pytest
from pypdf import PdfReader

def test_parse_pdf(sample_pdf_path):
    """
    Tests that text can be successfully extracted from a PDF file.
    """
    reader = PdfReader(sample_pdf_path)
    page = reader.pages[0]
    text = page.extract_text()
    
    assert "This is a test PDF document for Project Aura." in text 