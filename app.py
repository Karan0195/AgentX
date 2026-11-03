
import sys
import os
from pathlib import Path

# Auto-bootstrap: ensure execution under the project's virtual environment (.venv)
_project_dir = Path(__file__).resolve().parent
os.environ.setdefault("MPLCONFIGDIR", str(_project_dir / "data" / ".matplotlib"))
_venv_python = _project_dir / ".venv" / "Scripts" / "python.exe"
_venv_site = _project_dir / ".venv" / "Lib" / "site-packages"

if _venv_site.exists() and str(_venv_site) not in sys.path:
    sys.path.insert(0, str(_venv_site))

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

if __name__ == "__main__" and _venv_python.exists() and Path(sys.executable).resolve() != _venv_python.resolve():
    import subprocess
    try:
        sys.exit(subprocess.call([str(_venv_python)] + sys.argv))
    except KeyboardInterrupt:
        sys.exit(0)

from dotenv import load_dotenv
load_dotenv(_project_dir / ".env")

from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    send_from_directory,
    Response,
    session,
    redirect,
    url_for,
)
from functools import wraps
import os
import re
from pathlib import Path
import pandas as pd
import uuid
import json
import io

from pypdf import PdfReader
from docx import Document
from pptx import Presentation

from agents.analyst_agent import AnalystAgent
from agents.visualization_agent import VisualizationAgent
from agents.orchestrator import Orchestrator
from agents.report_agent import ReportAgent
from utils.data_engine import DataEngine
from utils.document_engine import DocumentEngine
from utils.auth_db import (
    init_db,
    register_user,
    authenticate_user,
    reset_user_password,
    get_user_by_id,
    create_conversation,
    get_user_conversations,
    get_conversation,
    get_conversation_messages,
    add_message,
    delete_conversation,
    update_conversation_title,
    save_dataset_record,
    get_dataset_record,
    update_conversation_dataset,
)


from flask.json.provider import DefaultJSONProvider

class SafeRFC8259JSONProvider(DefaultJSONProvider):
    def dumps(self, obj, **kwargs):
        sanitized = DataEngine.sanitize_for_json(obj)
        kwargs["allow_nan"] = False
        return json.dumps(sanitized, **kwargs)

app = Flask(__name__)
app.json_provider_class = SafeRFC8259JSONProvider
app.json = SafeRFC8259JSONProvider(app)
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024
app.secret_key = os.getenv("SECRET_KEY", "agentx-super-secret-key-prod-2026")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

PROJECT_ROOT = Path(__file__).resolve().parent

# Initialize SQLite user database
init_db()

UPLOAD_DIR = (PROJECT_ROOT / "uploads").resolve()
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

datasets = {}
conversations = {}

orchestrator = Orchestrator()
report_agent = ReportAgent()

CHARTS_DIR = (PROJECT_ROOT / "charts").resolve()
CHARTS_DIR.mkdir(parents=True, exist_ok=True)


def generate_doc_suggested_questions(doc_category: str, records: list) -> list:
    """Generate domain-specific questions for document / multimodal files."""
    if doc_category == "exam_results":
        questions = [
            "Show me the students who have FF grade",
            "Total student records in this sheet",
        ]
        if records:
            names = [r.get("name") for r in records if r.get("name")]
            if names:
                questions.append(f"Give full details about {names[0]}")
                if len(names) > 3:
                    questions.append(f"Give full details about {names[3]}")
        questions.append("Show grade distribution of students")
        return questions[:5]

    if doc_category == "voter_list":
        questions = [
            "How many total registered voters in this list?",
            "List all female voters",
            "Show voters with age above 60",
            "Voters distribution grouped by house number",
        ]
        if records:
            v_names = [r.get("name") for r in records if r.get("name")]
            if v_names:
                questions.append(f"Search voter details for {v_names[0]}")
        return questions[:5]

    if doc_category == "standalone_image":
        return [
            "What text and details are visible in this image?",
            "Describe the visual elements, people, and colors in this photo",
            "Extract all numbers, dates, or tabular information",
            "Summarize everything shown in this image",
        ]

    return [
        "What is this document about?",
        "Summarize the key findings in this document",
        "List all people, entities, or tables mentioned",
        "Extract any metrics, numbers, or dates in this file",
    ]


