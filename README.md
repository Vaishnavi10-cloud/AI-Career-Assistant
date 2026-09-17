# AI Career Assistant

**Turn your resume into a personalized career roadmap.**

AI Career Assistant is an AI-powered resume analysis web application that helps students and job seekers understand how well their resume matches their target career role.

Users can upload or paste their resume, provide a target job description or role, and receive an AI-powered analysis of their skills, missing skills, job-description match, learning roadmap, and interview preparation.

---

## The problem

A resume may contain good skills and experience, but it can be difficult to determine:

- Whether the resume matches a particular job description
- Which required skills are missing
- Which areas of the resume need improvement
- What skills should be learned next
- How to prepare for interviews for the target role

Traditional resume checking tools often focus on basic formatting or keyword matching.

AI Career Assistant focuses on turning resume analysis into **actionable career guidance**.

---

## The idea

The application takes the user's resume together with their target role or job description and uses AI to generate a structured career analysis.

```text
Resume
   +
Job Description / Target Role
        ↓
   AI Analysis
        ↓
 ┌──────────────────────┐
 │ Current Skills       │
 │ Missing Skills       │
 │ Job Match            │
 │ Learning Roadmap     │
 │ Interview Questions  │
 └──────────────────────┘

```

The goal is to help users understand not only **where they currently stand**, but also **what they can do next**.

---

## Core features

### Resume Analysis

Users can provide their resume by uploading a resume file or entering their resume text.

The application extracts and processes the resume information before sending it for AI analysis.

### Job Description Matching

Users can provide a target job description and compare it with their resume.

The AI analyzes the relationship between the candidate's existing profile and the requirements mentioned in the job description.

This helps identify:

- Matching skills
- Missing skills
- Relevant qualifications
- Areas that may need improvement

### Target Role Analysis

Users can specify the role they are targeting, allowing the generated analysis to be focused on a particular career path.

Examples:

```text
Python Developer
Frontend Developer
Data Analyst
Machine Learning Engineer
Software Developer

```

### Skill Identification

The system identifies the technical and relevant skills present in the resume.

### Missing Skills

The application identifies skills that are required or useful for the selected role or job description but are not sufficiently represented in the resume.

### Learning Roadmap

Based on the identified skill gaps, the AI generates a personalized roadmap that helps the user understand what they can learn next.

### Interview Questions

The system generates interview questions related to the user's target role and profile.

This connects resume analysis with interview preparation.

### User Authentication

The application includes:

- Sign up
- Login
- Logout

### Analysis History

Previous analyses can be stored and accessed through the user's history, allowing users to review their previous resume evaluations.

---

## How it works

```text
                    ┌──────────────────┐
                    │      User        │
                    └────────┬─────────┘
                             │
                             ▼
              ┌────────────────────────────┐
              │ Resume + Job Description   │
              │       / Target Role        │
              └─────────────┬──────────────┘
                            │
                            ▼
              ┌────────────────────────────┐
              │      Flask Backend         │
              └─────────────┬──────────────┘
                            │
                            ▼
              ┌────────────────────────────┐
              │   Resume Text Processing   │
              └─────────────┬──────────────┘
                            │
                            ▼
              ┌────────────────────────────┐
              │        OpenAI API          │
              │      AI Analysis           │
              └─────────────┬──────────────┘
                            │
                            ▼
           ┌──────────────────────────────────┐
           │       Career Analysis             │
           ├──────────────────────────────────┤
           │ • Skills                         │
           │ • Missing Skills                 │
           │ • Job Description Match          │
           │ • Learning Roadmap               │
           │ • Interview Questions            │
           └────────────────┬─────────────────┘
                            │
                            ▼
              ┌────────────────────────────┐
              │ Dashboard + Analysis      │
              │ History                   │
              └────────────────────────────┘

```

---

## Architecture

```text
┌──────────────────────────────────────────────┐
│                Web Interface                 │
│                                              │
│              HTML + CSS                     │
│                                              │
│   Login │ Signup │ Dashboard │ History      │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│              Flask Backend                  │
│                                              │
│ Authentication                               │
│ Resume Processing                            │
│ Job Description Matching                     │
│ AI Analysis                                  │
│ Database Operations                          │
│ Analysis History                             │
└───────────────┬────────────────┬─────────────┘
                │                │
                ▼                ▼
       ┌────────────────┐   ┌─────────────────┐
       │    Database    │   │   OpenAI API    │
       │                │   │                 │
       │ Users          │   │ Resume Analysis │
       │ Analyses       │   │ Skill Analysis  │
       │ History        │   │ Job Matching    │
       └────────────────┘   │ Roadmap         │
                            │ Interview Prep  │
                            └─────────────────┘

```

