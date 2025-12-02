# 🤖 AI-Powered Personal Learning Coach (Multi-Agent System)

## 🌟 Personalized, Dynamic, and Goal-Oriented Learning Experience

Beginner students often face the challenge of resource abundance and lack of direction. The endless flow of information on the internet makes it difficult to know where to start a learning journey, what is essential, and how to ensure consistent progress.

This project introduces a **Multi-Agent Artificial Intelligence (AI) Learning Coach** designed to solve this core challenge. It is personalized, dynamic, and possesses memory. The system guides the learning process by understanding the user's unique goals, researching up-to-date resources, and creating personalized, daily study plans.

---

## 🎯 The Core Problem and Solution

| Category | Problem | Solution |
|----------|---------|----------|
| **The Problem** | Beginner students feel directionless amidst resource overflow and complex learning paths. | Providing the student with a consistent and structured roadmap via a personalized, dynamic, memory-enabled system. |
| **Learning** | Passive and one-size-fits-all content consumption. | Delivering personalized daily plans with continuous feedback to support active learning. |

---

## 🧠 System Architecture: Multi-Agent Approach

The system consists of five main AI agents, each with a defined, focused task.

### 1. ⚙️ Orchestration Agent
**Role:** The brain and coordinator of the entire system. It receives the initial user input, initiates the flow, and directs tasks to the appropriate agents. It manages inter-agent communication.

### 2. 👤 Profile Agent
**Role:** Understands the user's current knowledge level, learning goals (e.g., "Learn fundamental Python in 1 month"), preferred learning style (visual, hands-on, etc.), and time constraints. It saves this data to the Long-Term Memory (LTM).

### 3. 🔍 Research Agent
**Role:** Finds current, high-quality learning resources relevant to the goals defined by the Profile Agent.

**Tool:** Utilizes the Google Search tool to find up-to-date articles, tutorials, and documentation.

**Output:** A prioritized list of topics, resource links, and learning objectives.

### 4. 🗓️ Planning Agent (The Loop)
**Role:** Creates personalized daily study plans using the resources provided by the Research Agent and the preferences set by the Profile Agent.

**Key Feature:** Operates as a Loop Agent. It dynamically adjusts the next day's plan based on feedback received from the Evaluation Agent at the end of each session.

### 5. ✅ Evaluation Agent
**Role:** Assesses how much of the day's plan the user completed, which topics they struggled with, and the overall learning outcome.

**Feedback:** Sends this evaluation to the Planning Agent, enabling the plan's dynamic adjustment.

---

## 🛠️ Key Features and Tools

| Feature | Description | Benefit |
|---------|-------------|---------|
| **Google Search Tool** | Allows the Research Agent to access current and diverse resources. | Ensures that the learning content is always up-to-date and relevant. |
| **Long-Term Memory (LTM)** | Stores profile information, completed lessons, and historical evaluation data. | Makes the plans smarter and more accurate over time by remembering the student's progress. |
| **Sessions** | Manages each daily study period or learning objective as an isolated session. | Helps the student focus on one topic and facilitates accurate feedback from the Evaluation Agent. |
| **Loop Agent** | The Planning Agent operates in a continuous feedback loop (Plan-Execute-Evaluate-Adjust). | Enables real-time adaptation of the plan based on the student's pace and performance. |
| **Custom Tool (Placeholder)** | A slot for custom tools that can be developed for specific project needs (e.g., integration with a coding practice simulator). | Increases the system's flexibility and future extensibility. |

---

## 🌊 Workflow Diagram

The interaction and flow between all the agents in the system is illustrated below:

### Flow Summary:

1. **Input:** User provides a learning goal to the Orchestration Agent.
2. **Personalization:** Orchestration → Profile Agent (Save data to LTM).
3. **Resource Gathering:** Profile Agent → Research Agent (Find resources using Google Search).
4. **Daily Plan:** Research → Planning Agent (Create the personalized daily study plan).
5. **Execution:** User executes the plan. (Session begins)
6. **Feedback:** User → Evaluation Agent (Learning outcome/difficulties).
7. **Loop:** Evaluation → Planning Agent (Revise the plan and create a new daily plan).
8. **Repeat:** The process remains in the loop until the user's goal is completed.

---

## 🚀 Getting Started

1. Clone the repository.
2. Install the necessary dependencies.
3. Configure your Google Search API key and language model settings in the `config.yaml` file.
4. Run the main script and enter your first learning objective!

---

## 🤝 Contributing

We welcome contributions! Any suggestions, bug fixes, or ideas for new agent/tool integrations are appreciated. Please feel free to open a Pull Request.