def get_or_load_dataset(dataset_id, user_id):
    """
    Retrieve dataset from memory cache or persistently restore from disk/database.
    Ensures datasets survive server restarts, browser closures, and re-logins.
    """
    if not dataset_id or not user_id:
        return None

    # Check in-memory cache
    if dataset_id in datasets:
        item = datasets[dataset_id]
        if item.get("user_id") == user_id:
            return item
        return None

    # Check persistent SQLite storage
    record = get_dataset_record(dataset_id, user_id)
    if not record:
        return None

    filepath = Path(record["filepath"]).resolve()
    if not filepath.is_file():
        return None

    try:
        extension = filepath.suffix.lower()
        content_type = record.get("file_type", "table")
        records = []
        doc_category = "document"
        profile = None
        suggested_q = []

        if extension in {".csv", ".tsv", ".xlsx", ".xls", ".parquet", ".json", ".jsonl"}:
            with open(filepath, "rb") as f:
                content, content_type = read_uploaded_file(f, extension)
            profile = DataEngine.profile_dataset(content, record["filename"], str(filepath))
            suggested_q = profile.get("suggested_questions", [])
        else:
            doc_info = DocumentEngine.extract_document(filepath, record["filename"])
            content = doc_info["content"]
            content_type = "document"
            records = doc_info.get("records", [])
            doc_category = doc_info.get("doc_category", "general_document")
            suggested_q = generate_doc_suggested_questions(doc_category, records)

        item = {
            "user_id": user_id,
            "content": content,
            "type": content_type,
            "filename": record["filename"],
            "filepath": str(filepath),
            "records": records,
            "doc_category": doc_category,
            "rows": record.get("rows", len(records)),
            "columns": record.get("columns", 0),
            "column_names": record.get("column_names", []),
            "profile": profile,
            "suggested_questions": suggested_q,
        }
        # Re-cache in memory
        datasets[dataset_id] = item
        return item
    except Exception:
        app.logger.exception(f"Failed to reload persistent dataset {dataset_id}")
        return None

ALLOWED_EXTENSIONS = {
    ".csv",
    ".tsv",
    ".xlsx",
    ".xls",
    ".json",
    ".jsonl",
    ".parquet",
    ".txt",
    ".xml",
    ".pdf",
    ".docx",
    ".pptx",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".bmp",
    ".tiff",
    ".tif",
}


def format_answer(answer):
    """Preserve structured table and chart responses with complete JSON sanitization."""

    if isinstance(answer, dict):
        return DataEngine.sanitize_for_json(answer)

    if isinstance(answer, str):
        try:
            result = json.loads(answer)
            if isinstance(result, dict) and result.get("type") in {"table", "chart", "scalar"}:
                return DataEngine.sanitize_for_json(result)
        except (ValueError, TypeError):
            pass

    return str(answer)


def read_uploaded_file(file, extension):
    """Read supported tabular and document file formats with encoding and delimiter auto-detection."""

    if extension in {".csv", ".tsv", ".txt"}:
        content_bytes = file.read()
        file.seek(0)
        encoding = DataEngine.detect_encoding(content_bytes)
        sample_text = content_bytes[:8192].decode(encoding, errors="replace")
        delimiter = DataEngine.detect_delimiter(sample_text)
        try:
            df = pd.read_csv(
                io.BytesIO(content_bytes),
                sep=delimiter,
                encoding=encoding,
                low_memory=False,
                on_bad_lines="skip"
            )
            df.columns = [str(c).strip() for c in df.columns]
            return df, "table"
        except Exception:
            df = pd.read_csv(
                io.BytesIO(content_bytes),
                sep=None,
                engine="python",
                encoding="latin-1",
                on_bad_lines="skip"
            )
            df.columns = [str(c).strip() for c in df.columns]
            return df, "table"

    elif extension in {".xlsx", ".xls"}:
        excel_file = pd.ExcelFile(file)
        df = excel_file.parse(excel_file.sheet_names[0])
        df.columns = [str(c).strip() for c in df.columns]
        return df, "table"

    elif extension in {".json", ".jsonl"}:
        content_bytes = file.read()
        file.seek(0)
        encoding = DataEngine.detect_encoding(content_bytes)
        try:
            df = pd.read_json(io.BytesIO(content_bytes), lines=True, encoding=encoding)
            df.columns = [str(c).strip() for c in df.columns]
            return df, "table"
        except Exception:
            try:
                df = pd.read_json(io.BytesIO(content_bytes), encoding=encoding)
                df.columns = [str(c).strip() for c in df.columns]
                return df, "table"
            except Exception:
                data = json.loads(content_bytes.decode(encoding, errors="replace"))
                if isinstance(data, list):
                    df = pd.json_normalize(data)
                elif isinstance(data, dict):
                    df = pd.json_normalize(data.get("data", data.get("records", [data])))
                else:
                    raise ValueError("JSON must contain tabular data.")
                df.columns = [str(c).strip() for c in df.columns]
                return df, "table"

    elif extension == ".parquet":
        df = pd.read_parquet(file)
        df.columns = [str(c).strip() for c in df.columns]
        return df, "table"

    elif extension == ".xml":
        import xml.etree.ElementTree as ET
        try:
            tree = ET.parse(file)
            root = tree.getroot()
            records = []
            for child in root:
                record = {}
                for elem in child:
                    record[elem.tag] = elem.text.strip() if elem.text else ""
                if record:
                    records.append(record)
            if records:
                df = pd.DataFrame(records)
                for col in df.columns:
                    try:
                        converted = pd.to_numeric(df[col])
                        if not converted.isna().all():
                            df[col] = converted
                    except (ValueError, TypeError):
                        pass
                return df, "table"
        except Exception:
            pass
        file.seek(0)
        return file.read().decode("utf-8", errors="replace"), "document"

    elif extension == ".parquet":
        return pd.read_parquet(file), "table"

    elif extension == ".pdf":
        reader = PdfReader(file)
        pages_text = []
        for i, page in enumerate(reader.pages, start=1):
            page_str = (page.extract_text() or "").strip()
            if page_str:
                pages_text.append(f"--- Page {i} ---\n" + page_str)
        text = "\n\n".join(pages_text)
        return text, "document"

    elif extension == ".docx":
        document = Document(file)
        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )
        return text, "document"

    elif extension == ".pptx":
        presentation = Presentation(file)
        slides = []

        for index, slide in enumerate(
            presentation.slides, start=1
        ):
            slide_text = [
                shape.text
                for shape in slide.shapes
                if shape.has_text_frame and shape.text.strip()
            ]

            slides.append(
                f"Slide {index}:\n" + "\n".join(slide_text)
            )

        return "\n\n".join(slides), "document"

    elif extension == ".txt":
        return file.read().decode("utf-8-sig"), "document"

    raise ValueError("Unsupported file format.")


