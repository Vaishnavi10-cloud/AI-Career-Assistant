from flask import Flask, render_template, request, redirect, session, send_file
from db import Base, engine, SessionLocal
from ai import analyze_resume
import models

from pypdf import PdfReader
import docx
import json
import pytesseract
import tempfile

from pdf2image import convert_from_bytes

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER


# =========================================
# OCR CONFIGURATION
# =========================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

POPPLER_PATH = (
    r"C:\Users\vaish\Downloads\Release-26.02.0-0"
    r"\poppler-26.02.0\Library\bin"
)


# =========================================
# FLASK APP
# =========================================

app = Flask(__name__)

app.secret_key = "vaish123"


# =========================================
# CREATE DATABASE TABLES
# =========================================

Base.metadata.create_all(bind=engine)


# =========================================
# HOME
# =========================================

@app.route("/")
def home():

    if "user" in session:
        return redirect("/dashboard")

    return redirect("/login")


# =========================================
# SIGNUP
# =========================================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    db = SessionLocal()

    try:

        if request.method == "POST":

            email = request.form.get("email")
            password = request.form.get("password")

            existing_user = db.query(models.User).filter_by(
                email=email
            ).first()

            if existing_user:
                return "User already exists. Please log in."

            user = models.User(
                email=email,
                password=password
            )

            db.add(user)
            db.commit()

            return redirect("/login")

        return render_template("signup.html")

    finally:
        db.close()


# =========================================
# LOGIN
# =========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    db = SessionLocal()

    try:

        if request.method == "POST":

            email = request.form.get("email")
            password = request.form.get("password")

            user = db.query(models.User).filter_by(
                email=email,
                password=password
            ).first()

            if user:

                session["user"] = user.email

                return redirect("/dashboard")

            return "Invalid email or password."

        return render_template("login.html")

    finally:
        db.close()


