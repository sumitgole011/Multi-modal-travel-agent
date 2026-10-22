# 🌍 Multi-Modal Travel Agent

## Recruiter quick view

**Problem:** Travel research often requires switching between destination context, search results, weather and images.

**Solution:** A Streamlit travel assistant orchestrated with LangGraph that routes questions between retrieval and web search and brings together weather and image context.

**What to inspect:** Conditional routing, tool integrations, vector retrieval, error handling and the UI workflow described below.

**Repository navigation:** The application source is in the `multi-modal-travel-agent/` directory. A root-level ZIP archive is also present; use the source directory rather than treating the ZIP as the canonical code.

**Status note:** This description reflects the documented implementation. Live deployment, automated test coverage and response accuracy have not been independently verified here.


<p align="center">
  <b>An AI-powered travel assistant that brings travel information together through intelligent search, knowledge retrieval, and contextual insights.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/LangGraph-6C47FF?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/ChromaDB-Vector%20Database-2E8B57?style=for-the-badge" />
</p>

## ✨ About the Project

**Multi-Modal Travel Agent** is an AI-powered application designed to streamline travel information discovery using modern AI orchestration techniques.

Built with **LangGraph and Streamlit**, the application routes user queries between vector-database retrieval and web search. It also supports parallel retrieval of weather forecasts and destination images, helping bring relevant travel context into a structured, user-friendly interface.

The project demonstrates how multiple information sources and AI components can work together in a single travel assistant.

## 🚀 Key Features

- 🧠 **AI Workflow Orchestration:** Coordinates the application workflow using LangGraph.
- 🔀 **Intelligent Routing:** Uses conditional logic to route queries between vector retrieval and web search.
- 🔎 **Knowledge Retrieval:** Uses ChromaDB to retrieve relevant information from a vector database.
- 🌐 **Web Search:** Supplements retrieved knowledge with web-based information.
- 🌦️ **Weather Integration:** Fetches weather forecasts as additional travel context.
- 🖼️ **Destination Images:** Retrieves location-related imagery.
- ⚡ **Parallel Processing:** Fetches weather and image information concurrently.
- 🎨 **Interactive UI:** Provides a streamlined interface through Streamlit.
- 📋 **Structured Responses:** Organizes information into readable results.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| LangGraph | AI workflow orchestration and conditional routing |
| Streamlit | Interactive user interface |
| ChromaDB | Vector storage and semantic retrieval |
| OpenAI | Language-model integration |
| Grok | Additional AI integration, as configured |

## 🏗️ How It Works

The application follows a multi-step AI workflow:

**1. User Query** → The user submits a travel-related question through the interface.

**2. Workflow Orchestration** → LangGraph coordinates the execution flow.

**3. Conditional Routing** → The workflow directs the query to vector retrieval or web search according to its routing logic.

**4. Context Gathering** → Relevant information is retrieved, while weather and destination-image requests can run in parallel.

**5. Response Preparation** → The collected information is organized into a structured response.

**6. User Interface** → Streamlit presents the results in an accessible format.

## 🧰 Core Concepts Demonstrated

- Graph-based AI agent workflows
- Conditional routing and task orchestration
- Vector databases and semantic retrieval
- Integration of external information sources
- Concurrent information fetching
- Interactive application development with Streamlit

## 📦 Getting Started

### Prerequisites

- Python installed on your system
- Git
- API keys for the services configured in the project

### 1. Clone the Repository

```bash
git clone https://github.com/sumitgole011/multi-modal-travel-agent.git
cd multi-modal-travel-agent
```

### 2. Create a Virtual Environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

If a `requirements.txt` file is available in the application directory:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Set up the API keys required by your configured AI, search, weather, and image services.

Keep credentials in environment variables or a local `.env` file. Never commit API keys to GitHub.

### 5. Launch the Application

From the directory containing the Streamlit entry-point file, run:

```bash
streamlit run app.py
```

**Note:** Check the actual application directory, entry-point filename, and configuration requirements in the repository before running these commands.

## 💡 Potential Applications

- Travel destination discovery
- Context-aware travel information retrieval
- Weather-aware destination exploration
- AI-assisted research using multiple information sources
- Combining indexed knowledge with live search results

## 🔮 Future Enhancements

- 🗺️ Personalized, multi-day itinerary generation
- 💰 Travel budget estimation and cost comparison
- 🏨 Hotel and accommodation recommendations
- 🚆 Multi-modal transport planning
- 📅 Trip scheduling and itinerary management
- 🌐 Multilingual travel assistance
- 🚀 Cloud deployment and automated testing

These are potential extensions and are not necessarily part of the current implementation.

## 👨‍💻 Author

**Sumit Gole**

- GitHub: [@sumitgole011](https://github.com/sumitgole011)
- Repository: [Multi-Modal Travel Agent](https://github.com/sumitgole011/multi-modal-travel-agent)

---

<p align="center">
  <b>Exploring the intersection of AI agents, intelligent retrieval, and travel technology.</b>
</p>