def normalize_name(value):
    """Normalize a column name for question matching."""

    return "".join(
        character
        for character in str(value).casefold()
        if character.isalnum()
    )


def detect_chart_request(question):
    """Check whether the user explicitly requested a chart."""

    question_lower = question.casefold()

    chart_phrases = (
        "chart",
        "plot",
        "visualize",
        "visualise",
        "graph",
        "draw a graph",
        "create a graph",
    )

    return any(
        phrase in question_lower
        for phrase in chart_phrases
    )


def find_column_in_question(columns, question):
    """Find a dataset column explicitly mentioned in a question."""

    normalized_question = normalize_name(question)

    candidates = sorted(
        columns,
        key=lambda column: len(normalize_name(column)),
        reverse=True,
    )

    for column in candidates:
        normalized_column = normalize_name(column)

        if (
            normalized_column
            and normalized_column in normalized_question
        ):
            return column

    return None


def detect_aggregation(question):
    """Determine the requested aggregation for a chart."""

    question_lower = question.casefold()

    if any(
        phrase in question_lower
        for phrase in ("average", "mean", "avg")
    ):
        return "mean"

    if any(
        phrase in question_lower
        for phrase in (
            "count",
            "frequency",
            "number of",
            "how many",
        )
    ):
        return "count"

    if any(
        phrase in question_lower
        for phrase in ("maximum", "highest", "largest")
    ):
        return "max"

    if any(
        phrase in question_lower
        for phrase in ("minimum", "lowest", "smallest")
    ):
        return "min"

    return "sum"


