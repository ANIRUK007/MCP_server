from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from app.orchestrator import run_research

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <body>
            <h1>AI Research Tool</h1>
            <form action="/research" method="post">
                <input type="text" name="idea" placeholder="Enter idea" />
                <button type="submit">Research</button>
            </form>
        </body>
    </html>
    """

@app.post("/research", response_class=HTMLResponse)
def research(idea: str = Form(...)):
    result = run_research(idea)

    return f"""
    <html>
        <body>
            <h2>Research Result</h2>
            <pre>{result}</pre>
            <br>
            <a href="/">Go Back</a>
        </body>
    </html>
    """