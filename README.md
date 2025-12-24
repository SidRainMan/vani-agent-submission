# VANI (Voice Agent for Native Interaction) 🗣️

VANI is a voice-first, agentic AI system designed to help users in rural India identify government welfare schemes in their native language (**Bengali**). Unlike standard linear chatbots, VANI utilizes a **Planner-Executor-Evaluator** architecture to separate reasoning from response generation.

This system was built to demonstrate an autonomous workflow that can handle native language inputs, manage conversation state, and actively detect logical contradictions in user data.

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/sidrainman/vani-agent-submission.git](https://github.com/sidrainman/vani-agent-submission.git)
cd vani-agent-submission
2. Install Dependencies
Ensure you have Python 3.9+ installed, then run:

Bash

pip install -r requirements.txt
3. Google Cloud Configuration (Required)
This project uses Google Vertex AI and Cloud Text-to-Speech. You must provide valid credentials to run the agent.

Go to the Google Cloud Console.

Create a Service Account and grant it the following roles:

Vertex AI User

Cloud Text-to-Speech API User

Generate a JSON Key for this service account.

Rename the downloaded file to key.json.

Move key.json into the root folder of this repository (the same folder containing app.py).

Note: The key.json file is listed in .gitignore to prevent accidental commits.

▶️ Usage
Once the configuration is complete, launch the application:

Bash

streamlit run app.py
The application will open in your default browser at http://localhost:8501.

Demo Instructions
Grant Microphone Access: Allow the browser to access your microphone.

Speak in Bengali: Click the "Record" button and state your details (Name, Age, Occupation, Income, Caste).

Example: "Amar naam Siddhant. Amar boyosh 25. Ami ekjon chashi."

Monitor Internals: Open the sidebar to view the live Agent State, including extracted entities and real-time contradiction flags.


## 🚀 Key Features

* **Voice-First Interface:** Complete Speech-to-Text (STT) and Text-to-Speech (TTS) pipeline operating entirely in Bengali.
* **Agentic Reasoning:** Implements a cyclic state machine (using LangGraph) to plan next steps—deciding whether to ask for missing info, run tools, or resolve conflicts.
* **Contradiction Detection:** Features a custom logic layer that triggers a "Red Alert" resolution loop if the user provides conflicting data (e.g., changing age mid-conversation) rather than blindly overwriting memory.
* **Deterministic Guardrails:** Hybrid approach using LLMs for conversation and deterministic Python functions for strict eligibility rule enforcement (Age, Caste, Income limits).

---

## 🛠️ Architecture Overview

The system operates on three primary nodes:
1.  **Cognition Node (Planner):** Extracts entities and detects conflicts.
2.  **Tool Node (Executor):** Runs eligibility rules against the scheme database.
3.  **Generator Node (Evaluator):** Synthesizes the final Bengali audio response.

---
🧪 Scenarios to Test
Happy Path: Provide all details (Name, Age, Occupation, Income, Caste) to get an immediate scheme recommendation.

Missing Information: Provide partial details (e.g., just "I am a farmer"). The agent will dynamically ask for the missing Income and Caste fields.

Conflict Resolution: Try changing a core detail (like Age) in the middle of the conversation. The agent will detect the inconsistency and force a clarification loop.