def extract_relevant_document_context(content, question, max_chars=12000):
    """
    Search and retrieve the most relevant sections of a document.
    Ensures long documents (PDFs, voter lists, student examination records)
    are searched end-to-end with line-level precision and table header preservation.
    """
    if not content:
        return ""

    if len(content) <= max_chars:
        return content

    import re

    stopwords = {
        "what", "when", "where", "which", "who", "whom", "whose", "why", "how",
        "is", "are", "was", "were", "the", "a", "an", "this", "that", "these",
        "find", "show", "tell", "me", "about", "give", "details", "information",
        "person", "all", "record", "records", "search", "lookup", "for", "in",
        "can", "you", "please", "profile", "data", "file", "document", "full",
        "student", "info", "result", "results", "marks"
    }

    raw_tokens = re.findall(r"[A-Za-z0-9_-]+", question)
    query_terms = [t for t in raw_tokens if t.lower() not in stopwords and len(t) > 1]
    query_terms_lower = [t.lower() for t in query_terms]

    lines = content.splitlines()

    # 1. Detect column headers from the start of document or pages
    header_lines = []
    for l in lines[:25]:
        l_str = l.strip()
        if (l_str and not l_str.startswith("--- Page")
                and any(h in l_str.lower() for h in [
                    "prn", "name", "student", "roll", "code", "marks",
                    "grade", "total", "college", "subject", "branch", "course"
                ])):
            header_lines.append(l_str)

    header_block = ""
    if header_lines:
        header_block = "=== DOCUMENT COLUMN HEADERS ===\n" + "\n".join(header_lines) + "\n\n"

    # 2. Line-by-line exact and multi-term match (handles student names, PRNs, IDs)
    matched_line_blocks = []
    seen_lines = set()
    current_page_label = "Document"

    for idx, line in enumerate(lines):
        line_strip = line.strip()
        if line_strip.startswith("--- Page "):
            current_page_label = line_strip.strip("- ")
            continue

        if not line_strip or len(line_strip) < 4:
            continue

        line_lower = line_strip.lower()

        # Count how many search tokens appear in this line
        term_matches = sum(1 for t in query_terms_lower if t in line_lower)
        if term_matches > 0:
            ratio = term_matches / len(query_terms_lower) if query_terms_lower else 0
            # Matches all tokens or majority of multi-term query (e.g. both "karan" and "kajgunde")
            if term_matches == len(query_terms_lower) or (len(query_terms_lower) >= 2 and ratio >= 0.5):
                if line_strip not in seen_lines:
                    seen_lines.add(line_strip)
                    # Add line with page label and surrounding context line if available
                    surrounding = []
                    if idx > 0 and lines[idx - 1].strip() and not lines[idx - 1].startswith("--- Page"):
                        surrounding.append(lines[idx - 1].strip())
                    surrounding.append(f"[{current_page_label}]: {line_strip}")
                    if idx + 1 < len(lines) and lines[idx + 1].strip() and not lines[idx + 1].startswith("--- Page"):
                        surrounding.append(lines[idx + 1].strip())
                    matched_line_blocks.append((term_matches, "\n".join(surrounding)))

    # 3. Intelligent Paragraph / Section Chunking
    raw_chunks = [p.strip() for p in re.split(r"\n\s*\n", content) if p.strip()]
    chunks = []
    # If chunks are too large (> 2500 chars) or document has no double newlines, subdivide
    for chunk in raw_chunks:
        if len(chunk) <= 2500:
            chunks.append(chunk)
        else:
            sublines = chunk.splitlines()
            buf = []
            curr_b_len = 0
            for sl in sublines:
                buf.append(sl)
                curr_b_len += len(sl) + 1
                if curr_b_len >= 1800:
                    chunks.append("\n".join(buf))
                    buf = []
                    curr_b_len = 0
            if buf:
                chunks.append("\n".join(buf))

    if not chunks:
        chunk_size = 1500
        chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size - 200)]

    scored_chunks = []
    full_query_lower = " ".join(query_terms_lower)

    for idx, chunk in enumerate(chunks):
        chunk_lower = chunk.lower()
        score = 0
        if full_query_lower and full_query_lower in chunk_lower:
            score += 150

        matched_terms = [t for t in query_terms_lower if t in chunk_lower]
        score += len(matched_terms) * 25
        if len(matched_terms) == len(query_terms_lower) and len(query_terms_lower) > 1:
            score += 100

        if score > 0:
            scored_chunks.append((score, idx, chunk))

    scored_chunks.sort(key=lambda x: x[0], reverse=True)

    selected_blocks = []
    curr_len = len(header_block)

    # First add exact matching records
    if matched_line_blocks:
        matched_line_blocks.sort(key=lambda x: x[0], reverse=True)
        exact_records_str = (
            "=== EXACT MATCHING RECORDS FOUND IN DOCUMENT ===\n"
            + "\n---\n".join(b for _, b in matched_line_blocks[:15])
            + "\n\n"
        )
        selected_blocks.append(exact_records_str)
        curr_len += len(exact_records_str)

    # Then add top scored excerpt chunks
    for s, idx, chunk in scored_chunks:
        if curr_len + len(chunk) > max_chars:
            if not selected_blocks:
                selected_blocks.append(chunk[:max_chars - curr_len])
            break
        selected_blocks.append(f"=== RELEVANT EXCERPT (Section {idx + 1}) ===\n" + chunk)
        curr_len += len(chunk) + 10

    if not selected_blocks:
        return content[:max_chars]

    final_result = header_block + "\n\n".join(selected_blocks)
    return final_result[:max_chars]


