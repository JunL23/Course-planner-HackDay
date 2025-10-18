# Course-planner-Hack-Day-
---
# 🎓 AI Course Planner

An intelligent 4-year course planning assistant that uses **Generative AI** and **web automation** to design, refine, and personalize your entire academic path — automatically.

This project parses degree requirements, scrapes course descriptions and general education information, and utilizes the **Google Gemini API** to generate and iteratively refine a customized academic plan that aligns with your goals, interests, and timeline.

---

## 🚀 Features

### 🧠 AI-Driven Planning

* Automatically generates a **4-year academic plan** from your degree PDF and web data.
* Evaluates **course difficulty**, **prerequisites**, and **scheduling constraints**.
* Suggests **balanced semester loads** and **prerequisite ordering**.

### 🔍 Intelligent Web Scraping

* Uses Python to scrape:

  * Course descriptions
  * General education and major requirement pages
  * Prerequisite data (when available)

### 📚 Smart PDF Parsing

* Parses official major requirement PDFs (or exported text)
* Extracts:

  * Core and elective courses
  * Required credits
  * Special notes (e.g., “at least 2 upper-level electives”)

### 🧩 Interactive Customization

After the initial plan is generated, the user can:

* Move or swap courses between semesters
* Add summer sessions or overload terms
* Shorten degree completion to **3.5 years** (or fewer)
* Lock specific courses into preferred semesters
* Ask the AI to **re-optimize** based on changes

### 🌐 Full Stack Web App

| Layer    | Tech                      | Description                              |
| -------- | ------------------------- | ---------------------------------------- |
| Frontend | HTML / CSS / JavaScript   | Clean, lightweight interface             |
| Backend  | Python (Flask or FastAPI) | Handles parsing, scraping, and AI calls  |
| AI       | Google Gemini API         | Generates course plans and reasoning     |
| Scraping | BeautifulSoup / Requests  | Collects course & gen ed info            |
| Data     | JSON / local cache        | Stores scraped info and user preferences |

---

## 🛠️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/ai-course-planner.git
cd ai-course-planner
```

### 2. Set up the Python environment

```bash
python -m venv venv
source venv/bin/activate  # (Mac/Linux)
venv\Scripts\activate     # (Windows)
pip install -r requirements.txt
```

### 3. Add your Gemini API key

Create a `.env` file in the `backend/` directory:

```
GOOGLE_API_KEY=your_api_key_here
```

### 4. Run the backend

```bash
python backend/main.py
```

### 5. Open the frontend

Open `frontend/index.html` in your browser.

---

## 🧩 Example Flow

1. **Upload major requirements PDF**
   → Backend parses course list and requirements.

2. **AI web-scrapes** official course pages for gen-eds, electives, and descriptions.

3. **Gemini model generates** a balanced 8-semester plan, like:

   ```
   Fall 2025: CS101, MATH221, ENGL110, GENED1
   Spring 2026: CS102, MATH222, HIST101, GENED2
   ...
   ```

4. **You customize interactively**:

   * “Move CS201 to Spring 2027”
   * “Add a summer semester”
   * “Finish one semester early”

5. **AI regenerates** a revised, valid schedule reflecting your edits.

---

## 🧠 Planned Enhancements (Feasible in a Day with AI Help)

* [ ] **Difficulty Scoring** via course reviews / credit hours
* [ ] **Visualization**: timeline or credit-progress chart
* [ ] **Save / Load plans** as JSON or PDF
* [ ] **Auto prerequisite checking** using scraped course trees
* [ ] **Advisor Mode** – simulate “what-if” scenarios for switching majors
* [ ] **Multi-major or minor support**

---

## ⚙️ Technologies

| Category    | Stack                                     |
| ----------- | ----------------------------------------- |
| Language    | Python 3.11, JavaScript, HTML, CSS        |
| Backend     | Flask or FastAPI                          |
| AI API      | Google Gemini (via `google-generativeai`) |
| Scraping    | BeautifulSoup, Requests                   |
| Parsing     | PyPDF2 or pdfplumber                      |
| Environment | dotenv                                    |
| Frontend    | Vanilla JS or Tailwind (optional)         |

---

## 🧩 Example Prompts for Gemini

> “Given the following required courses and prerequisites, generate an optimized 8-semester plan minimizing difficulty overlap and ensuring all graduation requirements are met.”

> “Regenerate the plan so that MATH221 and PHYS201 are not taken in the same semester.”

> “Update the plan to finish in 3.5 years with one summer session.”

---

## 🤖 AI Workflow

```
PDF Parse → Requirement Extract → Web Scrape (Descriptions + GenEds)
   ↓
Gemini Model → Generate Initial Plan
   ↓
Frontend → User Edits + Constraints
   ↓
Gemini → Regenerate Revised Plan
```

---

## 🧑‍💻 Development Plan (Finish in ~5 hours)

| Time      | Task                                   |
| --------- | -------------------------------------- |
| 0:00–0:30 | Project setup, API key config          |
| 0:30–1:30 | Flask endpoints + test Gemini response |
| 1:30–2:30 | Frontend UI + fetch integration        |
| 2:30–3:30 | PDF parsing + scraping prototype       |
| 3:30–4:30 | Plan generation & editing logic        |
| 4:30–5:00 | Polish, test, deploy (optional)        |

---

## 🧾 License

MIT License © 2025 Your Name

---

## 🌟 Acknowledgments

Built with guidance from OpenAI GPT-5 and powered by Google Gemini.
Created as an AI-aided prototype for educational and project planning purposes.

---

Would you like me to generate the matching **`requirements.txt`** and **`.env.example`** files for this next, so it’s immediately runnable on GitHub Codespaces or Render?