---

## AI analysis flow

The application combines the resume with the user's target role or job description and sends the relevant information to the AI model.

The AI response is structured into useful categories such as:

```text
Skills
Missing Skills
Job Description Match
Learning Roadmap
Interview Questions

```

The structured response allows the application to display each part of the analysis separately in the user interface.

---

## Project structure

```text
AI-Career-Assistant/
│
├── static/
│   └── style.css
│
├── templates/
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── history.html
│   └── ...
│
├── app.py
├── ai.py
├── db.py
├── models.py
│
├── about.txt
├── learn.txt
├── resume_analysis.pdf
│
├── requirements.txt
├── .gitignore
└── README.md

```

---

## Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/Vaishnavi10-cloud/AI-Career-Assistant.git
cd AI-Career-Assistant

```

### 2. Create a virtual environment

On Windows:

```powershell
python -m venv venv

```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1

```

### 3. Install dependencies

```bash
pip install -r requirements.txt

```

### 4. Configure the OpenAI API key

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here

```

**Never upload your API key or** **`.env`** **file to GitHub.**

### 5. Run the application

```bash
python app.py

```

The application will be available at:

```text
http://127.0.0.1:5000

```

---

## Example workflow

### Step 1 — Create an account

Create an account and log into AI Career Assistant.

### Step 2 — Add your resume

Upload your resume or provide the resume text.

### Step 3 — Add your target

Provide either:

- A target job role, or
- A job description

### Step 4 — Analyze

The application processes the resume and target information and sends it for AI analysis.

### Step 5 — Review the results

The application provides insights including:

```text
Current Skills
       ↓
Job Description Match
       ↓
Missing Skills
       ↓
Learning Roadmap
       ↓
Interview Questions

```

### Step 6 — Review history

Previous analyses can be accessed from the history section.

---

## What makes it useful

AI Career Assistant connects multiple stages of career preparation in one workflow:

```text
Resume Analysis
       ↓
Job Description Matching
       ↓
Skill Gap Identification
       ↓
Learning Roadmap
       ↓
Interview Preparation

```

Instead of simply telling the user whether their resume looks good, the application provides information that can help them understand their current profile and plan their next steps.

---

## Scope and limitations

### Current scope

- Resume analysis
- Resume upload / text input
- Target role analysis
- Job description matching
- Skill identification
- Missing-skill identification
- Learning roadmap generation
- Interview-question generation
- User authentication
- Analysis history

### Limitations

- AI-generated recommendations may contain inaccuracies and should be reviewed by the user.
- Analysis quality depends on the information provided in the resume and job description.
- AI analysis requires access to the configured OpenAI API.
- API usage may incur costs depending on the OpenAI account and model being used.
- The application is intended as a career-support tool and does not replace professional recruitment or career counselling.

---

## Future improvements

- ATS compatibility analysis
- Resume improvement suggestions
- Resume scoring against job descriptions
- Resume version comparison
- Skill-progress tracking
- Job recommendation based on skills
- More advanced interview preparation
- Exportable career reports
- Production deployment
- Support for additional resume formats

---

## Built with

| TechnologyPurpose         |                                       |
| ------------------------- | ------------------------------------- |
| **Python**                | Core programming language             |
| **Flask**                 | Web application backend               |
| **HTML**                  | Web interface                         |
| **CSS**                   | User interface styling                |
| **OpenAI API**            | AI-powered resume and career analysis |
| **SQLAlchemy / Database** | User and analysis data management     |
| **PDF/DOCX processing**   | Resume text extraction                |

---

## Project workflow

```text
                 AI CAREER ASSISTANT

                       USER
                        │
                        ▼
                Upload / Paste Resume
                        │
                        ▼
               Enter Target Role /
                Job Description
                        │
                        ▼
                 AI PROCESSING
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
       Skills      Missing Skills   Job Match
          │             │             │
          └─────────────┼─────────────┘
                        ▼
                Learning Roadmap
                        │
                        ▼
               Interview Questions
                        │
                        ▼
                Save Analysis
                        │
                        ▼
                     History


