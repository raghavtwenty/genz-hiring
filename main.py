"""
Project Name: Genz Hiring
Developers:
    Farhaan
    Muhilan
    Naveen
    Raghava
Filename: main.py
Title: Flask route and logics
Author: Raghava | GitHub: @raghavtwenty
Date Created: November 20, 2023 | Last Updated: May 15, 2024
Language: Python | Version: 3.10.14, 64-bit
"""

# Importing required libraries
from flask import Flask, render_template, request, send_file
from langchain_community.document_loaders import DirectoryLoader
from llm import llm_prompt

# Flask App
app = Flask(__name__)


def get_appreciation(score):
    if score < 50:
        return "Attention required"
    elif score < 70:
        return "Getting closer..."
    elif score < 85:
        return "Good to go!"
    else:
        return "Perfect!!!"


def extract_text_from_pdf(pdf_file):
    if request.method == "POST":
        # Get the PDF file from the user
        pdf_file = request.files["pdf_file"]

        # Save the PDF file to a temporary location
        pdf_file.save("./data/temp.pdf")

        loc = "./data"

        # Extract text from pdf using langchain
        loader = DirectoryLoader(loc)
        documents = loader.load()

        for document in documents:
            if hasattr(document, "page_content"):
                page_content = document.page_content
            else:
                page_content = "No 'page_content' found in the document."

        # print(page_content)
        return page_content


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/result", methods=["GET", "POST"])
def result():
    global results
    global magic
    global jobSeek

    # Get the uploaded PDF file
    uploaded_file = request.files["pdf_file"]

    # user data
    jobrole = request.form.get("role")
    jobdesc = request.form.get("jobdesc")

    # Extract text from the PDF file
    text = extract_text_from_pdf(uploaded_file)

    # pass to llm
    results, Magic, JobSeek = llm_prompt(jobrole, jobdesc, text)

    left = results[0].split("\n")
    right = results[1].split("\n")
    score = int(results[2])
    magic = Magic.split("\n")
    jobSeek = JobSeek
    appreciation = get_appreciation(score)
    return render_template(
        "home.html",
        appreciation=appreciation,
        left=left,
        right=right,
        score=score,
        magic=magic,
        jobSeek=jobSeek,
    )


@app.route("/overview")
def overview():
    left = results[0].split("\n")
    right = results[1].split("\n")
    score = int(results[2])
    appreciation = get_appreciation(score)
    return render_template(
        "overview.html",
        appreciation=appreciation,
        left=left,
        right=right,
        score=score,
        magic=magic,
        jobSeek=jobSeek,
    )


@app.route("/length")
def length():
    left = results[3].split("\n")
    right = results[4].split("\n")
    score = int(results[5])

    return render_template("length.html", left=left, right=right, score=score)


@app.route("/total")
def total():
    left = results[6].split("\n")
    right = results[7].split("\n")
    score = int(results[8])

    return render_template("total.html", left=left, right=right, score=score)


@app.route("/bullet")
def bullet():
    left = results[9].split("\n")
    right = results[10].split("\n")
    score = int(results[11])

    return render_template("bullet.html", left=left, right=right, score=score)


@app.route("/action")
def action():
    left = results[12].split("\n")
    right = results[13].split("\n")
    score = int(results[14])

    return render_template("action.html", left=left, right=right, score=score)


@app.route("/quanti")
def quanti():
    left = results[15].split("\n")
    right = results[16].split("\n")
    score = int(results[17])

    return render_template("quanti.html", left=left, right=right, score=score)


@app.route("/skills")
def skills():
    left = results[18].split("\n")
    right = results[19].split("\n")
    score = int(results[20])

    return render_template("skills.html", left=left, right=right, score=score)


@app.route("/consis")
def consis():
    left = results[21].split("\n")
    right = results[22].split("\n")
    score = int(results[23])

    return render_template("consis.html", left=left, right=right, score=score)


@app.route("/dates")
def dates():
    left = results[24].split("\n")
    right = results[25].split("\n")
    score = int(results[26])

    return render_template("dates.html", left=left, right=right, score=score)


@app.route("/spell")
def spell():
    left = results[27].split("\n")
    right = results[28].split("\n")
    score = int(results[29])

    return render_template("spell.html", left=left, right=right, score=score)


@app.route("/read")
def read():
    left = results[30].split("\n")
    right = results[31].split("\n")
    score = int(results[32])
    return render_template("read.html", left=left, right=right, score=score)


# Main
if __name__ == "__main__":
    app.run()
