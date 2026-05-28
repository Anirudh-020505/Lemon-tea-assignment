import os
import pytest
from app.ingestion.parser import DocumentParser
from app.ingestion.chunker import RecursiveCharacterChunker
from app.ingestion.embedder import LocalEmbedder

def test_document_parser_txt(tmp_path):
    txt_file = tmp_path / "sample.txt"
    txt_file.write_text("Hello World! This is LemonRAG.", encoding="utf-8")
    
    text = DocumentParser.parse(str(txt_file))
    assert text == "Hello World! This is LemonRAG."

def test_document_parser_invalid_path():
    with pytest.raises(FileNotFoundError):
        DocumentParser.parse("nonexistent_file.pdf")

def test_recursive_character_chunker():
    text = "Paragraph one is here.\n\nParagraph two is there. It is a bit longer."
    chunker = RecursiveCharacterChunker(chunk_size=30, chunk_overlap=5)
    chunks = chunker.chunk(text)
    
    assert len(chunks) >= 2
    assert all(len(c) > 0 for c in chunks)
    assert "Paragraph one is here." in chunks

def test_local_embedder():
    vector = LocalEmbedder.embed_text("Test query")
    assert isinstance(vector, list)
    assert len(vector) > 0
    assert all(isinstance(val, float) for val in vector)
