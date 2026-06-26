import os
import io
import json

import PyPDF2
import google.generativeai as genai

from dotenv import load_dotenv

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


#######################################
# Extract Text
#######################################

def extract_text_from_pdf(pdf_file):

    reader = PyPDF2.PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return text



def extract_text_from_file(uploaded_file):


    if uploaded_file.type == "application/pdf":

        return extract_text_from_pdf(

            io.BytesIO(

                uploaded_file.read()

            )

        )



    return uploaded_file.read().decode("utf-8")




#######################################
# Statistics
#######################################


def get_resume_stats(text):


    words = len(text.split())


    pages = max(

        1,

        round(words / 500)

    )


    read_time = max(

        1,

        round(words / 200)

    )



    return {

        "words": words,

        "pages": pages,

        "read_time": read_time

    }



#######################################
# Gemini Analysis
#######################################


def analyze_resume(

        resume_text,

        role,

        experience

):



    prompt = f"""

You are a Senior HR Manager and ATS Specialist.


Analyze the following resume.


Target Role :

{role}


Experience Level :

{experience}



Return ONLY JSON.



Required Structure


{{
"resume_score":85,
"ats_score":80,

"strengths":[
"..."
],


"weaknesses":[
"..."
],


"missing_keywords":[
"..."
],


"suggested_skills":[
"..."
],


"formatting_suggestions":[
"..."
],


"verdict":"Good"

}}



Resume


{resume_text}

"""



    model = genai.GenerativeModel(

        "gemini-2.5-flash"

    )



    response = model.generate_content(

        prompt

    )



    return parse_response(

        response.text

    )




#######################################
# Cleaner
#######################################


def clean_json(text):


    text = text.replace(

        "```json",

        ""

    )


    text = text.replace(

        "```",

        ""

    )


    start = text.find("{")

    end = text.rfind("}")


    if start != -1 and end != -1:

        text = text[start:end+1]



    return text.strip()




#######################################
# Parser
#######################################


def parse_response(text):


    try:


        text = clean_json(

            text

        )



        data = json.loads(

            text

        )



        return {

            "resume_score":

                data.get(

                    "resume_score",

                    0

                ),




            "ats_score":

                data.get(

                    "ats_score",

                    0

                ),




            "strengths":

                data.get(

                    "strengths",

                    []

                ),




            "weaknesses":

                data.get(

                    "weaknesses",

                    []

                ),




            "missing_keywords":

                data.get(

                    "missing_keywords",

                    []

                ),




            "suggested_skills":

                data.get(

                    "suggested_skills",

                    []

                ),




            "formatting_suggestions":

                data.get(

                    "formatting_suggestions",

                    []

                ),




            "verdict":

                data.get(

                    "verdict",

                    "Unknown"

                )

        }



    except:


        return {

            "resume_score":0,

            "ats_score":0,

            "strengths":[],

            "weaknesses":[],

            "missing_keywords":[],

            "suggested_skills":[],

            "formatting_suggestions":[],

            "verdict":"Unknown"

        }




#######################################
# PDF Export
#######################################


def generate_pdf(data):


    buffer = io.BytesIO()



    doc = SimpleDocTemplate(

        buffer

    )



    styles = getSampleStyleSheet()



    elements = []



    elements.append(

        Paragraph(

            "Resume Analysis Report",

            styles["Title"]

        )

    )



    elements.append(

        Spacer(

            1,

            20

        )

    )



    sections = [

        (

            "Resume Score",

            [

                str(

                    data["resume_score"]

                )

            ]

        ),


        (

            "ATS Score",

            [

                str(

                    data["ats_score"]

                )

            ]

        ),


        (

            "Strengths",

            data["strengths"]

        ),


        (

            "Weaknesses",

            data["weaknesses"]

        ),


        (

            "Missing Keywords",

            data["missing_keywords"]

        ),


        (

            "Suggested Skills",

            data["suggested_skills"]

        ),


        (

            "Formatting Suggestions",

            data["formatting_suggestions"]

        )

    ]



    for title, items in sections:



        elements.append(

            Paragraph(

                f"<b>{title}</b>",

                styles["Heading2"]

            )

        )



        for item in items:


            elements.append(

                Paragraph(

                    f"• {item}",

                    styles["BodyText"]

                )

            )



        elements.append(

            Spacer(

                1,

                10

            )

        )




    elements.append(

        Paragraph(

            f"<b>Verdict:</b> {data['verdict']}",

            styles["Heading2"]

        )

    )



    doc.build(

        elements

    )



    buffer.seek(0)



    return buffer