def login_required(f):
    """Ensure user is authenticated before accessing protected routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            if request.path.startswith("/api/"):
                return jsonify({
                    "error": "Authentication required. Please sign in to access AgentX.",
                    "redirect": "/login",
                }), 401
            return redirect(url_for("login_page"))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/login")
def login_page():
    """Render dynamic login and registration portal."""
    if request.args.get("switch") or request.args.get("logout"):
        session.clear()
        return render_template("login.html")
    if "user_id" in session and not request.args.get("force"):
        return redirect(url_for("home"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Clear session and log out the user."""
    session.clear()
    return redirect(url_for("login_page"))


@app.route("/api/auth/register", methods=["POST"])
@app.route("/api/auth/signup", methods=["POST"])
@app.route("/api/register", methods=["POST"])
@app.route("/api/signup", methods=["POST"])
def api_register():
    """Register a new user account."""
    body = request.get_json(silent=True) or {}
    username = body.get("username", "")
    email = body.get("email", "")
    password = body.get("password", "")
    full_name = body.get("full_name", "") or username
    remember = body.get("remember", False)

    success, message, user = register_user(username, email, password, full_name)
    if not success:
        return jsonify({
            "success": False,
            "status": "error",
            "error": message,
        }), 400

    session["user_id"] = user["id"]
    session["username"] = user["username"]
    session["email"] = user["email"]
    session.permanent = bool(remember)

    return jsonify({
        "success": True,
        "status": "success",
        "message": message,
        "user": user,
        "redirect": "/",
    })


@app.route("/api/auth/login", methods=["POST"])
@app.route("/api/login", methods=["POST"])
def api_login():
    """Authenticate user credentials."""
    body = request.get_json(silent=True) or {}
    identifier = body.get("identifier", "")
    password = body.get("password", "")
    remember = body.get("remember", False)

    success, message, user = authenticate_user(identifier, password)
    if not success:
        return jsonify({
            "success": False,
            "status": "error",
            "error": message,
        }), 401

    session["user_id"] = user["id"]
    session["username"] = user["username"]
    session["email"] = user["email"]
    session.permanent = bool(remember)

    return jsonify({
        "success": True,
        "status": "success",
        "message": message,
        "user": user,
        "redirect": "/",
    })


@app.route("/api/auth/reset-password", methods=["POST"])
@app.route("/api/reset-password", methods=["POST"])
def api_reset_password():
    """Reset user password by username or email."""
    body = request.get_json(silent=True) or {}
    identifier = body.get("identifier", "")
    new_password = body.get("new_password", "")

    if not identifier or not new_password:
        return jsonify({
            "success": False,
            "status": "error",
            "error": "Please provide your username/email and a new password.",
        }), 400

    success, message = reset_user_password(identifier, new_password)
    if not success:
        return jsonify({
            "success": False,
            "status": "error",
            "error": message,
        }), 400

    return jsonify({
        "success": True,
        "status": "success",
        "message": message,
    })


@app.route("/api/auth/me", methods=["GET"])
def api_current_user():
    """Return currently authenticated user information."""
    if "user_id" not in session:
        return jsonify({"logged_in": False}), 200

    user = get_user_by_id(session["user_id"])
    return jsonify({
        "logged_in": True,
        "user": user or {
            "id": session["user_id"],
            "username": session.get("username", "User"),
            "email": session.get("email", ""),
        }
    })


@app.route("/api/conversations", methods=["GET"])
@login_required
def api_get_conversations():
    """Retrieve all saved conversations for the authenticated user, recent first."""
    user_id = session.get("user_id")
    convs = get_user_conversations(user_id)
    return jsonify({
        "status": "success",
        "conversations": convs,
    })


@app.route("/api/conversations", methods=["POST"])
@login_required
def api_create_conversation():
    """Create a new conversation session for the authenticated user."""
    user_id = session.get("user_id")
    body = request.get_json(silent=True) or {}
    title = body.get("title", "New Chat").strip() or "New Chat"
    dataset_id = body.get("dataset_id")
    conv = create_conversation(user_id, title=title, dataset_id=dataset_id)
    return jsonify({
        "status": "success",
        "conversation": conv,
    }), 201