# =========================================
# DASHBOARD
# =========================================

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    # Check if user is logged in
    if "user" not in session:
        return redirect("/login")

    result = {}

    if request.method == "POST":

        # Get form data
        user_goal = request.form.get(
            "role",
            ""
        ).strip()

        resume_text = request.form.get(
            "resume",
            ""
        ).strip()

        job_description = request.form.get(
            "job_description",
            ""
        ).strip()

        file = request.files.get("file")

        print("\n====================================")
        print("RESUME ANALYSIS STARTED")
        print("====================================")

        print("ROLE:", user_goal)
        print(
            "FILENAME:",
            file.filename if file else "NO FILE"
        )


        # =========================================
        # FILE HANDLING
        # =========================================

        if file and file.filename != "":

            filename = file.filename.lower()


            # =====================================
            # PDF FILE
            # =====================================

            if filename.endswith(".pdf"):

                try:

                    reader = PdfReader(file)

                    text = ""

                    for page in reader.pages:

                        extracted = page.extract_text()

                        if extracted:
                            text += extracted + "\n"

                    resume_text = text.strip()

                    print(
                        "PDF TEXT LENGTH:",
                        len(resume_text)
                    )


                    # =================================
                    # OCR FALLBACK
                    # =================================

                    if len(resume_text) == 0:

                        print(
                            "NO PDF TEXT FOUND."
                        )

                        print(
                            "STARTING OCR..."
                        )

                        # Reset file pointer
                        file.seek(0)

                        pdf_bytes = file.read()

                        images = convert_from_bytes(
                            pdf_bytes,
                            dpi=200,
                            poppler_path=POPPLER_PATH
                        )

                        ocr_text = ""

                        for image in images:

                            page_text = (
                                pytesseract.image_to_string(
                                    image
                                )
                            )

                            ocr_text += page_text
                            ocr_text += "\n"

                        resume_text = (
                            ocr_text.strip()
                        )

                        print(
                            "OCR TEXT LENGTH:",
                            len(resume_text)
                        )


                except Exception as e:

                    print(
                        "PDF/OCR ERROR:",
                        str(e)
                    )

                    result = {
                        "skills": [],
                        "missing_skills": [],
                        "roadmap": [],
                        "interview_questions": [],
                        "resume_improvements": [],
                        "recruiter_action_plan": [],
                        "error": (
                            f"PDF/OCR error: {str(e)}"
                        )
                    }


            # =====================================
            # DOCX FILE
            # =====================================

            elif filename.endswith(".docx"):

                try:

                    doc = docx.Document(file)

                    text = ""

                    for para in doc.paragraphs:

                        text += para.text + "\n"

                    resume_text = text.strip()

                    print(
                        "DOCX TEXT LENGTH:",
                        len(resume_text)
                    )


                except Exception as e:

                    print(
                        "DOCX ERROR:",
                        str(e)
                    )

                    result = {
                        "skills": [],
                        "missing_skills": [],
                        "roadmap": [],
                        "interview_questions": [],
                        "resume_improvements": [],
                        "recruiter_action_plan": [],
                        "error": (
                            f"DOCX error: {str(e)}"
                        )
                    }


            # =====================================
            # INVALID FILE
            # =====================================

            else:

                result = {
                    "skills": [],
                    "missing_skills": [],
                    "roadmap": [],
                    "interview_questions": [],
                    "resume_improvements": [],
                    "recruiter_action_plan": [],
                    "error": (
                        "Please upload a PDF or DOCX file."
                    )
                }


        # =========================================
        # AI ANALYSIS
        # =========================================

        if (
            resume_text
            and user_goal
            and not result.get("error")
        ):

            try:

                print("\nCALLING OPENAI...")

                print(
                    "ROLE:",
                    user_goal
                )

                print(
                    "RESUME LENGTH:",
                    len(resume_text)
                )

                print(
                    "JOB DESCRIPTION LENGTH:",
                    len(job_description)
                )


                # Call AI function
                result = analyze_resume(
                    resume_text,
                    user_goal,
                    job_description
                )

                print(
                    "AI ANALYSIS COMPLETED"
                )


                # =================================
                # SAVE REPORT
                # =================================

                db = SessionLocal()

                try:

                    user = db.query(
                        models.User
                    ).filter_by(
                        email=session["user"]
                    ).first()

                    if user:

                        report = models.Reports(
                            user_id=user.id,
                            resume_text=resume_text,
                            result=json.dumps(result)
                        )

                        db.add(report)

                        db.commit()

                        print(
                            "REPORT SAVED TO DATABASE"
                        )

                finally:
                    db.close()


            except Exception as e:

                print(
                    "AI ERROR:",
                    str(e)
                )

                result = {
                    "skills": [],
                    "missing_skills": [],
                    "roadmap": [],
                    "interview_questions": [],
                    "resume_improvements": [],
                    "recruiter_action_plan": [],
                    "error": (
                        f"AI analysis error: {str(e)}"
                    )
                }


        # =========================================
        # EMPTY RESUME OR ROLE
        # =========================================

        elif not result.get("error"):

            result = {
                "skills": [],
                "missing_skills": [],
                "roadmap": [],
                "interview_questions": [],
                "resume_improvements": [],
                "recruiter_action_plan": [],
                "error": (
                    "Please enter your resume or upload "
                    "a resume file and enter a target role."
                )
            }


    return render_template(
        "dashboard.html",
        user=session["user"],
        result=result
    )


# =========================================
# HISTORY
# =========================================

@app.route("/history")
def history():

    if "user" not in session:
        return redirect("/login")

    db = SessionLocal()

    try:

        user = db.query(
            models.User
        ).filter_by(
            email=session["user"]
        ).first()

        if not user:
            return redirect("/login")


        reports = db.query(
            models.Reports
        ).filter_by(
            user_id=user.id
        ).all()


        parsed_reports = []


        for report in reports:

            try:

                parsed_result = json.loads(
                    report.result
                )

            except Exception:

                parsed_result = {}


            parsed_reports.append({
                "resume": report.resume_text,
                "result": parsed_result
            })


        return render_template(
            "history.html",
            reports=parsed_reports
        )


    finally:
        db.close()


