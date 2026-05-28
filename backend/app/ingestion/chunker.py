from typing import List

class RecursiveCharacterChunker:
    def __init__(self, chunk_size: int = 2000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = ["\n\n", "\n", ".", " ", ""]

    def chunk(self, text: str) -> List[str]:
        if not text:
            return []
            
        return self._split_text(text, self.separators)

    def _split_text(self, text: str, separators: List[str]) -> List[str]:
        separator = separators[0] if separators else ""
        next_separators = separators[1:] if len(separators) > 1 else []

        if separator == "":
            splits = list(text)
        else:
            splits = text.split(separator)

        chunks = []
        current_doc = []
        current_len = 0

        for split in splits:
            split_len = len(split)
            
            if split_len > self.chunk_size:
                if current_doc:
                    chunks.append(separator.join(current_doc))
                    current_doc = []
                    current_len = 0
                
                if next_separators:
                    recursive_chunks = self._split_text(split, next_separators)
                    chunks.extend(recursive_chunks)
                else:
                    for i in range(0, split_len, self.chunk_size):
                        chunks.append(split[i : i + self.chunk_size])
            else:
                sep_len = len(separator) if current_doc else 0
                if current_len + split_len + sep_len > self.chunk_size:
                    chunks.append(separator.join(current_doc))
                    
                    overlap_doc = []
                    overlap_len = 0
                    for prev_split in reversed(current_doc):
                        prev_len = len(prev_split)
                        sep_add = len(separator) if overlap_doc else 0
                        if overlap_len + prev_len + sep_add <= self.chunk_overlap:
                            overlap_doc.insert(0, prev_split)
                            overlap_len += prev_len + sep_add
                        else:
                            break
                    current_doc = overlap_doc
                    current_len = overlap_len

                sep_len = len(separator) if current_doc else 0
                current_doc.append(split)
                current_len += split_len + sep_len

        if current_doc:
            chunks.append(separator.join(current_doc))

        return [c.strip() for c in chunks if c.strip()]