@app.route("/api/conversations/<conversation_id>", methods=["GET"])
@app.route("/api/conversations/<conversation_id>/messages", methods=["GET"])
@login_required
def api_get_conversation_messages(conversation_id):
    """Retrieve all messages and restore dataset context for a conversation."""
    user_id = session.get("user_id")
    conv = get_conversation(conversation_id, user_id)
    if not conv:
        return jsonify({"error": "Conversation not found or access denied."}), 404

    messages = get_conversation_messages(conversation_id, user_id)

    # Check and restore dataset if associated with this conversation
    dataset_info = None
    if conv.get("dataset_id"):
        loaded_item = get_or_load_dataset(conv["dataset_id"], user_id)
        is_available = loaded_item is not None
        dataset_info = {
            "available": is_available,
            "id": conv["dataset_id"],
            "filename": conv.get("dataset_name") or (loaded_item.get("filename") if loaded_item else "Dataset"),
            "rows": conv.get("dataset_rows") or (loaded_item.get("rows") if loaded_item else 0),
            "columns": conv.get("dataset_columns") or (loaded_item.get("columns") if loaded_item else 0),
            "column_names": conv.get("column_names") or (loaded_item.get("column_names") if loaded_item else []),
        }
        if loaded_item:
            dataset_info["suggested_questions"] = loaded_item.get("suggested_questions", [])
            if not dataset_info["suggested_questions"] and loaded_item.get("profile"):
                dataset_info["suggested_questions"] = loaded_item["profile"].get("suggested_questions", [])
            if loaded_item.get("profile"):
                dataset_info["profile"] = loaded_item["profile"]

    return jsonify(DataEngine.sanitize_for_json({
        "status": "success",
        "id": conv["id"],
        "title": conv.get("title", "Chat"),
        "dataset_id": conv.get("dataset_id"),
        "dataset_name": conv.get("dataset_name"),
        "dataset_rows": conv.get("dataset_rows"),
        "dataset_columns": conv.get("dataset_columns"),
        "column_names": conv.get("column_names", []),
        "suggested_questions": (dataset_info.get("suggested_questions") if dataset_info else []),
        "conversation": conv,
        "messages": messages,
        "dataset": dataset_info,
    }))


@app.route("/api/conversations/<conversation_id>/messages", methods=["POST"])
@login_required
def api_add_conversation_message(conversation_id):
    """Append a message to an existing conversation."""
    user_id = session.get("user_id")
    conv = get_conversation(conversation_id, user_id)
    if not conv:
        return jsonify({"error": "Conversation not found or access denied."}), 404

    body = request.get_json(silent=True) or {}
    role = body.get("role", "user")
    content = body.get("content", "")
    critic = body.get("critic")
    workflow = body.get("workflow")

    msg = add_message(conversation_id, role, content, critic=critic, workflow=workflow)
    return jsonify({
        "status": "success",
        "message": msg,
    }), 201


@app.route("/api/conversations/<conversation_id>", methods=["DELETE"])
@login_required
def api_delete_conversation(conversation_id):
    """Permanently delete a conversation and its messages, verifying user ownership."""
    user_id = session.get("user_id")
    deleted = delete_conversation(conversation_id, user_id)
    if not deleted:
        return jsonify({"error": "Conversation not found or access denied."}), 404

    return jsonify({
        "status": "success",
        "message": "Conversation deleted successfully.",
    })


@app.route("/")
@login_required
def home():
    return render_template("index.html")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "AgentX backend is running",
    })


