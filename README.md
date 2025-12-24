Here is a clean, professional `README.md` tailored for your repository. It includes clear steps for the `key.json` setup and all necessary terminal commands.

```markdown
# VANI - Voice Agent for Native Interaction 🗣️

VANI is a voice-first, agentic AI system designed to help users identify government welfare schemes in their native language (**Bengali**). [cite_start]It uses a planner-executor-evaluator architecture powered by Google Vertex AI to reason, handle incomplete information, and detect contradictions in user input[cite: 2, 4, 11].

## 🚀 Features
* [cite_start]**Voice-First Interface:** Full Speech-to-Text (STT) and Text-to-Speech (TTS) pipeline supporting Bengali[cite: 9, 10].
* [cite_start]**Agentic Reasoning:** Uses LangGraph to manage state, plan next steps, and ask clarifying questions[cite: 11].
* [cite_start]**Contradiction Detection:** "Red Alert" logic to identify and resolve conflicting user data (e.g., changing age mid-conversation)[cite: 13].
* [cite_start]**Safety Guardrails:** deterministic checks to ensure scheme eligibility rules are strictly followed[cite: 12].

---

## 🛠️ Setup & Installation

Follow these steps to get the project running on your local machine.

### 1. Clone the Repository
Open your terminal and run:
```bash
git clone [https://github.com/sidrainman/vani-agent-submission.git](https://github.com/sidrainman/vani-agent-submission.git)
cd vani-agent-submission

```

### 2. Install Dependencies

Make sure you have Python installed. Then run:

```bash
pip install -r requirements.txt

```

---

## 🔑 Configuration (Critical Step)

This project requires a **Google Cloud Service Account** key to access Vertex AI (Gemini) and Text-to-Speech services.

1. **Go to Google Cloud Console:**
* Navigate to [IAM & Admin > Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts).


2. **Create a Service Account:**
* Click "Create Service Account". Give it a name (e.g., `vani-agent`).


3. **Grant Permissions:**
* Grant the account **Vertex AI User** and **Cloud Text-to-Speech API User** roles.


4. **Generate Key:**
* Click on the newly created email -> **Keys** tab -> **Add Key** -> **Create new key**.
* Select **JSON** and download the file.


5. **Add to Project:**
* Rename the downloaded file to exactly `key.json`.
* Move this `key.json` file into the **root folder** of this project (same folder as `app.py`).



> **⚠️ Security Note:** Never share your `key.json` or commit it to GitHub. This repository is configured to ignore it automatically.

---

## ▶️ How to Run

Once the dependencies are installed and the `key.json` is in place, start the application with:

```bash
streamlit run app.py

```

This will open the application in your default web browser (usually at `http://localhost:8501`).

---

## 🧪 How to Use the Demo

1. **Allow Microphone Access:** The browser will ask for permission to use your mic.
2. **Speak in Bengali:** Click "Record" and state your details (Name, Age, Occupation, etc.).
* *Example:* "Amar naam Siddhant. Amar boyosh 25. Ami ekjon chashi."


3. **View Internals:** Open the **Sidebar** on the left to see the agent's memory updating in real-time and any "Red Alert" contradictions.

```

```
