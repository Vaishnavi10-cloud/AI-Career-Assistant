from openai import OpenAI
import json

client = OpenAI()


def analyze_resume(resume_text, user_goal, job_description=""):

    prompt = f"""
You are a senior software engineer and hiring manager.

Evaluate the resume based on the user's career goal.

User goal:
"{user_goal}"

Resume:
{resume_text}

Job Description:
{job_description}

STRICT RULES:

- Extract skills that are actually present in the resume.
- Prioritize and evaluate those skills based on their relevance to the target career.
- Identify genuine missing skills for this career goal.
- Generate a roadmap only for the missing skills.
- Make the analysis different depending on the user's career goal.
- Generate interview questions relevant to the target role.
- Do not list a skill under "skills" unless it is actually present in the resume.

- Give the resume an overall strength score from 0 to 100.
- Consider skills, projects, education, experience, certifications,
  achievements, and relevance to the target career role.
- Do not give a high score just because many skills are listed.
- Identify 3 to 5 specific improvements that would make the resume stronger.

- Generate a recruiter action plan containing 3 to 5 practical actions the candidate should take to improve their chances of getting shortlisted.
- Prioritize the actions based on the resume, target role, and job description if provided.
- Actions should be specific and actionable, such as improving a project, adding a missing skill, quantifying achievements, improving resume keywords, or gaining relevant experience.

If a Job Description is provided and is not empty:

- Calculate a job match score from 0 to 100.
- Matching skills must ONLY contain skills that are present in BOTH
  the resume and the job description.
- Do not consider a resume skill a matching skill just because it is
  relevant to the career role.
- Missing job skills must contain requirements from the job description
  that are not present in the resume.
- Missing keywords must contain important technical terms from the job
  description that are missing from the resume.
- Treat equivalent terms as matches when appropriate.
  For example, "OOP" and "Object-Oriented Programming" can be considered
  the same skill.
 
If the Job Description is empty:

- Set "job_match_score" to null.
- Set "matching_skills" to [].
- Set "missing_job_skills" to [].
- Set "missing_keywords" to [].

Return ONLY valid JSON in exactly this format:

{{
    "skills": [],
    "missing_skills": [],
    "roadmap": [],
    "interview_questions": [],
    "job_match_score": null,
    "matching_skills": [],
    "missing_job_skills": [],
    "missing_keywords": [],
    "resume_score": 0,
    "resume_improvements": [],
    "recruiter_action_plan": []
}}
"""

    try:

        response = client.chat.completions.create(
            model="gpt-5.4-mini",
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict hiring manager."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response.choices[0].message.content.strip()

        start = content.find("{")
        end = content.rfind("}") + 1

        if start == -1 or end == 0:
            raise ValueError("AI did not return valid JSON")

        return json.loads(content[start:end])

    except Exception as e:

        return {
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_questions": [],
            "error": str(e)
        }