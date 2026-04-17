Swasthya_Sahayak

A **high-fidelity, panic-resistant emergency voice assistant** designed to deliver **real-time first aid guidance** using **Edge AI + Retrieval-Augmented Generation (RAG)**.

Built for **low-connectivity and high-stress environments**, the system provides **instant, voice-driven medical assistance** with multilingual support tailored for India.

---

 Overview

In critical situations, users often lack immediate access to trained medical personnel. This system bridges that gap by combining:

* On-device AI (LLMs via Ollama)
* Trusted medical knowledge (WHO, Red Cross, NDMA)
* Voice-first interaction model

The result is a **fast, reliable, and offline-capable assistant** that delivers **clear, step-by-step emergency instructions**.

---

Key Features

 Voice-First Interaction

* Wake-word activated (hands-free usage)
* Continuous listening for emergency triggers
* Designed for panic scenarios

 Real-Time RAG Triage

* Retrieves verified medical instructions dynamically
* Uses domain-specific datasets (first aid & emergency care)
* Minimizes hallucinations

Edge AI Execution

* Runs locally using Ollama (no cloud dependency)
* Ensures privacy, low latency, and offline capability

 Mobile-Optimized HUD (100svh)

* Full-screen emergency interface
* Minimal cognitive load design
* High contrast + large actionable elements

 Multilingual Support

* Hindi
* Marathi
* Tamil
* Telugu

 Emergency Instruction Mode

* Short, command-based responses
* Prioritizes action over explanation
* Inspired by field medic protocols

---

 System Architecture

```text
User (Voice Input)
        ↓
Wake Word Detection (Porcupine)
        ↓
Speech-to-Text (Whisper)
        ↓
Query Processing Layer
        ↓
RAG Pipeline (ChromaDB + Embeddings)
        ↓
LLM Inference (medllama2 / llama3 via Ollama)
        ↓
Response Formatting (Step-based)
        ↓
Text-to-Speech (Coqui TTS)
        ↓
User (Voice Output)
```

---

 Tech Stack

 Frontend

* React (mobile-first architecture)
* Tailwind CSS (responsive HUD design)

Backend

* FastAPI (high-performance API layer)

 AI & Data

* LLMs: `medllama2`, `llama3`
* Vector Database: ChromaDB
* Embeddings: `nomic-embed-text`
* RAG pipeline (custom implementation)

 Voice Processing

* Wake Word: Porcupine
* Speech-to-Text: Whisper (faster-whisper)
* Text-to-Speech: Coqui TTS

---

 Data Sources

The assistant relies on authoritative medical datasets:

* World Health Organization
* International Federation of Red Cross and Red Crescent Societies
* National Disaster Management Authority

All responses are grounded in **retrieved context** rather than model-only generation.

---

Getting Started

Clone the Repository

```bash
git clone https://github.com/your-username/emergency-voice-assistant
cd emergency-voice-assistant
```

---

 Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

---

 Install Ollama & Models

```bash
ollama pull medllama2
ollama pull llama3
```

---

Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

RAG Pipeline (Concept)

1. Medical documents are ingested and chunked
2. Chunks are converted into embeddings
3. Stored in ChromaDB
4. On user query:

   * Relevant chunks are retrieved
   * Passed to LLM as context
   * Response is generated with grounding

---

 Safety Disclaimer

This system is intended for **first aid assistance only**.

* Not a substitute for professional medical diagnosis
* Always escalate severe cases to hospitals or emergency services

> If the condition is critical, seek immediate medical help.

---

 Use Cases

* Rural healthcare assistance
* Disaster and emergency response
* Offline medical guidance
* First aid education tools

---

 Future Enhancements

* Integration with emergency services (e.g., 108)
* GPS-based hospital recommendations
* Vision-based injury detection (CV models)
* Fine-tuned domain-specific medical LLM

---
 Contributing

Contributions are welcome.
Please open issues or submit pull requests for improvements.

---

License

MIT License

---

## 💡 Vision

To build a **reliable, accessible, and life-saving AI system** that empowers individuals to act effectively during medical emergencies—especially in underserved regions.

# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