@app.route("/api/upload", methods=["POST"])
@login_required
def upload_dataset():
    """Upload a dataset, document, or image with multi-tier ingestion."""

    if "file" not in request.files:
        return jsonify({
            "error": "Please select a file.",
        }), 400

    file = request.files["file"]

    if not file.filename:
        return jsonify({
            "error": "No file selected.",
        }), 400

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        return jsonify({
            "error": f"Unsupported file format '{extension}'. Supported formats include CSV, XLSX, Parquet, JSON, PDF, Images (PNG, JPG, WEBP), Word, and PPTX.",
        }), 400

    try:
        dataset_id = str(uuid.uuid4())
        safe_filename = re.sub(r"[^A-Za-z0-9_.-]", "_", file.filename)
        disk_path = UPLOAD_DIR / f"{dataset_id}_{safe_filename}"
        file.seek(0)
        file.save(str(disk_path))

        is_tabular = extension in {".csv", ".tsv", ".xlsx", ".xls", ".parquet", ".json", ".jsonl"}

        if is_tabular:
            content, meta = DataEngine.load_file(disk_path, file.filename)
            content_type = "table"

            if content.empty:
                return jsonify({
                    "error": "The uploaded file contains no data.",
                }), 400

            profile = DataEngine.profile_dataset(content, filename=file.filename, filepath=str(disk_path))
            quality_report = f"Dataset verified: {content.shape[0]:,} rows, {content.shape[1]} columns."

            details = {
                "type": "table",
                "rows": int(content.shape[0]),
                "columns": int(content.shape[1]),
                "column_names": [str(c) for c in content.columns],
                "data_quality_report": quality_report,
                "profile": profile,
                "suggested_questions": profile.get("suggested_questions", []),
            }
            records = []
            doc_category = "tabular"
        else:
            # Multi-tier document & multimodal extraction (fitz + RapidOCR + OpenCV CLAHE + structure parsing)
            doc_info = DocumentEngine.extract_document(disk_path, file.filename)
            content = doc_info.get("content", "")
            content_type = "document"
            records = doc_info.get("records", [])
            doc_category = doc_info.get("doc_category", "general_document")

            if not content.strip() and not records:
                return jsonify({
                    "error": "No readable text or images found in this document. Please upload a clearer copy.",
                }), 400

            # Dynamic suggested questions tailored to content category
            suggested_q = generate_doc_suggested_questions(doc_category, records)

            details = {
                "type": "document",
                "characters": len(content),
                "rows": len(records),
                "columns": 0,
                "column_names": [],
                "doc_category": doc_category,
                "suggested_questions": suggested_q,
            }

        save_dataset_record(
            dataset_id=dataset_id,
            user_id=session.get("user_id"),
            filename=file.filename,
            filepath=str(disk_path),
            file_type=content_type,
            rows=details.get("rows", 0),
            columns=details.get("columns", 0),
            column_names=details.get("column_names", [])
        )

        datasets[dataset_id] = {
            "user_id": session.get("user_id"),
            "content": content,
            "type": content_type,
            "filename": file.filename,
            "filepath": str(disk_path),
            "records": records,
            "doc_category": doc_category,
            "rows": details.get("rows", 0),
            "columns": details.get("columns", 0),
            "column_names": details.get("column_names", []),
            "profile": details.get("profile"),
            "suggested_questions": details.get("suggested_questions", []),
        }

        return jsonify(DataEngine.sanitize_for_json({
            "status": "success",
            "message": "File uploaded and indexed successfully.",
            "dataset_id": dataset_id,
            "filename": file.filename,
            **details,
        }))

    except Exception:
        app.logger.exception("File upload failed")

        return jsonify({
            "error": (
                "Could not process this file. "
                "Check the terminal for details."
            ),
        }), 400


@app.route("/api/ask", methods=["POST"])
@login_required
def ask_question():
    """Answer questions or generate charts via the Orchestrator with persistent chat history."""

    body = request.get_json(silent=True) or {}

    dataset_id = body.get("dataset_id")
    question = body.get("question", "").strip()
    conversation_id = body.get("conversation_id")
    user_id = session.get("user_id")

    # If conversation_id is passed, check if it already has an associated dataset
    conv = None
    if conversation_id:
        conv = get_conversation(conversation_id, user_id)
        if not dataset_id and conv and conv.get("dataset_id"):
            dataset_id = conv["dataset_id"]

    if not dataset_id:
        return jsonify({
            "error": "Please upload a dataset or file first.",
        }), 400

    item = get_or_load_dataset(dataset_id, user_id)
    if not item:
        return jsonify({
            "error": "The dataset for this chat is no longer available. Please upload your dataset above to continue.",
        }), 400

    if not question:
        return jsonify({
            "error": "Please enter a question.",
        }), 400

    # Ensure a valid persistent conversation exists or create one dynamically
    if not conv:
        # Create meaningful conversation title from the first question
        title = question[:36].strip() + ("..." if len(question) > 36 else "")
        conv = create_conversation(
            user_id=user_id,
            title=title,
            dataset_id=dataset_id,
            dataset_name=item.get("filename"),
            dataset_rows=item.get("rows"),
            dataset_columns=item.get("columns"),
            column_names=item.get("column_names"),
            dataset_path=item.get("filepath")
        )
        conversation_id = conv["id"]
    else:
        # If conversation didn't have dataset attached yet, update it
        if not conv.get("dataset_id") or conv.get("dataset_id") != dataset_id:
            update_conversation_dataset(
                conversation_id=conversation_id,
                user_id=user_id,
                dataset_id=dataset_id,
                dataset_name=item.get("filename"),
                dataset_rows=item.get("rows"),
                dataset_columns=item.get("columns"),
                column_names=item.get("column_names"),
                dataset_path=item.get("filepath")
            )

    # Retrieve prior conversation messages from DB for cross-session continuity
    prior_messages = get_conversation_messages(conversation_id, user_id) or []
    history = []
    for i in range(0, len(prior_messages) - 1, 2):
        if prior_messages[i]["role"] == "user" and prior_messages[i + 1]["role"] == "assistant":
            history.append({
                "question": prior_messages[i]["content"],
                "answer": prior_messages[i + 1]["content"],
            })
    if not history and dataset_id in conversations:
        history = conversations[dataset_id]

    try:
        result = orchestrator.process_query(
            item, question, history=history
        )

        answer = format_answer(result["answer"])
        critic = result.get("critic", {})
        workflow = result.get("workflow", [])

        # Persist messages permanently in the SQLite database
        add_message(conversation_id, "user", question)
        add_message(conversation_id, "assistant", answer, critic=critic, workflow=workflow)

        # Store in session conversation history
        if dataset_id not in conversations:
            conversations[dataset_id] = []

        conversations[dataset_id].append({
            "question": question,
            "resolved_question": result.get("resolved_question", question),
            "answer": answer,
            "critic": critic,
            "workflow": workflow,
        })

        return jsonify(DataEngine.sanitize_for_json({
            "status": "success",
            "conversation_id": conversation_id,
            "dataset_id": dataset_id,
            "question": question,
            "resolved_question": result.get("resolved_question", question),
            "answer": answer,
            "critic": critic,
            "workflow": workflow,
            "history": conversations[dataset_id],
        }))

    except Exception:
        app.logger.exception("Question processing failed")

        return jsonify({
            "error": "AgentX could not process this question.",
        }), 500


