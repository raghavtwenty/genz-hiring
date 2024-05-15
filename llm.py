import openai
import serpapi
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")
client = serpapi.Client(api_key=SERP_API_KEY)
jobSeek = []


def evaluate_resume(prompt, conversation_history):
    conversation_history.append({"role": "user", "content": prompt})

    full_prompt = "\n".join([message["content"] for message in conversation_history])

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": full_prompt}],
        max_tokens=500,
    )

    result = response["choices"][0]["message"]["content"]

    conversation_history.append({"role": "system", "content": result})

    return conversation_history, result


def job_seek_fun(Job_Role):
    results_ = client.search(
        {
            "engine": "google_jobs",
            "q": Job_Role,
            "location": "New York, NY",
            "chips": "date_posted:month",
        }
    )

    for job_result in results_["jobs_results"]:
        # Extract details separately
        job_title = job_result.get("title", "N/A")
        company_name = job_result.get("company_name", "N/A")
        location = job_result.get("location", "N/A")
        extensions = job_result.get("extensions", "N/A")
        detected_extensions = job_result.get("detected_extensions", "N/A")

        temp = f"Job Title: {job_title}\nCompany Name: {company_name}\nLocation: {location}\nExtensions: {extensions}"
        jobSeek.append(temp)

    return jobSeek


def llm_prompt(job_role, job_description, resume_content):
    qualities = [
        "Resume Length",
        "Total Bulleted Points",
        "Bulleted Point Length",
        "Action Verbs",
        "Quantification",
        "Skills",
        "Consistency",
        "Dates Ordering",
        "Spell Check",
        "Readability",
    ]

    prompts1 = [
        f"Evaluate the following resume for job role: {job_role} with job description: {job_description}:\n\n{resume_content}"
    ]

    prompts2 = [
        f"Evaluate the following resume for job role: {job_role} with job description: {job_description}:\n\n{resume_content}"
    ]

    prompts3 = [
        f"Evaluate the following resume for job role: {job_role} with job description: {job_description}:\n\n{resume_content}"
    ]

    for i in range(len(qualities)):
        if i < 4:
            prompts1.append(
                f"Provide insights on the {qualities[i]} for the above resume (no points only in paragraphs)"
            )

            prompts1.append(
                f"Suggest some modification on {qualities[i]} to improve the above resume (no points only in paragraphs)"
            )

            prompts1.append(
                f"Give a score of 10 for the {qualities[i]} for the above resume (only integer no words) example output: 8"
            )

        elif i < 7:
            prompts2.append(
                f"Provide insights on the {qualities[i]} for the above resume (no points only in paragraphs)"
            )

            prompts2.append(
                f"Suggest some modification on {qualities[i]} to improve the above resume (no points only in paragraphs)"
            )

            prompts2.append(
                f"Give a score of 10 for the {qualities[i]} for the above resume (only integer no words)example output: 8"
            )

        else:
            prompts3.append(
                f"Provide insights on the {qualities[i]} for the above resume (no points only in paragraphs)"
            )

            prompts3.append(
                f"Suggest some modification on {qualities[i]} to improve the above resume (no points only in paragraphs)"
            )

            prompts3.append(
                f"Give a score of 10 for the {qualities[i]} for the above resume (only integer no words ) example output: 8"
            )

    # prompts.append("Suggest some overall modification to improve the resume")
    results1, conversation_history = [], []

    for prompt in prompts1:
        conversation_history, result = evaluate_resume(prompt, conversation_history)
        results1.append(result)

    results2, conversation_history = [], []
    for prompt in prompts2:
        conversation_history, result = evaluate_resume(prompt, conversation_history)
        results2.append(result)

    results3, conversation_history = [], []
    for prompt in prompts3:
        conversation_history, result = evaluate_resume(prompt, conversation_history)
        results3.append(result)

    results = results1 + results2[1:] + results3[1:]
    insights, modifications, scores = [], [], []
    for i in range(1, len(results), 3):
        insights.append(results[i])
        modifications.append(results[i + 1])
        scores.append(int(results[i + 2]))

    conversation_history = []
    prompt = f"Summarize this:\n\n{modifications}\n\n(no points only in paragraphs)"
    _, result = evaluate_resume(prompt, conversation_history)
    results.insert(1, result)
    results.insert(2, sum(scores))

    conversation_history = []
    prompt = f"For the job role: {job_role} with job description: {job_description} take the content from this resume:\n\n{resume_content}\n\nAnd now using this alterations:\n\n{modifications}\n\nI am beginner provide me a new resume."
    _, magic = evaluate_resume(prompt, conversation_history)

    conversation_history = []
    prompt = (
        f"For this resume:\n\n{resume_content}\n\nWhat is the best role (only one word)"
    )
    _, Job_Role = evaluate_resume(prompt, conversation_history)
    # print(Job_Role)

    recc_jobs = job_seek_fun(Job_Role)

    return results, magic, recc_jobs
