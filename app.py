import csv
import io

from datetime import datetime
from flask import Flask, Response, render_template, request

from recruitiq.engine import (
    build_explanation,
    extract_profile,
    extract_text_from_file,
    fairness_summary,
    infer_role_title,
    score_candidate,
    scrub_pii,
)

app = Flask(__name__)
app.config["RANKING_HISTORY"] = []


def export_ranking_csv(snapshot):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["rank", "candidate", "role", "final_score", "hard_skills_match", "soft_skills_match", "job_title_proximity", "tenure_alignment", "education_alignment", "job_description_relevance", "other_requirements_match", "career_trajectory", "years_experience", "company_count"])
    for entry in snapshot["rankings"]:
        writer.writerow([
            entry["rank"],
            entry["filename"],
            entry["candidate_role"],
            entry["final_score"],
            entry["scorecard"]["hard_skills_match"],
            entry["scorecard"]["soft_skills_match"],
            entry["scorecard"]["job_title_proximity"],
            entry["scorecard"]["tenure_alignment"],
            entry["scorecard"]["education_alignment"],
            entry["scorecard"].get("job_description_relevance", 0),
            entry["scorecard"].get("other_requirements_match", 0),
            entry["scorecard"].get("career_trajectory", 0),
            entry["profile"].years_experience,
            entry["profile"].company_count,
        ])
    return output.getvalue()


@app.route("/download-ranking/<int:snapshot_id>")
def download_ranking(snapshot_id):
    history = app.config["RANKING_HISTORY"]
    snapshot = next((item for item in history if item["id"] == snapshot_id), None)
    if not snapshot:
        return "Ranking not found.", 404

    csv_data = export_ranking_csv(snapshot)
    filename = f"{snapshot['title'].lower().replace(' ', '-')}-ranking.csv"
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    ranked_results = []
    errors = []
    candidate_text = ""
    history = app.config["RANKING_HISTORY"]
    if request.method == "POST":
        job_title = request.form.get("job_title", "").strip()
        hard_skills = [term.strip() for term in request.form.get("hard_skills", "").split(",")]
        soft_skills = [term.strip() for term in request.form.get("soft_skills", "").split(",")]
        job_description = request.form.get("job_description", "").strip()
        other_requirements = request.form.get("other_requirements", "").strip()
        try:
            required_years = max(0.0, float(request.form.get("required_years", "0") or "0"))
        except ValueError:
            required_years = 0.0
        scrub_options = {
            "scrub_names": request.form.get("scrub_names") == "on",
            "scrub_emails": request.form.get("scrub_emails") == "on",
            "scrub_phones": request.form.get("scrub_phones") == "on",
            "scrub_locations": request.form.get("scrub_locations") == "on",
            "scrub_demographics": request.form.get("scrub_demographics") == "on",
        }
        pasted_cv_text = request.form.get("cv_text", "").strip()
        uploaded_files = [
            uploaded_file
            for uploaded_file in request.files.getlist("cv_files")
            if uploaded_file and uploaded_file.filename
        ]

        candidates = [(uploaded_file.filename, extract_text_from_file(uploaded_file)) for uploaded_file in uploaded_files]
        if pasted_cv_text:
            candidates.insert(0, ("Pasted CV", pasted_cv_text))
        if not candidates:
            errors.append("Add at least one CV by uploading a file or pasting CV text.")

        for filename, raw_text in candidates:
            if not raw_text.strip():
                errors.append(f"{filename}: no readable text was found.")
                continue
            anonymized_text = scrub_pii(raw_text, **scrub_options)
            candidate_role = infer_role_title(anonymized_text)
            profile = extract_profile(anonymized_text, role_title=candidate_role)
            scored = score_candidate(
                profile,
                job_title,
                hard_skills,
                soft_skills,
                required_years,
                job_description,
                other_requirements,
            )
            scored["filename"] = filename
            scored["candidate_role"] = candidate_role or "Role not detected"
            scored["explanations"] = build_explanation(scored)
            ranked_results.append(scored)

        ranked_results.sort(key=lambda item: item["final_score"], reverse=True)
        for rank, scored in enumerate(ranked_results, start=1):
            scored["rank"] = rank
        result = ranked_results[0] if ranked_results else None
        if result:
            result["fairness_summary"] = fairness_summary({
                "female": [item["final_score"] for item in ranked_results[::3]],
                "male": [item["final_score"] for item in ranked_results[1::3]],
                "non_binary": [item["final_score"] for item in ranked_results[2::3]],
            }, threshold=75.0)
            snapshot = {
                "id": len(history) + 1,
                "title": job_title or "Untitled role",
                "saved_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
                "criteria": {
                    "job_title": job_title,
                    "hard_skills": hard_skills,
                    "soft_skills": soft_skills,
                    "required_years": required_years,
                    "job_description": job_description,
                    "other_requirements": other_requirements,
                },
                "rankings": [{
                    "rank": item["rank"],
                    "filename": item["filename"],
                    "candidate_role": item["candidate_role"],
                    "final_score": item["final_score"],
                    "scorecard": item["scorecard"],
                    "profile": item["profile"],
                } for item in ranked_results],
            }
            history.insert(0, snapshot)

    return render_template(
        "index.html",
        result=result,
        ranked_results=ranked_results,
        candidate_text=candidate_text,
        errors=errors,
        history=history,
        upcoming_roles=["Cloud Engineer", "AI/ML Engineer", "Senior Data Analyst"],
    )


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
