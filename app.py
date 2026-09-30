import os
import sqlite3
from dotenv import load_dotenv
import streamlit as st

# 1. Load environment variables first
load_dotenv()

# 2. Set environment variables to force REST transport over gRPC
os.environ["GOOGLE_API_USE_CLIENT_CERTIFICATE"] = "false"
os.environ["GOOGLE_PYTHON_GAPI_TRANSPORT"] = "rest"

from google import genai

# Set page config
st.set_page_config(page_title="Gemini Text-to-SQL Studio", page_icon="🪐", layout="wide")

# --- GEMINI CYBER-DARK CSS STYLING ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Inter:wght@300;400;600;700;800&display=swap');

/* Main App Background */
.stApp {
    background-color: #eaf6ff;
    background-image:
        radial-gradient(at 15% 10%, rgba(124, 77, 255, 0.08) 0px, transparent 50%),
        radial-gradient(at 90% 85%, rgba(68, 138, 255, 0.12) 0px, transparent 50%);
    font-family: 'Inter', sans-serif;
    color: #172554;
}

/* Main Content */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Gradient Header Title */
.gemini-title {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #7c4dff 0%, #448aff 50%, #00bcd4 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 4s linear infinite;
    margin-bottom: 0.2rem;
}

@keyframes shine {
    to { background-position: 200% center; }
}

/* Subtitle - Bold and Italic */
.gemini-subtitle {
    color: #475569 !important;
    font-size: 1.15rem;
    font-weight: 700 !important;
    font-style: italic !important;
    margin-bottom: 1.5rem;
}

/* Glassmorphic Cards - Light Theme */
.css-card {
    background: rgba(255, 255, 255, 0.75);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(148, 163, 184, 0.25);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 20px rgba(30, 64, 175, 0.06);
    margin-bottom: 25px;
}

/* Input Labels - Increased Size & Italic */
.stTextInput label {
    color: #172554 !important;
    font-weight: 700 !important;
    font-style: italic !important;
    font-size: 1.25rem !important;
}

/* Input Fields */
.stTextInput input {
    background-color: #ffffff !important;
    color: #172554 !important;
    border: 1px solid #bfdbfe !important;
    border-radius: 10px !important;
    padding: 12px 16px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1.05rem !important;
    font-style: italic !important;
}

/* Placeholder Text */
.stTextInput input::placeholder {
    color: #94a3b8 !important;
    opacity: 1 !important;
    font-style: italic !important;
}

/* Input Focus */
.stTextInput input:focus {
    border-color: #448aff !important;
    box-shadow: 0 0 0 2px rgba(68, 138, 255, 0.15) !important;
}

/* Gradient Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c4dff, #448aff) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    box-shadow: 0 4px 12px rgba(124, 77, 255, 0.18) !important;
    transition: all 0.3s ease !important;
}

/* Button Hover */
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(68, 138, 255, 0.25) !important;
}

/* Output Data Rows */
.result-card {
    background: #ffffff;
    border-left: 4px solid #448aff;
    border-radius: 8px;
    padding: 12px 16px;
    margin-top: 8px;
    font-family: 'Fira Code', monospace;
    color: #1e40af;
    box-shadow: 0 2px 8px rgba(30, 64, 175, 0.05);
}

/* SQL Code Blocks */
.stCode,
pre {
    border-radius: 10px !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Configure API Key with explicit REST transport
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except Exception:
        pass

if api_key:
    client = genai.Client(api_key=api_key)
else:
    st.error("Google API Key not found. Please set GOOGLE_API_KEY in your .env or secrets.")
    st.stop()


# Load Gemini model and get the SQL query response
def get_gemini_response(question, prompt):
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=f"""
        {prompt}

        User Question:
        {question}
        """
    )
    return response.text


# Run the SQL query on the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows


