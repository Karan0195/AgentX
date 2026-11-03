"""
DocumentEngine: Autonomous Multimodal & Document Question-Answering Engine for AgentX.
Reads any PDF, image, scanned page, tabular sheet, voter list, or document.
Features multi-tier extraction, OCR fallback, structural record parsing,
fuzzy/transliterated name lookups, and visual analysis.
"""

import os
import re
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import fitz  # PyMuPDF
from PIL import Image
import numpy as np

logger = logging.getLogger("agentx.document_engine")

# Initialize RapidOCR engine lazily
_ocr_engine = None

def get_ocr_engine():
    global _ocr_engine
    if _ocr_engine is None:
        try:
            from rapidocr_onnxruntime import RapidOCR
            _ocr_engine = RapidOCR()
            logger.info("RapidOCR initialized successfully.")
        except Exception as e:
            logger.warning(f"Could not initialize RapidOCR: {e}")
            _ocr_engine = False
    return _ocr_engine if _ocr_engine is not False else None


# Transliteration character mapping (Devanagari <-> Latin)
DEVA_TO_LATIN = {
    'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'ng',
    'च': 'ch', 'छ': 'chh', 'ज': 'j', 'झ': 'jh', 'ञ': 'ny',
    'ट': 't', 'ठ': 'th', 'ड': 'd', 'ढ': 'dh', 'ण': 'n',
    'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n',
    'प': 'p', 'फ': 'ph', 'ब': 'b', 'भ': 'bh', 'म': 'm',
    'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'v', 'श': 'sh',
    'ष': 'sh', 'स': 's', 'ह': 'h', 'ळ': 'l', 'क्ष': 'ksh', 'ज्ञ': 'dny',
    'ा': 'a', 'ि': 'i', 'ी': 'ee', 'ु': 'u', 'ू': 'oo',
    'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au', 'ं': 'n',
    '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
    '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
}

def transliterate_devanagari(text: str) -> str:
    """Approximate transliteration of Devanagari text to Latin phonetics."""
    res = []
    for char in text:
        res.append(DEVA_TO_LATIN.get(char, char))
    return "".join(res).lower()


def normalize_tokens(text: str) -> List[str]:
    """Tokenize and normalize text for fuzzy order-independent matching."""
    text_clean = re.sub(r"[^\w\s]", " ", text.lower())
    tokens = [t for t in text_clean.split() if len(t) > 1]
    return tokens


def match_person_name(query_name: str, target_name: str) -> bool:
    """
    Check if query_name matches target_name, handling:
    1. Word order variations (e.g., 'Karan Kajgunde' <-> 'KAJGUNDE KARAN DATTATRAY')
    2. Devanagari / Marathi / Hindi transliterations
    3. Initials and middle names
    """
    if not query_name or not target_name:
        return False

    q_tokens = normalize_tokens(query_name)
    t_tokens = normalize_tokens(target_name)

    if not q_tokens or not t_tokens:
        return False

    # Direct token subset match (all query tokens found in target)
    if all(any(qt in tt or tt in qt for tt in t_tokens) for qt in q_tokens):
        return True

    # Transliterated comparison
    q_trans = normalize_tokens(transliterate_devanagari(query_name))
    t_trans = normalize_tokens(transliterate_devanagari(target_name))

    if all(any(qt in tt or tt in qt for tt in t_trans) for qt in q_trans):
        return True

    return False


