Text2SQL-Gemini-Agent: -
Bridges the gap between plain English and databases. An intelligent agent powered by Google Gemini that instantly translates natural language questions into accurate, production-ready SQL queries.

Description: -
Navigating complex database schemas and writing custom SQL queries shouldn't be a bottleneck for data insights. This project is an intelligent, conversational assistant built to make data exploration completely frictionless. 
By combining the reasoning power of LLMs with structured database systems, it allows developers, business analysts, or non-technical stakeholders to ask questions in everyday language and receive optimized, production-ready SQL queries instantly.

Tech Stack: -
* **Language:** Python
* **LLM Engine:** Google Gemini API
* **Agent Framework:** LangChain (for orchestration and memory management)
* **Database Toolkit:** SQLAlchemy (for secure database connections)
* **User Interface:** Streamlit (for a clean, responsive chat experience)

Usage Guide: -
### 1. Configure Environment Variables
Create a file named `.env` in the root directory of your project and add your specific API key and database path:
GEMINI_API_KEY=your_actual_gemini_api_key_here

### 2. Launch the Application
Run the Streamlit app
streamlit run app.py
Once open, type any question like "Show me top scores in the Data Science subject" or "Show me the average marks of all the students" and watch the  AI agent instantly generate your query!