# System Prompt
prompt = """
You are an expert in converting English questions to SQL queries!
The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION and MARKS

For example,
Example 1 - How many entries of records are present?, the SQL command will be something like this: SELECT COUNT(*) FROM STUDENT;

Example 2 - Tell me all the students studying in Data Science class?, the SQL command will be something like this: SELECT * FROM STUDENT WHERE CLASS="Data Science";

Example 3 - What is the average marks of students in section A?, the SQL command will be something like this: SELECT AVG(MARKS) FROM STUDENT WHERE SECTION="A";

Example 4 - What is the total number of students in any class?, the SQL command will be something like this: SELECT COUNT* FROM STUDENT;

Example 5 - Show the details of Aarav, the SQL command will be something like this: SELECT * FROM STUDENT WHERE NAME = 'Aarav';

Example 6 - Show names and marks of all students, the SQL command will be something like this: SELECT NAME, MARKS FROM STUDENT;

Example 7 - Show all students from DEVOPS, the SQL command will be something like this: SELECT * FROM STUDENT WHERE CLASS = 'DEVOPS';

Example 8 - Show students from section A, the SQL command will be something like this: SELECT * FROM STUDENT WHERE SECTION = 'A';

Example 8 - Show students from section B, the SQL command will be something like this: SELECT * FROM STUDENT WHERE SECTION = 'B';

Example 9 - Show students who scored marks more than 80, the SQL command will be something like this: SELECT * FROM STUDENT WHERE MARKS > 80;

Example 10 - Show students who scored less than 50, the SQL command will be something like this: SELECT * FROM STUDENT WHERE MARKS < 50;

Example 11 - Show students who scored between 50 and 90, the SQL command will be something like this: SELECT * FROM STUDENT WHERE MARKS BETWEEN 50 AND 90;

Example 12 - Show students who scored exactly 100, the SQL command will be something like this: SELECT * FROM STUDENT WHERE MARKS = 100;

Example 13 - Show students who failed, the SQL command will be something like this: SELECT * FROM STUDENT WHERE MARKS < 33;

Example 14 - Show the student name who scored the highest marks?, the SQL command will be something like this: SELECT * FROM STUDENT WHERE MARKS = (SELECT MAX(MARKS) FROM STUDENT);

Example 15 - Who scored the lowest marks?, the SQL command will be something like this: SELECT * FROM STUDENT WHERE MARKS=(SELECT MIN (MARKS)FROM STUDENT);

Example 16 - What is the average mark of all the students?, the SQL command will be something like this: SELECT AVG(MARKS) FROM STUDENT;

Example 17 - What is the total of all students' marks?, the SQL command will be something like this: SELECT SUM(MARKS) FROM STUDENT;

Example 18 - What is the average mark of each class?, the SQL command will be something like this: SELECT CLASS, AVG(MARKS) FROM STUDENT GROUP BY CLASS;

Example 19 - Show Data Science students in section A who scored above 85, the SQL command will be something like this: SELECT * FROM STUDENT WHERE CLASS = "DATA SCIENCE" AND SECTION = "A" AND MARKS > 85;

Example 20 - Who scored higher than Aarav? the SQL command will be something like this: SELECT * FROM STUDENT WHERE MARKS > (SELECT MARKS FROM STUDENT WHERE NAME = 'AARAV');

Also, the SQL code should not have ``` at the beginning or end, and the word "sql" should not appear in the output.
Return only the SQL query with no explanation or extra text. If the question cannot be answered using the STUDENT table, reply with: Invalid question.
"""

# --- UI Header (Only One Title & Formatted Subtitle) ---
st.markdown('<div class="gemini-title">✦ TEXT TO SQL STUDIO</div>', unsafe_allow_html=True)
st.markdown('<p class="gemini-subtitle">Ask questions in plain English to query your SQLite database</p>', unsafe_allow_html=True)

# --- User Input Section ---
question = st.text_input("Input: ", key="input", placeholder="e.g. Show all students in section A with marks > 80")
submit = st.button("Ask the question")

# --- Results Processing ---
if submit and question:
    response = get_gemini_response(question, prompt)

    # Clean any stray markdown fences
    sql_query = response.replace("```sql", "").replace("```", "").strip()

    if sql_query.lower().startswith("invalid question"):
        st.warning("Invalid question. Please ask something about the STUDENT table.")
    else:
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        st.subheader("⚡ Generated SQL Query")
        st.code(sql_query, language="sql")

        try:
            data = read_sql_query(sql_query, "student.db")
            st.subheader("📊 The response is")

            if data:
                for row in data:
                    st.markdown(f'<div class="result-card">{row}</div>', unsafe_allow_html=True)
            else:
                st.info("Query executed successfully, but returned no matching records.")

        except sqlite3.Error as e:
            st.error(f"SQL error: {e}")

        st.markdown('</div>', unsafe_allow_html=True)
        