import os
import fitz 

class DocumentParser:
    @staticmethod
    def parse(file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        _, ext = os.path.splitext(file_path.lower())

        if ext == ".pdf":
            return DocumentParser._parse_pdf(file_path)
        elif ext in [".txt", ".md"]:
            return DocumentParser._parse_text(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    @staticmethod
    def _parse_pdf(file_path: str) -> str:
        text_content = []
        try:
            doc = fitz.open(file_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                blocks = page.get_text("blocks")
                blocks.sort(key=lambda b: (b[1], b[0]))
                
                for b in blocks:
                    if b[6] == 0: 
                        text = b[4].strip()
                        if text:
                            text_content.append(text)
            doc.close()
            return "\n\n".join(text_content)
        except Exception as e:
            raise RuntimeError(f"Error parsing PDF file with PyMuPDF: {str(e)}")

    @staticmethod
    def _parse_text(file_path: str) -> str:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            raise RuntimeError(f"Error parsing text file: {str(e)}")
