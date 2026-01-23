# 🤖 AI-Powered Personal Learning Coach (Multi-Agent System)

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Problem & Solution](#-problem--solution)
3. [System Architecture](#-system-architecture)
4. [Key Features](#-key-features)
5. [Project Structure](#-project-structure)
6. [Installation & Setup](#-installation--setup)
7. [Usage](#-usage)
8. [Documentation](#-documentation)
9. [Contributing](#-contributing)

---

## 🌟 Overview

**AI-Powered Personal Learning Coach** is a multi-agent AI system designed to help beginner students learn effectively by providing **personalized, dynamic, and goal-oriented guidance**.

The system solves the core challenge of information overload by:
- Understanding each student's unique learning goals and current knowledge level
- Researching and curating up-to-date learning resources
- Creating personalized daily study plans
- Providing continuous feedback and adapting plans based on performance
- Maintaining long-term memory of progress and preferences

---

## 🎯 Problem & Solution

| Aspect | Challenge | Solution |
|--------|-----------|----------|
| **Direction** | Students feel lost amidst resource overflow and complex learning paths | Personalized, dynamic roadmap guided by AI agents |
| **Content** | Passive, one-size-fits-all learning experiences | Curated, personalized daily plans with active feedback loops |
| **Progress** | No consistent tracking or adaptation | Memory-enabled system that learns and adapts continuously |
| **Quality** | Outdated or irrelevant resources | Google Search integration for current, high-quality materials |

---

## 🧠 System Architecture

The system uses a **multi-agent approach** where each AI agent has a specific, focused responsibility:

### Core Agents

#### 1. **Orchestrator Agent** (`orchestrator_agent.py`)
- **Role:** Central coordinator and brain of the system
- **Responsibilities:**
  - Receives and processes initial user input
  - Directs workflows between other agents
  - Manages inter-agent communication
  - Initiates the learning journey

#### 2. **Roadmap Agent** (`roadmap_agent.py`)
- **Role:** Strategic curriculum planner
- **Responsibilities:**
  - Creates comprehensive learning roadmaps
  - Defines learning objectives and milestones
  - Structures long-term learning goals
  - Plans the overall learning path

#### 3. **Content Curator Agent** (`content_curator_agent.py`)
- **Role:** Research and resource discovery specialist
- **Responsibilities:**
  - Finds current, high-quality learning resources
  - Uses Google Search for up-to-date materials
  - Prioritizes and organizes learning resources
  - Links resources to specific learning objectives

#### 4. **Assessment Agent** (`assessment_agent.py`)
- **Role:** Initial evaluation and knowledge level detector
- **Responsibilities:**
  - Conducts initial level assessment tests
  - Evaluates user's current knowledge
  - Identifies knowledge gaps
  - Personalizes content based on assessment results

#### 5. **Quiz Validation Agent** (`quiz_validation_agent.py`)
- **Role:** Learning outcome validator
- **Responsibilities:**
  - Generates quiz questions for learned topics
  - Validates quiz answers
  - Scores learning outcomes
  - Provides feedback on understanding

#### 6. **Progress Agent** (`progress_agent.py`)
- **Role:** Performance tracker and plan adjuster
- **Responsibilities:**
  - Tracks daily progress and completion
  - Evaluates learning outcomes
  - Adjusts future plans based on performance
  - Maintains learning consistency

### Memory System
- **Memory Bank** (`memory/memory_bank.py`): Stores user profiles, learning history, and progress data
- **Session Service** (`memory/session_service.py`): Manages individual learning sessions
- **Persistent Storage** (`data/memory/user_profile_store.json`): Long-term user data

### Tools & Utilities
- **AI Service** (`tools/ai_service.py`): Gemini API integration for AI capabilities
- **Google Search Tool** (`tools/google_search.py`): Finds and retrieves learning resources
- **Quiz Scoring** (`tools/quiz_scoring.py`): Evaluates quiz performance

---

## 🛠️ Key Features

| Feature | Description | Benefit |
|---------|-------------|---------|
| **Multi-Agent Architecture** | Specialized AI agents for different tasks | Modular, maintainable, and scalable system |
| **Personalization** | Adapts to individual learning styles and pace | Each student gets a unique learning experience |
| **Dynamic Planning** | Adjusts daily plans based on performance feedback | Plans improve and evolve with student progress |
| **Long-Term Memory** | Stores profiles, history, and progress data | System learns and makes smarter decisions over time |
| **Current Resources** | Google Search integration for latest materials | Always access up-to-date, relevant learning content |
| **Assessment** | Initial level testing and continuous evaluation | Accurate understanding of knowledge level and gaps |
| **Web Interface** | Streamlit-based user dashboard | Intuitive, interactive learning experience |
| **Session Management** | Isolated learning sessions with focused objectives | Clear structure for daily learning and feedback |

---

## 📁 Project Structure

```
Personal_learning_coach/
│
├── 📄 app.py                          # Streamlit web interface (main UI)
├── 📄 main.py                         # CLI demo script
├── 📄 debug_api.py                    # API debugging utilities
├── 📄 debug_quiz.py                   # Quiz debugging utilities
├── 📄 interactive_demo.py             # Interactive demonstration
├── 📄 repro_assessment.py             # Assessment reproduction script
│
├── 🗂️ src/                            # Core application source code
│   ├── agents/                        # AI agents
│   │   ├── orchestrator_agent.py      # System coordinator
│   │   ├── roadmap_agent.py           # Curriculum planner
│   │   ├── content_curator_agent.py   # Resource finder
│   │   ├── assessment_agent.py        # Level assessor
│   │   ├── progress_agent.py          # Performance tracker
│   │   └── quiz_validation_agent.py   # Quiz validator
│   │
│   ├── memory/                        # Memory management
│   │   ├── memory_bank.py             # Central memory storage
│   │   └── session_service.py         # Session manager
│   │
│   ├── models/                        # Data models
│   │   ├── user.py                    # User model
│   │   └── programs.py                # Learning program model
│   │
│   └── tools/                         # External tools & utilities
│       ├── ai_service.py              # Gemini API wrapper
│       ├── google_search.py           # Google Search integration
│       └── quiz_scoring.py            # Quiz evaluation
│
├── 🗂️ data/                           # Data storage
│   ├── users.json                     # User database
│   ├── memory/
│   │   └── user_profile_store.json    # Long-term user profiles
│   └── examples/
│       ├── demo_input.json            # Demo input data
│       └── sample_daily_plan.json     # Sample plan template
│
├── 🗂️ docs/                           # Documentation (Turkish)
│   ├── AI_TABANLI_SISTEM.md          # AI system documentation
│   ├── GUNLUK_AKIS.md                # Daily workflow guide
│   ├── IYILESTIRMELER.md             # Improvements
│   ├── KULLANIM_KILAVUZU.md          # User guide
│   ├── QUIZ_SISTEMI_DUZELTMESI.md    # Quiz system fixes
│   └── SETUP_GUIDE.md                # Setup instructions
│
├── 🗂️ tests/                          # Unit tests
│   ├── test_persistence.py            # Memory persistence tests
│   └── test_quiz.py                   # Quiz system tests
│
├── 📋 requirements.txt                # Python dependencies
├── 📝 config.py                       # Configuration settings
└── 📄 README.md                       # This file
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- API Keys:
  - Google Generative AI (Gemini)
  - Google Custom Search API (optional)

### Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Personal_learning_coach
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys**
   - Create a `.env` file in the root directory:
     ```
     GOOGLE_API_KEY=your_google_api_key
     GOOGLE_SEARCH_API_KEY=your_search_api_key
     GEMINI_API_KEY=your_gemini_api_key
     ```

4. **Verify setup**
   ```bash
   python main.py
   ```

---

## 💻 Usage

### Web Interface (Recommended)
Run the Streamlit application for an interactive experience:
```bash
streamlit run app.py
```

Access the application at `http://localhost:8501`

### CLI Demo
Run the command-line demonstration:
```bash
python main.py
```

### Interactive Demo
Try the interactive demonstration:
```bash
python interactive_demo.py
```

### Debug Utilities
- Test API connectivity: `python debug_api.py`
- Test quiz system: `python debug_quiz.py`
- Test assessments: `python repro_assessment.py`

---

## 📚 Documentation

Comprehensive documentation in Turkish (`docs/` folder):
- **SETUP_GUIDE.md** - Complete setup instructions
- **KULLANIM_KILAVUZU.md** - User guide and tutorials
- **AI_TABANLI_SISTEM.md** - Technical AI system details
- **GUNLUK_AKIS.md** - Daily workflow and operations
- **QUIZ_SISTEMI_DUZELTMESI.md** - Quiz system improvements
- **IYILESTIRMELER.md** - Enhancement documentation

---

## 🔄 Workflow Summary

```
1. USER INPUT
   ↓
2. ORCHESTRATOR AGENT → Receives and routes requests
   ↓
3. ASSESSMENT AGENT → Evaluates current knowledge level
   ↓
4. ROADMAP AGENT → Creates learning curriculum
   ↓
5. CONTENT CURATOR → Finds relevant learning resources
   ↓
6. DAILY PLANNING → Creates personalized daily plan
   ↓
7. USER EXECUTION → Student follows the plan
   ↓
8. ASSESSMENT → Quiz and progress evaluation
   ↓
9. PROGRESS AGENT → Analyzes performance
   ↓
10. FEEDBACK LOOP → Adjusts next day's plan
    └→ Returns to step 6
```

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes and test thoroughly
4. Commit with clear messages (`git commit -m 'Add your feature'`)
5. Push to your fork (`git push origin feature/your-feature`)
6. Open a Pull Request

### Areas for Contribution
- New agent implementations
- Additional assessment methods
- Integration with new learning platforms
- Performance optimizations
- Documentation improvements
- Bug fixes and testing

---

## 📝 License

This project is open source. Please check the LICENSE file for details.

---

## 📧 Support & Contact

For questions, issues, or suggestions, please open an issue in the repository.

---

**Last Updated:** January 2026