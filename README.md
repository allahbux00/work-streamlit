# AI Chat Assistant - Streamlit Version

A beautiful chat interface that can discuss any topic, powered by Streamlit.

## Deployment on Streamlit Cloud (100% Free)

1. Go to [GitHub.com](https://github.com) and create a new repository
   - Upload all files EXCEPT `.env`

2. Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign up/Login with your GitHub account
   - Click "New app"
   - Select your repository
   - In Advanced Settings, add your GROQ_API_KEY:
     - Key: `GROQ_API_KEY`
     - Value: `your_api_key_here`
   - Click "Deploy!"

Your app will be live in minutes with a public URL! No credit card needed.

## Local Development

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your API key:
```
GROQ_API_KEY=your_api_key_here
```

3. Run the app:
```bash
streamlit run streamlit_app.py
```

## Features

- Modern, clean UI
- Markdown support
- Chat history
- Mobile-friendly
- Can discuss any topic
- 100% free hosting on Streamlit Cloud
- No credit card needed

## Important

Keep your API key private - don't share it or commit it to GitHub!