@app.route("/api/history/<dataset_id>", methods=["GET"])
@login_required
def get_conversation_history(dataset_id):
    """Retrieve full conversation history for a dataset session."""
    if dataset_id not in datasets:
        return jsonify({"error": "Dataset not found."}), 404

    if datasets[dataset_id].get("user_id") != session.get("user_id"):
        return jsonify({"error": "Access denied: dataset belongs to another user account."}), 403

    return jsonify({
        "status": "success",
        "history": conversations.get(dataset_id, []),
    })


@app.route("/api/history/clear", methods=["POST"])
@login_required
def clear_conversation_history():
    """Clear conversation history for a dataset session."""
    body = request.get_json(silent=True) or {}
    dataset_id = body.get("dataset_id")

    if dataset_id and dataset_id in datasets:
        if datasets[dataset_id].get("user_id") != session.get("user_id"):
            return jsonify({"error": "Access denied: dataset belongs to another user account."}), 403
        if dataset_id in conversations:
            conversations[dataset_id] = []

    return jsonify({
        "status": "success",
        "message": "Conversation history cleared successfully.",
    })


@app.route("/api/report/download", methods=["GET"])
@login_required
def download_executive_report():
    """Download executive intelligence report in print/PDF-ready HTML format."""
    dataset_id = request.args.get("dataset_id")

    if not dataset_id or dataset_id not in datasets:
        return jsonify({"error": "Dataset not found. Please upload a file first."}), 404

    item = datasets[dataset_id]
    if item.get("user_id") != session.get("user_id"):
        return jsonify({"error": "Access denied: dataset belongs to another user account."}), 403

    history = conversations.get(dataset_id, [])
    filename = item.get("filename", "Dataset")

    if item["type"] == "table":
        html_report = report_agent.generate_html_report(
            item["content"], filename=filename, history=history
        )
    else:
        html_report = f"""<!DOCTYPE html><html><head><meta charset='UTF-8'><title>AgentX Document Report — {filename}</title>
        <style>body{{font-family:system-ui,-apple-system,sans-serif;padding:40px;background:#f8fafc;color:#1e293b;line-height:1.6;}}
        .box{{max-width:850px;margin:0 auto;background:#fff;padding:40px;border-radius:10px;border:1px solid #e2e8f0;box-shadow:0 4px 20px rgba(0,0,0,0.05);}}
        h1{{color:#1e1b4b;margin-top:0;}}</style></head><body><div class='box'>
        <h1>AgentX Document Intelligence Report</h1>
        <p><strong>File:</strong> {filename}</p>
        <p><strong>Total Characters:</strong> {len(item['content']):,}</p>
        <hr><h2 style='font-size:16px;'>Document Sample</h2>
        <pre style='background:#f1f5f9;padding:15px;border-radius:8px;white-space:pre-wrap;font-size:12px;'>{item['content'][:3000]}</pre>
        </div></body></html>"""

    safe_name = re.sub(r"[^A-Za-z0-9_.-]", "_", Path(filename).stem)
    return Response(
        html_report,
        mimetype="text/html",
        headers={
            "Content-Disposition": f"attachment; filename=AgentX_Executive_Report_{safe_name}.html"
        },
    )


@app.route("/charts/<path:filename>")
def serve_chart(filename):
    """Serve generated chart images."""

    return send_from_directory(
        CHARTS_DIR,
        filename,
    )


@app.errorhandler(413)
def file_too_large(_error):
    return jsonify({
        "error": "File too large. Maximum size is 25 MB.",
    }), 413


if __name__ == "__main__":
    app.run(debug=True)

