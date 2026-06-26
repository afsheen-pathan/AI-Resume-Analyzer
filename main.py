import streamlit as st
import json

from utils import *


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# ---------- Custom CSS ----------

st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
    background-color:#0F172A;
}


[data-testid="stSidebar"]{
    background-color:#1E293B;
}


div[data-testid="metric-container"]{
    background:#1E293B;
    border:1px solid #334155;
    padding:15px;
    border-radius:12px;
}


.stButton>button{
    background:#6366F1;
    color:white;
    border-radius:10px;
    width:100%;
}


.stDownloadButton>button{
    background:#10B981;
    color:white;
    border-radius:10px;
    width:100%;
}


</style>

""", unsafe_allow_html=True)



# ---------- Sidebar ----------

with st.sidebar:

    st.title("⚙️ Settings")


    role = st.selectbox(

        "Target Role",

        [

            "Software Engineer",

            "AI Engineer",

            "Data Analyst",

            "Frontend Developer",

            "Backend Developer",

            "Full Stack Developer",

            "DevOps Engineer",

            "Cyber Security Analyst",

            "UI/UX Designer",

            "General",

            "✍️ Write Manually"

        ]

    )


    custom_role = ""

    if role == "✍️ Write Manually":

        custom_role = st.text_input(

            "Enter Job Role"

        )

        if custom_role.strip():

            role = custom_role



    exp = st.selectbox(

        "Experience Level",

        [

            "Fresher",

            "1-3 Years",

            "3+ Years"

        ]

    )


    st.markdown("---")


    st.info("""

Supported Formats

• PDF

• TXT


Powered by Gemini 2.5 Flash

""")


# ---------- Header ----------

st.title("📄 AI Resume Analyzer")

st.caption(

    "Analyze resumes with ATS insights, keyword gaps and AI-powered suggestions."

)



uploaded_file = st.file_uploader(

    "Upload Resume",

    type=[

        "pdf",

        "txt"

    ]

)



if uploaded_file:


    resume = extract_text_from_file(

        uploaded_file

    )


    stats = get_resume_stats(

        resume

    )



    c1, c2, c3 = st.columns(3)


    c1.metric(

        "Words",

        stats["words"]

    )


    c2.metric(

        "Pages",

        stats["pages"]

    )


    c3.metric(

        "Read Time",

        f"{stats['read_time']} min"

    )



    tab1, tab2 = st.tabs(

        [

            "📊 Analysis",

            "📄 Resume Preview"

        ]

    )



    with tab2:


        st.text_area(

            "Extracted Resume",

            resume,

            height=500

        )




    with tab1:


        analyze = st.button(

            "🚀 Analyze Resume"

        )



        if analyze:


            with st.spinner(

                    "Gemini is analyzing your resume..."):


                data = analyze_resume(

                    resume,

                    role,

                    exp

                )



            st.success(

                "Analysis Completed Successfully"

            )



            st.progress(

                100

            )



            s1, s2 = st.columns(2)



            s1.metric(

                "Resume Score",

                data["resume_score"]

            )



            s2.metric(

                "ATS Score",

                data["ats_score"]

            )



            st.divider()



            st.subheader(

                "💪 Strengths"

            )


            for i in data["strengths"]:


                st.success(

                    i

                )




            st.subheader(

                "⚠️ Weaknesses"

            )



            for i in data["weaknesses"]:


                st.error(

                    i

                )




            st.subheader(

                "🔍 Missing Keywords"

            )



            for i in data["missing_keywords"]:


                st.info(

                    i

                )




            st.subheader(

                "🛠 Suggested Skills"

            )



            for i in data["suggested_skills"]:


                st.write(

                    "✅",

                    i

                )




            st.subheader(

                "🎨 Formatting Suggestions"

            )



            for i in data["formatting_suggestions"]:


                st.warning(

                    i

                )




            st.subheader(

                "🏁 Final Verdict"

            )


            st.markdown(

                f"## {data['verdict']}"

            )




            pdf = generate_pdf(

                data

            )



            col1, col2 = st.columns(2)



            with col1:


                st.download_button(

                    "📥 Download PDF Report",

                    data=pdf,

                    file_name="report.pdf",

                    mime="application/pdf"

                )



            with col2:


                st.download_button(

                    "📥 Download JSON",

                    data=json.dumps(

                        data,

                        indent=4

                    ),

                    file_name="report.json",

                    mime="application/json"

                )