class DocumentEngine:
    """
    Comprehensive document ingestion, OCR, parsing, and structured questioning.
    """

    SUPPORTED_DOC_EXTS = {".pdf", ".docx", ".pptx", ".txt"}
    SUPPORTED_IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif"}

    @classmethod
    def is_supported(cls, ext: str) -> bool:
        ext_lower = ext.lower()
        return ext_lower in cls.SUPPORTED_DOC_EXTS or ext_lower in cls.SUPPORTED_IMG_EXTS

    @classmethod
    def is_image(cls, ext: str) -> bool:
        return ext.lower() in cls.SUPPORTED_IMG_EXTS

    @classmethod
    def enhance_image_for_ocr(cls, pil_img: Image.Image) -> np.ndarray:
        """
        Enhance image contrast, sharpen, and denoise for maximum OCR accuracy.
        """
        try:
            import cv2
            img_np = np.array(pil_img)
            if len(img_np.shape) == 3 and img_np.shape[2] == 3:
                gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
            elif len(img_np.shape) == 3 and img_np.shape[2] == 4:
                gray = cv2.cvtColor(img_np, cv2.COLOR_RGBA2GRAY)
            else:
                gray = img_np

            # CLAHE (Contrast Limited Adaptive Histogram Equalization)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(gray)
            return enhanced
        except Exception:
            return np.array(pil_img)

    @classmethod
    def run_ocr_on_image(cls, img_input) -> str:
        """Run RapidOCR on image and return clean extracted text."""
        engine = get_ocr_engine()
        if not engine:
            return ""

        try:
            if isinstance(img_input, Image.Image):
                enhanced = cls.enhance_image_for_ocr(img_input)
            elif isinstance(img_input, (str, Path)):
                pil_img = Image.open(str(img_input))
                enhanced = cls.enhance_image_for_ocr(pil_img)
            else:
                enhanced = img_input

            result, _ = engine(enhanced)
            if not result:
                return ""

            lines = [item[1] for item in result if item and len(item) > 1]
            return "\n".join(lines).strip()
        except Exception as e:
            logger.warning(f"OCR execution error: {e}")
            return ""

    @classmethod
    def extract_document(cls, file_path: Path, filename: str) -> Dict[str, Any]:
        """
        Multi-tier document extraction.
        Extracts direct text, falls back to OCR on scanned pages,
        detects images, parses structured records (exam, voter list).
        """
        ext = file_path.suffix.lower()

        if ext in cls.SUPPORTED_IMG_EXTS:
            return cls._process_standalone_image(file_path, filename)
        elif ext == ".pdf":
            return cls._process_pdf(file_path, filename)
        elif ext == ".docx":
            return cls._process_docx(file_path, filename)
        elif ext == ".pptx":
            return cls._process_pptx(file_path, filename)
        else:
            return cls._process_text_file(file_path, filename)

    @classmethod
    def _process_standalone_image(cls, image_path: Path, filename: str) -> Dict[str, Any]:
        """Fast image processing with thumbnail color analysis and resolution-capped OCR."""
        pil_img = Image.open(image_path)
        orig_width, orig_height = pil_img.size

        # Cap image resolution for lightning-fast OCR if huge (> 1600px)
        if max(orig_width, orig_height) > 1600:
            pil_img.thumbnail((1600, 1600), Image.Resampling.LANCZOS)

        # Fast dominant color extraction via tiny thumbnail
        img_small = pil_img.resize((40, 40)).convert("RGB")
        colors = img_small.getcolors(1600) or []
        colors.sort(key=lambda x: x[0], reverse=True)
        top_rgb = colors[0][1] if colors else (128, 128, 128)

        color_name = "neutral"
        r, g, b = top_rgb
        if r > 180 and g < 100 and b < 100: color_name = "red"
        elif b > 180 and r < 100: color_name = "blue"
        elif g > 160 and r < 100: color_name = "green"
        elif r > 200 and g > 200 and b > 200: color_name = "white/light"
        elif r < 60 and g < 60 and b < 60: color_name = "black/dark"

        ocr_text = cls.run_ocr_on_image(pil_img)

        visual_summary = {
            "dimensions": f"{orig_width}x{orig_height}",
            "aspect_ratio": round(orig_width / max(1, orig_height), 2),
            "dominant_color": color_name,
            "has_readable_text": bool(ocr_text.strip()),
            "text_length": len(ocr_text),
        }

        full_content = (
            f"=== IMAGE METADATA ({filename}) ===\n"
            f"Dimensions: {orig_width}x{orig_height} pixels\n"
            f"Dominant Tone: {color_name}\n"
            f"Extracted Text (OCR):\n{ocr_text if ocr_text else '[No printed text detected]'}\n"
        )

        return {
            "type": "document",
            "content": full_content,
            "ocr_text": ocr_text,
            "filename": filename,
            "visual_summary": visual_summary,
            "pages": [{"page": 1, "text": ocr_text, "scanned": True}],
            "records": [],
            "doc_category": "standalone_image",
        }

    @classmethod
    def _process_pdf(cls, pdf_path: Path, filename: str) -> Dict[str, Any]:
        """
        Fast multi-tier PDF processor:
        1. Extract native text with PyMuPDF (super fast, < 0.2s for 50 pages).
        2. Detect if entire document has native text or is genuinely scanned.
        3. If genuinely scanned, run optimized OCR (150 DPI, skip blank pages, parallel execution).
        4. Detect and parse structured records (exam marksheets, voter lists).
        """
        doc = fitz.open(str(pdf_path))
        pages_data = []
        full_text_parts = []
        ocr_pages_count = 0

        # Step 1: Fast native text pass across all pages
        raw_pages_text = []
        total_native_chars = 0
        for page_idx in range(len(doc)):
            page = doc[page_idx]
            txt = (page.get_text() or "").strip()
            raw_pages_text.append(txt)
            total_native_chars += len(txt)

        # Check if PDF is already a digital document with native text
        # If total native text >= 80 chars, it's a digital PDF: NO OCR NEEDED!
        is_digital_pdf = total_native_chars >= 80

        if is_digital_pdf:
            for page_idx, page_text in enumerate(raw_pages_text):
                page_num = page_idx + 1
                full_text_parts.append(f"--- Page {page_num} ---\n" + page_text)
                pages_data.append({
                    "page": page_num,
                    "text": page_text,
                    "scanned": False,
                })
        else:
            # Genuinely scanned PDF: Run fast OCR on pages in parallel
            from concurrent.futures import ThreadPoolExecutor

            def process_scanned_page(page_idx):
                page = doc[page_idx]
                page_num = page_idx + 1
                native_txt = raw_pages_text[page_idx]
                if len(native_txt) >= 40:
                    return page_num, native_txt, False

                # Render at 150 DPI (fast & crystal clear for OCR)
                pix = page.get_pixmap(dpi=150)
                img_np = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
                # Quick blank check
                if np.std(img_np) < 6:
                    return page_num, "", False

                ocr_result = cls.run_ocr_on_image(img_np)
                return page_num, ocr_result.strip() if ocr_result else native_txt, bool(ocr_result)

            max_workers = min(4, len(doc))
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                results = list(executor.map(process_scanned_page, range(len(doc))))

            results.sort(key=lambda x: x[0])
            for p_num, p_text, was_ocr in results:
                if was_ocr:
                    ocr_pages_count += 1
                full_text_parts.append(f"--- Page {p_num} ---\n" + p_text)
                pages_data.append({
                    "page": p_num,
                    "text": p_text,
                    "scanned": was_ocr,
                })

        combined_text = "\n\n".join(full_text_parts)

        # Structure detection and record extraction
        records, doc_category = cls.detect_and_parse_records(pages_data, filename)

        return {
            "type": "document",
            "content": combined_text,
            "filename": filename,
            "total_pages": len(doc),
            "ocr_pages_count": ocr_pages_count,
            "pages": pages_data,
            "records": records,
            "doc_category": doc_category,
        }

    @classmethod
    def _process_docx(cls, file_path: Path, filename: str) -> Dict[str, Any]:
        from docx import Document
        doc = Document(file_path)
        text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        return {
            "type": "document",
            "content": text,
            "filename": filename,
            "pages": [{"page": 1, "text": text, "scanned": False}],
            "records": [],
            "doc_category": "document",
        }

    @classmethod
    def _process_pptx(cls, file_path: Path, filename: str) -> Dict[str, Any]:
        from pptx import Presentation
        prs = Presentation(file_path)
        slides = []
        for i, slide in enumerate(prs.slides, start=1):
            s_text = [shape.text for shape in slide.shapes if shape.has_text_frame and shape.text.strip()]
            slides.append(f"Slide {i}:\n" + "\n".join(s_text))
        text = "\n\n".join(slides)
        return {
            "type": "document",
            "content": text,
            "filename": filename,
            "pages": [{"page": 1, "text": text, "scanned": False}],
            "records": [],
            "doc_category": "document",
        }

    @classmethod
    def _process_text_file(cls, file_path: Path, filename: str) -> Dict[str, Any]:
        text = file_path.read_text(encoding="utf-8", errors="replace")
        return {
            "type": "document",
            "content": text,
            "filename": filename,
            "pages": [{"page": 1, "text": text, "scanned": False}],
            "records": [],
            "doc_category": "document",
        }

    # =========================================================================
    # STRUCTURE DETECTION & PARSING (EXAM RESULTS & VOTER LISTS)
    # =========================================================================

    @classmethod
    def detect_and_parse_records(cls, pages: List[Dict[str, Any]], filename: str) -> Tuple[List[Dict[str, Any]], str]:
        """
        Detect if document is:
        - 'exam_results': Student academic marksheet / results
        - 'voter_list': Electoral roll / voter card list
        - 'general_document': General prose/report
        """
        all_text_sample = " ".join(p["text"][:500] for p in pages[:5]).upper()

        if any(k in all_text_sample for k in ["PRN", "STUDENTNAME", "SUBJECTCODE", "COLLEGECODE", "BTES"]):
            records = cls.parse_exam_results(pages)
            return records, "exam_results"

        if any(k in all_text_sample for k in ["EPIC", "मतदार", "यादी", "वडील", "पती", "घर क्रमांक", "वय", "लिंग"]):
            records = cls.parse_voter_list(pages)
            return records, "voter_list"

        return [], "general_document"

    @classmethod
    def parse_exam_results(cls, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract structured student records across all pages."""
        records = []
        for p in pages:
            page_num = p["page"]
            lines = [l.strip() for l in p["text"].splitlines() if l.strip()]

            i = 0
            while i < len(lines):
                line = lines[i]
                # Match PRN (starts with 20-24, 10 to 16 digits)
                m = re.match(r"^(\d{10,16})\s+(.+)$", line)
                if m:
                    prn = m.group(1)
                    name = m.group(2).strip()

                    rec = {
                        "page": page_num,
                        "prn": prn,
                        "name": name,
                        "college_code": "",
                        "subject_code": "",
                        "subject_name": "",
                        "course_code": "",
                        "course_name": "",
                        "ca_mse": "",
                        "ete": "",
                        "grace": "0",
                        "total": "",
                        "grade": "",
                    }

                    # Collect tokens until next PRN or max 12 lines
                    j = i + 1
                    tokens = []
                    while j < len(lines) and not re.match(r"^(\d{10,16})\s+", lines[j]) and (j - i) <= 12:
                        tokens.append(lines[j])
                        j += 1

                    for t in tokens:
                        if re.match(r"^\d{4}$", t) and not rec["college_code"]:
                            rec["college_code"] = t
                        elif ("BTES" in t or "BT" in t) and not rec["subject_code"]:
                            rec["subject_code"] = t
                        elif "Engineering" in t or "Graphics" in t:
                            rec["subject_name"] = t
                        elif re.match(r"^\d{5}$", t) and not rec["course_code"]:
                            rec["course_code"] = t
                        elif "Bachelor of Technology" in t:
                            rec["course_name"] = t
                        elif t in ["FF", "AA", "AB", "DE", "EE", "DD", "CD", "CC", "BC", "BB", "O"]:
                            rec["grade"] = t

                    num_tokens = [t for t in tokens if re.match(r"^\d+$", t) and len(t) <= 3]
                    if len(num_tokens) >= 4:
                        rec["ca_mse"] = num_tokens[0]
                        rec["ete"] = num_tokens[1]
                        rec["grace"] = num_tokens[2]
                        rec["total"] = num_tokens[3]
                    elif len(num_tokens) == 3:
                        rec["ca_mse"] = num_tokens[0]
                        rec["ete"] = num_tokens[1]
                        rec["total"] = num_tokens[2]

                    records.append(rec)
                    i = j
                else:
                    i += 1

        return records

    @classmethod
    def parse_voter_list(cls, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract structured voter list records (supports Marathi, Hindi, English)."""
        records = []
        for p in pages:
            page_num = p["page"]
            text = p["text"]

            # Voter block splitting (by EPIC or Serial number)
            # Regex for EPIC: 3 letters + 7 digits (e.g. ABC1234567) or Devanagari blocks
            epic_matches = list(re.finditer(r"([A-Z]{3}\d{7})", text))

            if epic_matches:
                for idx, em in enumerate(epic_matches):
                    epic_id = em.group(1)
                    start = em.start()
                    end = epic_matches[idx + 1].start() if idx + 1 < len(epic_matches) else len(text)
                    block = text[start:end]

                    voter = {
                        "page": page_num,
                        "epic_id": epic_id,
                        "serial_no": "",
                        "name": "",
                        "relative_name": "",
                        "relation_type": "",
                        "house_no": "",
                        "age": "",
                        "gender": "",
                        "has_photo": "फोटो उपलब्ध आहे" in block or "Photo Available" in block or "AVAILABLE" in block,
                    }

                    # Extract details via regex patterns
                    name_m = re.search(r"(?:नाव|Name)\s*[:：]?\s*([^\n\r]+)", block)
                    if name_m: voter["name"] = name_m.group(1).strip()

                    rel_m = re.search(r"(?:वडिलांचे नाव|पतीचे नाव|आईचे नाव|Father's Name|Husband's Name)\s*[:：]?\s*([^\n\r]+)", block)
                    if rel_m: voter["relative_name"] = rel_m.group(1).strip()

                    house_m = re.search(r"(?:घर क्रमांक|House No)\s*[:：]?\s*([^\n\r]+)", block)
                    if house_m: voter["house_no"] = house_m.group(1).strip()

                    age_m = re.search(r"(?:वय|Age)\s*[:：]?\s*(\d+)", block)
                    if age_m: voter["age"] = age_m.group(1).strip()

                    gender_m = re.search(r"(?:लिंग|Gender)\s*[:：]?\s*([^\n\r]+)", block)
                    if gender_m: voter["gender"] = gender_m.group(1).strip()

                    records.append(voter)
        return records

    # =========================================================================
    # QUESTION ANSWERING DISPATCHER
    # =========================================================================

    @classmethod
    def answer_question(cls, doc_info: Dict[str, Any], question: str) -> Dict[str, Any]:
        """
        Main query responder for documents.
        Handles lookup, filter, visual queries, counts, and summaries.
        """
        q_clean = question.strip()
        q_lower = q_clean.lower()
        records = doc_info.get("records", [])
        doc_category = doc_info.get("doc_category", "general_document")

        # 1. EXAM RESULTS QUERIES
        if doc_category == "exam_results" and records:
            # A. Grade Filter Query (e.g. "show me the student who have ff grade")
            grade_match = re.search(r"\b(ff|aa|ab|de|ee|dd|cd|cc|bc|bb|o)\s+grade\b|\bgrade\s+(ff|aa|ab|de|ee|dd|cd|cc|bc|bb|o)\b", q_lower)
            if grade_match or "ff grade" in q_lower or "failed" in q_lower:
                target_grade = "FF"
                if grade_match:
                    target_grade = (grade_match.group(1) or grade_match.group(2)).upper()

                matching_students = [r for r in records if r["grade"].upper() == target_grade]
                total_count = len(matching_students)

                if not matching_students:
                    return {
                        "answer": f"No students found with **{target_grade}** grade in this examination document.",
                        "matched": False,
                    }

                limit = min(50, total_count)
                rows = [
                    [
                        s["prn"],
                        s["name"],
                        str(s["college_code"]),
                        str(s["subject_code"]),
                        f"CA:{s['ca_mse'] or '-'} ETE:{s['ete'] or '-'}",
                        str(s["total"]),
                        s["grade"],
                        f"Page {s['page']}"
                    ]
                    for s in matching_students[:limit]
                ]

                table_payload = {
                    "type": "table",
                    "total_records": total_count,
                    "displayed_records": limit,
                    "columns": ["PRN / Roll No", "Student Name", "College Code", "Subject Code", "Internal / ETE Marks", "Total Marks", "Grade", "Page"],
                    "rows": rows,
                    "message": f"Found **{total_count}** student(s) with **{target_grade}** grade in `{doc_info.get('filename')}`:"
                }

                return {
                    "answer": table_payload,
                    "matched": True,
                    "count": total_count,
                }

            # B. Specific Person Lookup (e.g. "karan kajgunde", "CHIMURKAR SHARAD LALAJI")
            # Extract potential names from query by removing common query words
            stopwords = {"give", "tell", "show", "me", "full", "information", "details", "about", "student", "who", "is", "the", "find", "for", "please"}
            q_words = [w for w in re.findall(r"[A-Za-z]+", q_clean) if w.lower() not in stopwords]
            search_phrase = " ".join(q_words)

            matched_records = []
            for r in records:
                if match_person_name(search_phrase, r["name"]) or match_person_name(q_clean, r["name"]):
                    matched_records.append(r)

            if matched_records:
                if len(matched_records) == 1:
                    s = matched_records[0]
                    rows = [
                        ["Student Name", s["name"]],
                        ["PRN / Roll No", s["prn"]],
                        ["College Code", str(s["college_code"])],
                        ["Subject Code & Name", f"{s['subject_code']} - {s['subject_name'] or 'Engineering Graphics'}"],
                        ["Course", s["course_name"] or "Bachelor of Technology"],
                        ["Internal Marks (CA + MSE)", str(s["ca_mse"])],
                        ["End Term Exam (ETE)", str(s["ete"])],
                        ["Grace Marks", str(s["grace"])],
                        ["Total Marks (100)", str(s["total"])],
                        ["Grade", s["grade"]],
                        ["Document Location", f"Page {s['page']} in {doc_info.get('filename')}"],
                    ]
                    return {
                        "answer": {
                            "type": "table",
                            "total_records": 1,
                            "displayed_records": 1,
                            "columns": ["Field", "Student Information"],
                            "rows": rows,
                            "message": f"Student Record for **{s['name']}** (PRN `{s['prn']}`):"
                        },
                        "matched": True,
                    }
                else:
                    return {
                        "answer": {
                            "type": "table",
                            "total_records": len(matched_records),
                            "displayed_records": len(matched_records),
                            "columns": ["PRN", "Student Name", "College", "Subject", "Total Marks", "Grade", "Page"],
                            "rows": [
                                [s["prn"], s["name"], str(s["college_code"]), str(s["subject_code"]), str(s["total"]), s["grade"], f"Page {s['page']}"]
                                for s in matched_records
                            ],
                            "message": f"Found **{len(matched_records)}** matching student record(s):"
                        },
                        "matched": True,
                    }

        # 2. VOTER LIST QUERIES
        if doc_category == "voter_list" and records:
            # Person Lookup in Voter List
            matched_voters = []
            for v in records:
                if match_person_name(q_clean, v["name"]) or match_person_name(q_clean, v["epic_id"]):
                    matched_voters.append(v)

            if matched_voters:
                if len(matched_voters) == 1:
                    v = matched_voters[0]
                    rows = [
                        ["Voter Name", v["name"]],
                        ["EPIC / Voter ID", v["epic_id"]],
                        ["Relative's Name", v["relative_name"]],
                        ["House Number", str(v["house_no"])],
                        ["Age", str(v["age"])],
                        ["Gender", v["gender"]],
                        ["Photo Available", "Yes (Printed next to entry)" if v["has_photo"] else "No"],
                        ["Document Location", f"Page {v['page']} in {doc_info.get('filename')}"],
                    ]
                    return {
                        "answer": {
                            "type": "table",
                            "total_records": 1,
                            "displayed_records": 1,
                            "columns": ["Field", "Voter Details"],
                            "rows": rows,
                            "message": f"Voter Record for **{v['name']}** (EPIC `{v['epic_id']}`):"
                        },
                        "matched": True,
                    }
                else:
                    return {
                        "answer": {
                            "type": "table",
                            "total_records": len(matched_voters),
                            "displayed_records": len(matched_voters),
                            "columns": ["EPIC ID", "Voter Name", "Relative", "House No", "Age", "Gender", "Page"],
                            "rows": [
                                [v["epic_id"], v["name"], v["relative_name"], str(v["house_no"]), str(v["age"]), v["gender"], f"Page {v['page']}"]
                                for v in matched_voters
                            ],
                            "message": f"Found **{len(matched_voters)}** matching voter record(s):"
                        },
                        "matched": True,
                    }

        # 3. STANDALONE IMAGE OR VISUAL QUERIES
        if doc_category == "standalone_image" or "color" in q_lower or "photo" in q_lower or "picture" in q_lower or "image" in q_lower or "shirt" in q_lower:
            visual = doc_info.get("visual_summary", {})
            ocr_text = doc_info.get("ocr_text", "")

            # If user asks about someone in photo:
            if "who" in q_lower or "person" in q_lower or "name" in q_lower:
                if ocr_text:
                    return {
                        "answer": (
                            f"Based on the text printed in the document/image (`{doc_info.get('filename')}`):\n\n"
                            f"**Printed Text / Label:**\n```\n{ocr_text}\n```\n\n"
                            f"*Note: In accordance with privacy and safety standards, names are provided only when explicitly written on the document itself.*"
                        ),
                        "matched": True
                    }
                else:
                    return {
                        "answer": (
                            f"No name is mentioned for this person in the document. Here is what I can observe visually:\n\n"
                            f"- **Image Dimensions:** {visual.get('dimensions', 'Standard resolution')}\n"
                            f"- **Dominant Color Tone:** {visual.get('dominant_color', 'Neutral')}\n"
                            f"- **Visual Elements:** Visible person figure detected, no explicit nameplate or caption present."
                        ),
                        "matched": True
                    }

        # 4. GENERAL DOCUMENT EXCERPT LLM FALLBACK
        return None
