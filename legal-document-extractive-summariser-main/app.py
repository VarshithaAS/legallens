from flask import (
    Flask,
    render_template,
    request,
    send_file,
    redirect,
    url_for
)

from werkzeug.utils import secure_filename

import os
import re
import json

from datetime import datetime

from summarizer.document_extractor import (
    extract_document_text
)

from summarizer.preprocessing import (
    preprocess_document
)

from summarizer.tfidf import (
    calculate_tfidf_scores
)

from summarizer.textrank import (
    calculate_textrank_scores
)

from summarizer.keywords import (
    extract_keywords
)

from summarizer.clauses import (
    detect_clauses
)

from summarizer.risk_detector import (
    detect_risks
)

from summarizer.report import (
    create_report
)


# ==========================================
# FLASK APPLICATION
# ==========================================

app = Flask(__name__)


# ==========================================
# FOLDERS
# ==========================================

UPLOAD_FOLDER = os.environ.get(
    "UPLOAD_FOLDER",
    "uploads"
)

REPORT_FOLDER = os.environ.get(
    "REPORT_FOLDER",
    "reports"
)

HISTORY_FOLDER = os.environ.get(
    "HISTORY_FOLDER",
    "history"
)

HISTORY_FILE = os.path.join(
    HISTORY_FOLDER,
    "history.json"
)


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["REPORT_FOLDER"] = REPORT_FOLDER


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)

os.makedirs(
    HISTORY_FOLDER,
    exist_ok=True
)


# ==========================================
# HISTORY
# ==========================================

def load_history():

    if not os.path.exists(HISTORY_FILE):

        return []

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (
        json.JSONDecodeError,
        OSError
    ):

        return []


def save_history(history):

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=4,
            ensure_ascii=False
        )


def add_to_history(
    filename,
    word_count,
    sentence_count,
    summary
):

    history = load_history()

    new_entry = {

        "filename": filename,

        "word_count": word_count,

        "sentence_count": sentence_count,

        "key_sentences": len(summary),

        "date": datetime.now().strftime(
            "%d-%m-%Y %I:%M %p"
        )
    }

    history.insert(
        0,
        new_entry
    )

    history = history[:10]

    save_history(history)


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==========================================
# LOGIN
# ==========================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        if not username or not password:

            return render_template(
                "login.html",
                error=(
                    "Please enter "
                    "username and password."
                )
            )

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "login.html"
    )
# ==========================================
# GUEST MODE
# ==========================================

@app.route("/guest")
def guest():

    return redirect(
        url_for("dashboard")
    )


# ==========================================
# REGISTER
# ==========================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        confirm_password = request.form.get(
            "confirm_password",
            ""
        ).strip()

        if not username:

            return render_template(
                "register.html",
                error="Please enter a username."
            )

        if not password:

            return render_template(
                "register.html",
                error="Please enter a password."
            )

        if password != confirm_password:

            return render_template(
                "register.html",
                error="Passwords do not match."
            )

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html"
    )


# ==========================================
# SUMMARY
# ==========================================

def create_summary(text):

    original_sentences, cleaned_sentences = (
        preprocess_document(text)
    )

    if not original_sentences:

        return []

    tfidf_scores = (
        calculate_tfidf_scores(
            cleaned_sentences
        )
    )

    textrank_scores = (
        calculate_textrank_scores(
            cleaned_sentences
        )
    )

    scored_sentences = []

    for i, sentence in enumerate(
        original_sentences
    ):

        tfidf = tfidf_scores.get(
            i,
            0
        )

        textrank = textrank_scores.get(
            i,
            0
        )

        score = (
            0.5 * tfidf
            +
            0.5 * textrank
        )

        scored_sentences.append(
            (
                score,
                sentence
            )
        )

    scored_sentences.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        sentence
        for score, sentence
        in scored_sentences[:7]
    ]


# ==========================================
# DASHBOARD
# ==========================================