# =========================================
# DOWNLOAD PDF REPORT
# =========================================

@app.route("/download-report")
def download_report():

    # Check login
    if "user" not in session:
        return redirect("/login")


    db = SessionLocal()

    try:

        # Get current user
        user = db.query(
            models.User
        ).filter_by(
            email=session["user"]
        ).first()


        if not user:
            return redirect("/login")


        # Get latest analysis report
        report = db.query(
            models.Reports
        ).filter_by(
            user_id=user.id
        ).order_by(
            models.Reports.id.desc()
        ).first()


        if not report:

            return (
                "No analysis report found. "
                "Please analyze a resume first."
            )


        # Convert JSON to dictionary
        result = json.loads(
            report.result
        )


    finally:
        db.close()


    # =========================================
    # CREATE TEMPORARY PDF
    # =========================================

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    file_path = temp_file.name

    temp_file.close()


    # =========================================
    # CREATE PDF DOCUMENT
    # =========================================

    pdf = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )


    # =========================================
    # PDF STYLES
    # =========================================

    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(

        "CustomTitle",

        parent=styles["Title"],

        fontName="Helvetica-Bold",

        fontSize=22,

        leading=28,

        textColor=colors.HexColor(
            "#2F5D50"
        ),

        alignment=TA_CENTER,

        spaceAfter=10
    )


    subtitle_style = ParagraphStyle(

        "Subtitle",

        parent=styles["Normal"],

        fontName="Helvetica",

        fontSize=10,

        leading=15,

        textColor=colors.HexColor(
            "#6B716C"
        ),

        alignment=TA_CENTER,

        spaceAfter=25
    )


    heading_style = ParagraphStyle(

        "CustomHeading",

        parent=styles["Heading2"],

        fontName="Helvetica-Bold",

        fontSize=15,

        leading=20,

        textColor=colors.HexColor(
            "#2F5D50"
        ),

        spaceBefore=18,

        spaceAfter=10
    )


    subheading_style = ParagraphStyle(

        "CustomSubHeading",

        parent=styles["Heading3"],

        fontName="Helvetica-Bold",

        fontSize=12,

        leading=16,

        textColor=colors.HexColor(
            "#1E2A24"
        ),

        spaceBefore=12,

        spaceAfter=8
    )


    normal_style = ParagraphStyle(

        "CustomNormal",

        parent=styles["Normal"],

        fontName="Helvetica",

        fontSize=10,

        leading=16,

        textColor=colors.HexColor(
            "#39413C"
        ),

        spaceAfter=5
    )


    story = []


    # =========================================
    # PDF TITLE
    # =========================================

    story.append(

        Paragraph(
            "AI Career Assistant",
            title_style
        )
    )


    story.append(

        Paragraph(
            "Personalized Resume Analysis Report",
            subtitle_style
        )
    )


    # =========================================
    # RESUME SCORE
    # =========================================

    score = result.get(
        "resume_score",
        0
    )


    score_table = Table(

        [
            ["RESUME STRENGTH SCORE"],
            [f"{score}/100"]
        ],

        colWidths=[500]
    )


    score_table.setStyle(

        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                colors.HexColor(
                    "#EFEBE1"
                )
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.HexColor(
                    "#1E2A24"
                )
            ),

            (
                "TEXTCOLOR",
                (0, 1),
                (-1, 1),
                colors.HexColor(
                    "#2F5D50"
                )
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "FONTNAME",
                (0, 1),
                (-1, 1),
                "Helvetica-Bold"
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, 0),
                11
            ),

            (
                "FONTSIZE",
                (0, 1),
                (-1, 1),
                28
            ),

            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "BOX",
                (0, 0),
                (-1, -1),
                1,
                colors.HexColor(
                    "#DCD5C4"
                )
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                14
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                14
            )

        ])
    )


    story.append(
        score_table
    )

    story.append(
        Spacer(1, 22)
    )


    # =========================================
    # HELPER FUNCTION
    # =========================================

    def add_list_section(
        title,
        items,
        numbered=False
    ):

        if not items:
            return


        story.append(

            Paragraph(
                title,
                heading_style
            )
        )


        for index, item in enumerate(
            items,
            start=1
        ):

            if numbered:

                text = (
                    f"{index}. {item}"
                )

            else:

                text = (
                    f"• {item}"
                )


            story.append(

                Paragraph(
                    text,
                    normal_style
                )
            )


        story.append(
            Spacer(1, 8)
        )


    # =========================================
    # SKILLS
    # =========================================

    add_list_section(

        "Skills",

        result.get(
            "skills",
            []
        )
    )


    # =========================================
    # MISSING SKILLS
    # =========================================

    add_list_section(

        "Missing Skills",

        result.get(
            "missing_skills",
            []
        )
    )


    # =========================================
    # ROADMAP
    # =========================================

    add_list_section(

        "Career Roadmap",

        result.get(
            "roadmap",
            []
        ),

        numbered=True
    )


    # =========================================
    # INTERVIEW QUESTIONS
    # =========================================

    add_list_section(

        "Interview Questions",

        result.get(
            "interview_questions",
            []
        ),

        numbered=True
    )


    # =========================================
    # RESUME IMPROVEMENTS
    # =========================================

    add_list_section(

        "How to Improve Your Resume",

        result.get(
            "resume_improvements",
            []
        )
    )


    # =========================================
    # RECRUITER ACTION PLAN
    # =========================================

    add_list_section(

        "Recruiter Action Plan",

        result.get(
            "recruiter_action_plan",
            []
        ),

        numbered=True
    )


    # =========================================
    # JOB MATCH ANALYSIS
    # =========================================

    if result.get(
        "job_match_score"
    ) is not None:


        story.append(

            Paragraph(
                "Job Match Analysis",
                heading_style
            )
        )


        story.append(

            Paragraph(

                f"<b>Job Match Score:</b> "
                f"{result.get('job_match_score')}%",

                normal_style
            )
        )


        story.append(
            Spacer(1, 10)
        )


        # MATCHING SKILLS

        matching_skills = result.get(
            "matching_skills",
            []
        )


        if matching_skills:

            story.append(

                Paragraph(
                    "Matching Skills",
                    subheading_style
                )
            )


            for skill in matching_skills:

                story.append(

                    Paragraph(
                        f"• {skill}",
                        normal_style
                    )
                )


        # MISSING JOB SKILLS

        missing_job_skills = result.get(
            "missing_job_skills",
            []
        )


        if missing_job_skills:

            story.append(

                Paragraph(
                    "Missing Job Skills",
                    subheading_style
                )
            )


            for skill in missing_job_skills:

                story.append(

                    Paragraph(
                        f"• {skill}",
                        normal_style
                    )
                )


        # MISSING KEYWORDS

        missing_keywords = result.get(
            "missing_keywords",
            []
        )


        if missing_keywords:

            story.append(

                Paragraph(
                    "Missing Keywords",
                    subheading_style
                )
            )


            for keyword in missing_keywords:

                story.append(

                    Paragraph(
                        f"• {keyword}",
                        normal_style
                    )
                )


    # =========================================
    # PDF FOOTER
    # =========================================

    story.append(
        Spacer(1, 25)
    )


    story.append(

        Paragraph(
            "Generated by AI Career Assistant",
            subtitle_style
        )
    )


    # =========================================
    # BUILD PDF
    # =========================================

    pdf.build(
        story
    )


    # =========================================
    # DOWNLOAD PDF
    # =========================================

    return send_file(

        file_path,

        as_attachment=True,

        download_name=(
            "AI_Resume_Analysis_Report.pdf"
        ),

        mimetype="application/pdf"
    )


# =========================================
# LOGOUT
# =========================================

@app.route("/logout")
def logout():

    session.pop(
        "user",
        None
    )

    return redirect("/login")


# =========================================
# RUN APPLICATION
# =========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )

