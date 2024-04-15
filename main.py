from dotenv import load_dotenv

load_dotenv()
import streamlit as st
import google.generativeai as genai
import PyPDF2
import pickle
from pathlib import Path
import streamlit_authenticator as stauth

genai.configure(api_key=st.secrets["GOOGLE_API"])


def get_gemini_response(input,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([input,prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    text = ""
    for resume in uploaded_file:
        if resume!=None:
            print(resume.read())
            with resume:
                # Create a PDF file reader object
                pdf_reader = PyPDF2.PdfReader(resume)
                
                # Loop through each page of the PDF
                for page_num in range(len(pdf_reader.pages)):
                    # Extract text from the current page
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
        else:
            return "No response Recorded"
    print(text)
    return text

## Streamlit App

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resumes against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role('There are multiple resumes plz filter accordingly'). 
 Highlight the strengths and weaknesses of the applicant ('with the name of applicant  mentioned at the top') in relation to the specified job requirements job Description is:-:.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, ('There are multiple resumes plz filter accordingly')
your task is to evaluate the resumes against the provided job description. give me the percentage of match if the resumes matches
the job description. First the name of applicants then output should come as percentages and then keywords missing and last final thoughts job Description is:-:.
"""

input_prompt2 = """
You are a highly experienced career consultant with expertise in resume evaluation and job matching. Your task is to provide feedback and improvement tips based on the weaknesses identified in the resume,
('note:- There are multiple resumes plz filter accordingly and  all were in  tabular format in which mention rank of resumes and the names of the candidates also percentage matches with the job profiles strength and weakneses')
 aligning it with the job description. 
 Please share your professional evaluation and suggestions for improvement. 
 Job improvements is:-:.
"""

input_prompt7 = """
You are a highly experienced career consultant and also you have knowledge about all the domain and I am giving you the resume information which is as followed 
"""

input_prompt8 = """
and using job description generate the road map to get achieve this goal in tabular format with expected complition time line and skill sets which you have to acquire.
"""

st.set_page_config(page_title="Xcellence Board : AI TPO",page_icon="favicon.jpg")
# USER AUTHENTICATION
names = ["Urvashi","Kalki","Prateek"]
usernames = ["urvashi","kalki","prateek"]
passwords=['$2b$12$g2gA6hHELmc8eKgQBBBqROytK6otPqPRDLD56j2CADur2zUIHrxTe', '$2b$12$fuHdgIIdRyFmFFK0fX7jn.U8KiAGwIy4nT/3.LT47bpoR4p/A/xpG', '$2b$12$qwrzvcXcJdarwJImjrConOnv3/cV5KTpkqghSapVVa4Q91YAY1TyS']

credentials = {
        "usernames":{
            usernames[0]:{
                "name":names[0],
                "password":passwords[0]
                },
            usernames[1]:{
                "name":names[1],
                "password":passwords[1]
                },
            usernames[2]:{
                "name":names[2],
                "password":passwords[2]
                }        
            }
        }



#load hashed passwords

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)


authenticator = stauth.Authenticate(credentials, "garudaats_system", "garuda", cookie_expiry_days=30.0)

name, authentication_status, username = authenticator.login("main")

if authentication_status == False:
    st.error("Username/Password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status :

    current_page = 1

    # Sidebar navigation
    st.sidebar.image("xcellenceboard.png",use_column_width=True)
    st.sidebar.title("XCELLENCE BOARD")
    st.sidebar.subheader(f"Welcome {name}")
    page_selection = st.sidebar.radio("Go to", ("SIN ATS Tracking System","Generate Questions(Garud GenZ)"))
    uploaded_file = st.sidebar.file_uploader("Upload your resume(PDF)...",type=["pdf"], accept_multiple_files=True)
    # Page 1: Garuda ATS Tracking System
    if page_selection == "SIN ATS Tracking System":
        st.image("sinindia.jpg", use_column_width=True)
        st.title("SIN ATS Tracking System")
        input_text=st.text_area("Job Description: ",key="input")
        
        col2, col3, col4, col5 = st.columns(4)

        with col2:
            submit1 = st.button("Resume Summary")

        with col3:
            submit2 = st.button("Improvements Suggestions")

        with col4:
            submit3 = st.button("Percentage match")
        
        with col5:
            submit7 = st.button("Roadmap Suggestions")
        
        if submit1:
            if uploaded_file is not None:
                pdf_content=input_pdf_setup(uploaded_file)
                response=get_gemini_response(input_prompt1+input_text,pdf_content)
                st.subheader("The Repsonse is")
                st.write(response)
                with open("response.txt", "w") as file:
                    file.write(response)
                    a = response
                    download_button = st.download_button("Download Response",a,file_name="HRResponse.txt")
            else:
                st.write("Please upload the resume")

        elif submit2:
            if uploaded_file is not None:
                pdf_content=input_pdf_setup(uploaded_file)
                response=get_gemini_response(input_prompt2+input_text,pdf_content)
                st.subheader("The Repsonse is")
                st.write(response)
                with open("response.txt", "w") as file:
                    file.write(response)
                    a = response
                    download_button = st.download_button("Download Response",a,file_name="HRResponse.txt")
            else:
                st.write("Please upload the resume")


        elif submit3:
            if uploaded_file is not None:
                pdf_content=input_pdf_setup(uploaded_file)
                response=get_gemini_response(input_prompt3+input_text,pdf_content)
                st.subheader("The Repsonse is")
                st.write(response)
                with open("response.txt", "w") as file:
                    file.write(response)
                    a = response
                    download_button = st.download_button("Download Response",a,file_name="HRResponse.txt")
            else:
                st.write("Please upload the resume")

        elif submit7:
            if uploaded_file is not None:
                pdf_content=input_pdf_setup(uploaded_file)
                response=get_gemini_response(input_prompt7+input_text+input_prompt8,pdf_content)
                st.subheader("The Repsonse is")
                st.write(response)
                with open("response.txt", "w") as file:
                    file.write(response)
                    a = response
                    download_button = st.download_button("Download Response",a,file_name="HRResponse.txt")
            else:
                st.write("Please upload the resume")


    elif page_selection=="Generate Questions(Garud GenZ)":

        st.image("sinindia.jpg", use_column_width=True)
        st.title("SIN GenZ Interview")
        input_job=st.text_area("Job profile:" ,key="input")
        hardness=st.radio("Difficulty Level",("Low","Medium","Hard"))
        gen_bt=st.button("Generate")
        if gen_bt==True:
            if hardness=="Low":
                prompts=f"""According to the job role:-{input_job} Generate interview question which we can ask to the applicant with answers
                """
                res_gemini=get_gemini_response(input=prompts,prompt=f"Hardness of the questions will be:-:{hardness}")
                st.write(res_gemini)
                a = res_gemini
                download_button = st.download_button("Download Response",a,file_name="HRResponse.txt")
            if hardness=="Medium":
                prompts=f"""According to the job role:-{input_job} Generate interview question which we can ask to the applicant with an overview and in a broad way plz check how the applicant
                would perform in real world 
                """
                res_gemini=get_gemini_response(input=prompts,prompt=f"Hardness of the questions will be:-:{hardness}")
                st.write(res_gemini)
                a = res_gemini
                download_button = st.download_button("Download Response",a,file_name="HRResponse.txt")
            if hardness=="Hard":
                prompts=f"""According to the job role:-{input_job} Generate interview question which we can ask to the applicant make sure to 
                check the analytical knowledge and deep dive into the domain also included some cutting edge techniques of the interviewer also mention answers for that questions
                """
                res_gemini=get_gemini_response(input=prompts,prompt=f"Hardness of the questions will be:-:{hardness}")
                st.write(res_gemini)
                a = res_gemini
                download_button = st.download_button("Download Response",a,file_name="HRResponse.txt")


    if uploaded_file is not None:
        st.sidebar.write("PDF Uploaded Successfully")

    authenticator.logout("Logout","sidebar")



