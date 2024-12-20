# 🎯 MultiModal GenProject

> An AI-powered multimodal generation application using FastAPI and Streamlit, demonstrating text, audio, and image generation using state-of-the-art generative AI models.

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

## ✨ Features

* **Text Generation** - Conversational chatbot functionality powered by state-of-the-art language models
* **Audio Generation** - Speech synthesis with customizable voice presets for natural-sounding audio
* **Image Generation** - Text-to-image synthesis using advanced diffusion models
* **Interactive Frontend** - User-friendly interface built with Streamlit
* **REST API** - Robust FastAPI backend for seamless integration

## 🏗️ Project Structure

```
MultiModal_GenProject/
│
├── app/
│   ├── __init__.py           # Package initialization
│   ├── aclient.py            # Streamlit audio generation client
│   ├── client.py             # Streamlit text generation client
│   ├── main.py               # FastAPI server
│   ├── models.py             # Model inference logic
│   ├── schemas.py            # Input validation schemas
│   ├── utils.py              # Audio/image processing utilities
│   └── vclient.py            # Streamlit image generation client
│
├── .env                      # Environment variables
├── .gitignore               
└── requirements.txt          # Project dependencies
```

## 🚀 Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/MultiModal_GenProject.git
   cd MultiModal_GenProject
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv env
   source env/bin/activate  # Windows: .\env\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   Create a `.env` file:
   ```env
   HF_TOKEN=your_hugging_face_token
   ```

5. **Launch the Server**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

6. **Run Streamlit Clients**
   ```bash
   # Text Generation
   streamlit run app/client.py
   
   # Audio Generation
   streamlit run app/aclient.py
   
   # Image Generation
   streamlit run app/vclient.py
   ```

## 🛣️ API Endpoints

| Endpoint | Description | Input | Output |
|----------|-------------|-------|--------|
| `/generate/text` | Text generation | `prompt` | JSON (text response) |
| `/generate/audio` | Audio synthesis | `prompt`, `preset` | WAV audio file |
| `/generate/image` | Text-to-image | `prompt` | PNG image |
| `/` | API documentation | None | OpenAPI Docs |

## 💡 Example Usage

### Text Generation
```bash
curl "http://localhost:8000/generate/text?prompt=Hello,%20how%20are%20you?"
```

### Audio Generation
```bash
curl "http://localhost:8000/generate/audio?prompt=Hello,%20world&preset=v2/en_speaker_1" \
     --output audio.wav
```

### Image Generation
```bash
curl "http://localhost:8000/generate/image?prompt=A%20sunset%20over%20mountains" \
     --output image.png
```

## 💼 Business Impact

* **Enhanced User Engagement** - Multimodal outputs create immersive experiences
* **Content Personalization** - Customizable voices and high-quality images
* **Scalable AI Foundation** - Perfect for virtual assistants and creative content generation
* **Rapid Development** - FastAPI's performance meets Streamlit's simplicity

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature-name`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
Made with ❤️ using FastAPI and Streamlit
