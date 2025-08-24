from dataclasses import dataclass
from pathlib import Path
import json
import re
from typing import List

from pypdf import PdfReader


@dataclass
class QAPair:
    """Represents a question/answer pair."""
    question: str
    answer: str


def _split_document(pdf_path: str, pattern: str) -> List[str]:
    """Split a PDF into chunks based on a regex pattern.

    The pattern should capture the beginning of each problem (e.g., ``"\n\d+\."``).
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"

    matches = list(re.finditer(pattern, text))
    chunks: List[str] = []
    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        chunks.append(text[start:end].strip())
    return chunks


def build_pairs(question_pdf: str, answer_pdf: str, pattern: str = r"\n\d+\.") -> List[QAPair]:
    """Create question/answer pairs from two PDFs."""
    questions = _split_document(question_pdf, pattern)
    answers = _split_document(answer_pdf, pattern)
    pairs = [QAPair(q, a) for q, a in zip(questions, answers)]
    return pairs


def save_pairs(pairs: List[QAPair], output_dir: str) -> None:
    """Save pairs as a JSON file."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    data = [dict(id=i + 1, question=p.question, answer=p.answer) for i, p in enumerate(pairs)]
    out_file = Path(output_dir) / "pairs.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Split PDF workbooks into paired question/answer JSON data")
    parser.add_argument("question_pdf", help="Path to the questions PDF")
    parser.add_argument("answer_pdf", help="Path to the answers PDF")
    parser.add_argument("output_dir", help="Directory to write the resulting pairs.json")
    args = parser.parse_args()

    qa_pairs = build_pairs(args.question_pdf, args.answer_pdf)
    save_pairs(qa_pairs, args.output_dir)