@app.route(
    "/dashboard",
    methods=["GET", "POST"]
)
def dashboard():

    history = load_history()

    if request.method == "POST":

        if "document" not in request.files:

            return render_template(
                "dashboard.html",
                error=(
                    "Please select a document."
                ),
                history=history
            )

        file = request.files["document"]

        if file.filename == "":

            return render_template(
                "dashboard.html",
                error=(
                    "Please select a document."
                ),
                history=history
            )

        # ==================================
        # ALLOWED FILE TYPES
        # ==================================

        allowed_extensions = {

            ".pdf",
            ".docx",
            ".txt"
        }

        extension = os.path.splitext(
            file.filename
        )[1].lower()

        if extension not in allowed_extensions:

            return render_template(
                "dashboard.html",
                error=(
                    "Supported files: "
                    "PDF, DOCX and TXT."
                ),
                history=history
            )

        # ==================================
        # SAVE FILE
        # ==================================

        filename = secure_filename(
            file.filename
        )

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(filepath)

        print(
            "DOCUMENT SAVED:",
            filepath
        )

        # ==================================
        # EXTRACT TEXT
        # ==================================

        text = extract_document_text(
            filepath
        )

        print(
            "EXTRACTED TEXT LENGTH:",
            len(text)
        )

        # ==================================
        # CHECK TEXT
        # ==================================

        if not text.strip():

            return render_template(
                "dashboard.html",
                error=(
                    "No readable text was "
                    "found in this document."
                ),
                history=history
            )

        # ==================================
        # SUMMARY
        # ==================================

        summary = create_summary(
            text
        )

        # ==================================
        # KEYWORDS
        # ==================================

        keywords = extract_keywords(
            text
        )

        # ==================================
        # CLAUSES
        # ==================================

        clauses = detect_clauses(
            text
        )

        # ==================================
        # RISKS
        # ==================================

        risks = detect_risks(
            text
        )

        # ==================================
        # STATISTICS
        # ==================================

        word_count = len(
            re.findall(
                r"\b\w+\b",
                text
            )
        )

        sentence_count = len(
            [
                sentence
                for sentence in re.split(
                    r"(?<=[.!?])\s+",
                    text
                )
                if sentence.strip()
            ]
        )

        # ==================================
        # HISTORY
        # ==================================

        add_to_history(
            filename,
            word_count,
            sentence_count,
            summary
        )

        history = load_history()

        # ==================================
        # DISPLAY
        # ==================================

        return render_template(
            "dashboard.html",

            summary=summary,

            filename=filename,

            keywords=keywords,

            clauses=clauses,

            risks=risks,

            word_count=word_count,

            sentence_count=sentence_count,

            history=history
        )

    return render_template(
        "dashboard.html",
        history=history
    )


# ==========================================
# DOWNLOAD REPORT
# ==========================================

@app.route(
    "/download-report",
    methods=["POST"]
)
def download_report():

    filename = request.form.get(
        "filename",
        "document"
    )

    summary = request.form.getlist(
        "summary"
    )

    keywords = request.form.getlist(
        "keywords"
    )

    clauses = request.form.getlist(
        "clauses"
    )

    # --------------------------------------
    # GET RISKS
    # --------------------------------------

    risks = []

    risk_data = request.form.getlist(
        "risks"
    )

    for risk in risk_data:

        try:

            risk_object = json.loads(
                risk
            )

            if isinstance(
                risk_object,
                dict
            ):

                risks.append(
                    risk_object
                )

        except (
            json.JSONDecodeError,
            TypeError
        ):

            continue

    # --------------------------------------
    # COUNTS
    # --------------------------------------

    word_count = request.form.get(
        "word_count",
        "0"
    )

    sentence_count = request.form.get(
        "sentence_count",
        "0"
    )

    try:

        word_count = int(
            word_count or 0
        )

    except (
        ValueError,
        TypeError
    ):

        word_count = 0

    try:

        sentence_count = int(
            sentence_count or 0
        )

    except (
        ValueError,
        TypeError
    ):

        sentence_count = 0

    # --------------------------------------
    # REPORT FILE
    # --------------------------------------

    report_filename = (
        os.path.splitext(filename)[0]
        + "_LegalLens_Report.pdf"
    )

    report_path = os.path.join(
        app.config["REPORT_FOLDER"],
        report_filename
    )

    # --------------------------------------
    # CREATE REPORT
    # --------------------------------------

    create_report(
        report_path,
        filename,
        summary,
        keywords,
        clauses,
        risks,
        word_count,
        sentence_count
    )

    # --------------------------------------
    # DOWNLOAD
    # --------------------------------------

    return send_file(
        report_path,
        as_attachment=True,
        download_name=report_filename
    )
# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    )