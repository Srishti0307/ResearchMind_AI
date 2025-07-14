# 📚 ResearchMind AI - Smart Research Summarization Assistant

## 🔬 Overview

**ResearchMind AI** is an intelligent research document analysis tool that transforms complex academic papers into actionable insights. Using advanced AI powered by the Groq API, it provides instant summaries, interactive Q&A, and knowledge assessments for any research document.

### 🌐 Live Demo & Video

**🚀 Try it now:** [https://researchmind-ai-ez.streamlit.app/](https://researchmind-ai-ez.streamlit.app/)

**📺 Watch the demo:** [YouTube Video Tutorial](https://youtu.be/n5WZDDANiXo)

*Experience the full functionality without any setup - just upload your research document and start exploring!*

### ✨ Key Features

- **🤖 AI-Powered Summarization** - Generate comprehensive 150-word summaries of research papers
- **💬 Interactive Q&A** - Ask questions and get evidence-based answers from your documents
- **🎯 Knowledge Assessment** - Auto-generated quiz questions to test comprehension
- **📊 Document Analysis** - Detailed statistics, search functionality, and content exploration
- **📄 PDF Export** - Download summaries, Q&A sessions, and quiz results as professional PDFs
- **🔍 Smart Search** - Find specific content within research documents with context

---

## 🚀 Setup Instructions

### 🌐 Option 1: Try the Live Demo (Recommended)

**No setup required!** Experience ResearchMind AI instantly:
👉 **[Launch Live Demo](https://researchmind-ai-ez.streamlit.app/)**

### 🛠️ Option 2: Local Installation

### Prerequisites

- Python 3.8 or higher
- Groq API key (free at [console.groq.com](https://console.groq.com))

### 1. Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd ResearchMind_AI

# Or download and extract the ZIP file
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- `streamlit>=1.32.0` - Web application framework
- `requests>=2.31.0` - HTTP requests for API calls
- `python-dotenv>=1.0.0` - Environment variable management
- `PyPDF2>=3.0.1` - PDF document processing
- `reportlab>=4.0.4` - PDF generation and export

### 3. Set Up Environment Variables

Create a `.env` file in the project root directory:

```bash
# Create the .env file
touch .env  # On Windows: type nul > .env
```

Add your Groq API key to the `.env` file:

```env
GROQ_API_KEY="your_groq_api_key_here"
```

**To get your free Groq API key:**
1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy and paste it into your `.env` file

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### 5. Upload and Analyze

1. Upload a research document (PDF or TXT file)
2. Wait for AI analysis to complete
3. Explore summaries, ask questions, and take quizzes!

---

## 🏗️ Architecture & Reasoning Flow

### System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend        │    │   AI Service    │
│   (Streamlit)   │◄──►│   (Python)       │◄──►│   (Groq API)    │
│                 │    │                  │    │                 │
│ • File Upload   │    │ • Document       │    │ • Text          │
│ • UI/UX         │    │   Processing     │    │   Summarization │
│ • Interactions  │    │ • State Mgmt     │    │ • Q&A           │
│ • Downloads     │    │ • API Calls      │    │ • Quiz Gen      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   File System   │    │   Session State  │    │   Model         │
│                 │    │                  │    │                 │
│ • PDF/TXT       │    │ • User Data      │    │ • Llama 4       │
│ • Exports       │    │ • Chat History   │    │   Scout 17B     │
│ • Downloads     │    │ • Quiz Results   │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### 🔄 Processing Flow

#### 1. Document Upload & Processing
```
User Upload → File Validation → Content Extraction
     │              │                   │
     ▼              ▼                   ▼
PDF/TXT File → Size/Type Check → PyPDF2/Text Reader
     │              │                   │
     ▼              ▼                   ▼
File Object → Error Handling → Extracted Text
```

#### 2. AI Analysis Pipeline
```
Raw Text → Text Preprocessing → API Request Formation
    │            │                      │
    ▼            ▼                      ▼
Chunking → Context Optimization → Groq API Call
    │            │                      │
    ▼            ▼                      ▼
Summary Generation → Q&A Preparation → Quiz Creation
```

#### 3. Interactive Features Flow
```
User Interaction → Query Processing → AI Response
       │               │                │
       ▼               ▼                ▼
Question Input → Context Retrieval → Answer Generation
       │               │                │
       ▼               ▼                ▼
Quiz Attempt → Answer Evaluation → Feedback Provision
```

### 🧠 AI Reasoning System

#### Document Summarization
1. **Text Analysis**: Extract key themes, methodology, and findings
2. **Content Prioritization**: Identify most important research insights
3. **Synthesis**: Generate coherent 150-word summary
4. **Quality Check**: Ensure accuracy and completeness

#### Question Answering
1. **Query Understanding**: Parse user question intent
2. **Context Retrieval**: Find relevant document sections using keyword matching
3. **Evidence Synthesis**: Combine multiple document sources
4. **Response Generation**: Provide comprehensive, source-referenced answers

#### Quiz Generation
1. **Content Analysis**: Identify key concepts and learning objectives
2. **Question Creation**: Generate questions at different cognitive levels:
   - **Comprehension**: Factual understanding
   - **Analysis**: Theme and implication recognition
   - **Inference**: Critical thinking and synthesis
3. **Answer Generation**: Create detailed model responses
4. **Evaluation**: Assess user answers with constructive feedback

### 🔧 Technical Components

#### Core Technologies
- **Frontend**: Streamlit for interactive web interface
- **Backend**: Python for document processing and API integration
- **AI Model**: Meta-Llama/Llama-4-Scout-17B via Groq API
- **Document Processing**: PyPDF2 for PDF parsing
- **Export Generation**: ReportLab for PDF creation

#### Key Functions
- `read_pdf_file()` - Extract text from PDF documents
- `generate_summary()` - Create AI-powered research summaries
- `answer_question()` - Process Q&A with context retrieval
- `generate_quiz()` - Create assessment questions
- `call_groq_api_with_retry()` - Robust API communication with error handling

#### Session Management
- Document content and metadata storage
- Chat history persistence
- Quiz progress tracking
- User interaction state management

---

## 📁 Project Structure

```
ResearchMind_AI/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (API keys)
├── README.md            # Project documentation
├── .streamlit/          # Streamlit configuration
│   └── config.toml      # Theme and server settings
└── .gitattributes       # Git configuration
```

---

## 🎯 Usage Examples

### 📺 Video Demonstration

**🎬 Complete Walkthrough:** [Watch on YouTube](https://youtu.be/n5WZDDANiXo)

See ResearchMind AI in action! This video demonstrates:
- Document upload and processing
- AI summarization in real-time
- Interactive Q&A features
- Quiz generation and evaluation
- PDF export functionality

### Basic Workflow
1. **Upload**: Drop a research paper (PDF/TXT)
2. **Analyze**: AI processes and generates summary
3. **Explore**: Ask questions about methodology, findings, implications
4. **Test**: Take comprehension quiz
5. **Export**: Download results as PDF reports

### Supported Document Types
- ✅ Academic research papers
- ✅ Scientific publications
- ✅ Technical documentation
- ✅ Text-based PDFs
- ✅ Plain text files (.txt)

### File Requirements
- **Size**: Up to 15MB
- **Length**: 1000+ words recommended for best results
- **Format**: Text-extractable (not scanned images)

---

## 🛡️ Error Handling & Reliability

### Robust API Integration
- Automatic retry mechanism for failed requests
- Rate limiting protection
- Timeout handling
- Comprehensive error messaging

### Document Processing Safety
- File type validation
- Size limit enforcement
- Encoding detection and fallback
- Content length verification

### User Experience Protection
- Graceful error recovery
- Progress indicators
- Helpful error messages
- Session state preservation

---

## 🔒 Security & Privacy

- **API Key Protection**: Environment variable storage
- **No Data Persistence**: Documents processed in memory only
- **Session Isolation**: User data separated per session
- **Secure Communication**: HTTPS API calls to Groq

---

## 🚀 Future Enhancements

- 📊 Advanced analytics and visualizations
- 🔗 Multi-document comparison features
- 🌐 Support for additional file formats
- 📱 Mobile-optimized interface
- 🔄 Batch processing capabilities
- 🎨 Custom theming options

---

## 📞 Support & Contributing

For issues, questions, or contributions:
1. Check existing documentation
2. Review error messages and logs
3. Verify API key configuration
4. Ensure all dependencies are installed

**Common Issues:**
- **API Errors**: Verify Groq API key in `.env` file
- **PDF Issues**: Ensure PDF contains extractable text
- **Slow Performance**: Check internet connection and file size

---

## 📄 License

This project is created for educational and research purposes. Please ensure compliance with your institution's policies and the terms of service of any APIs used.

---

**🔬 Transform your research workflow with AI-powered insights!**
