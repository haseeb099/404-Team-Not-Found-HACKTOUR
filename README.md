# Anchor: Your AI Companion for Dementia Care

![Project Status](https://img.shields.io/badge/Status-Prototype-red)
![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Tech Stack](https://img.shields.io/badge/Tech-Python%2C%20FastAPI%2C%20HTML%2FCSS%2FJS%2C%20AI-green)

**Anchor is an innovative AI-powered companion designed to support individuals experiencing memory loss, particularly those with Alzheimer\'s or dementia, by intelligently managing and recalling personal memories.** This project was developed by 404-Team-Not-Found during the Global AI HackTour London 2026, aiming to provide a compassionate and professional solution for memory care.

## ✨ Features

*   **Intelligent Memory Management:** Stores and retrieves personal memories to assist patients in maintaining their sense of self and daily routine.
*   **Patient-Centric Interface:** A user-friendly interface tailored for individuals with memory impairment, ensuring ease of interaction.
*   **Carer Notification System:** Provides a dedicated view for carers to monitor patient interactions and receive important updates.
*   **Voice Interaction:** Leverages AI for natural language processing to facilitate intuitive voice-based communication.
*   **Privacy-First Design:** Built with considerations for sensitive health data, adhering to principles of UK GDPR Article 9 for special-category data (prototype only, not for production use).

## 🚀 Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Ensure you have `uv` (a fast Python package installer and resolver) installed. If not, you can install it via `pip`:

```bash
pip install uv
```

### Installation

1.  **Clone the repository:**

    ```bash
git clone https://github.com/MuhammadHaseebRafique/404-Team-Not-Found-HACKTOUR.git
cd 404-Team-Not-Found-HACKTOUR/anchor
    ```

2.  **Set up environment variables:**

    ```bash
cp .env.example .env
    ```
    Open `.env` and add your necessary API keys (e.g., for LLM services).

3.  **Install dependencies:**

    ```bash
uv sync
    ```

4.  **Run the application:**

    ```bash
uv run uvicorn backend.main:app --reload --port 8000
    ```

    The application will be accessible at:
    *   **Patient Interface:** `http://localhost:8000`
    *   **Carer Notification View:** `http://localhost:8000/carer`

### Resetting Demo Data

To reset the memory between demonstrations, use the following command:

```bash
curl -X POST http://localhost:8000/api/reset
```

## 💻 Tech Stack

*   **Backend:** Python, FastAPI, Uvicorn
*   **Frontend:** HTML5, CSS3, JavaScript
*   **AI/ML:** Large Language Models (LLMs) for natural language understanding and memory recall.
*   **Package Management:** `uv`

## 🏗️ Architecture / How It Works

Anchor operates with a clear separation between its backend and frontend components. The **backend**, built with Python and FastAPI, handles the core logic, including AI model interactions, memory storage, and data processing. It exposes a RESTful API for communication. The **frontend**, developed using standard web technologies (HTML, CSS, JavaScript), provides the user interfaces for both patients and carers, interacting with the backend API to display information and capture input. The system is designed to be modular, allowing for future expansion and integration of advanced AI capabilities.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💖 Acknowledgements

Made with ❤️ by 404-Team-Not-Found for the Global AI HackTour London 2026.

© 2026 Muhammad Haseeb Rafique. All rights reserved.