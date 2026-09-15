import { useState } from "react"

function App() {
  const [url, setUrl] = useState("")
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  async function askQuestion() {
    setLoading(true)
    setError("")
    setAnswer("")

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: url,
          question: question,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Something went wrong")
      }

      setAnswer(data.answer)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">

      <nav className="navbar">
        <div className="logo">
          <span className="logo-icon">▶</span>
          YouTube<span>Mind</span>
        </div>

        <div className="nav-tag">
          AI VIDEO ASSISTANT
        </div>
      </nav>

      <main className="main">

        <section className="hero">
          <div className="badge">
            ✦ YOUR PERSONAL VIDEO INTELLIGENCE
          </div>

          <h1>
            Don't watch the
            <br />
            <span>whole video.</span>
          </h1>

          <p>
            Give YouTubeMind the link.
            <br />
            Ask anything. Get the answer.
          </p>

          <div className="quote">
            "Your time is valuable. Let AI do the watching."
          </div>
        </section>

        <section className="workspace">

          <div className="card">

            <div className="step">
              <div className="step-number">01</div>

              <div>
                <h2>Add your YouTube video</h2>
                <p>
                  Paste the video link you want YouTubeMind to understand.
                </p>
              </div>
            </div>

            <div className="input-wrapper">
              <span className="input-icon">🔗</span>

              <input
                type="text"
                placeholder="Paste YouTube URL here..."
                value={url}
                onChange={(e) => setUrl(e.target.value)}
              />
            </div>

          </div>

          <div className="card">

            <div className="step">
              <div className="step-number">02</div>

              <div>
                <h2>Ask anything</h2>
                <p>
                  Summarize it, explain a concept, or ask a specific question.
                </p>
              </div>
            </div>

            <textarea
              placeholder="What do you want to know about this video?"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
            />

            <button onClick={askQuestion} disabled={loading}>
              {loading ? "Thinking..." : "Ask YouTubeMind"}
              <span>{loading ? "..." : "→"}</span>
            </button>

          </div>

          <div className="card answer-card">

            <div className="step">
              <div className="step-number">03</div>

              <div>
                <h2>Your answer</h2>
                <p>
                  Your AI-generated answer will appear here.
                </p>
              </div>
            </div>

            <div className="answer-box">
              {loading ? (
                <div className="answer-placeholder">
                  <div className="spark">✦</div>
                  <span>Understanding the video...</span>
                </div>
              ) : error ? (
                <div className="answer-placeholder">
                  <span>{error}</span>
                </div>
              ) : answer ? (
                <div className="answer-text">
                  {answer}
                </div>
              ) : (
                <div className="answer-placeholder">
                  <div className="spark">✦</div>
                  <span>Your answer will appear here...</span>
                </div>
              )}
            </div>

          </div>

        </section>

        <section className="features">

          <div>
            <strong>⚡ Fast</strong>
            <span>Get answers without watching the whole video.</span>
          </div>

          <div>
            <strong>◈ Context-aware</strong>
            <span>Answers are based on the video's transcript.</span>
          </div>

          <div>
            <strong>✦ AI-powered</strong>
            <span>Ask natural questions about any processed video.</span>
          </div>

        </section>

      </main>

      <footer>
        YouTubeMind <span>•</span> Understand more. Watch less.
      </footer>

    </div>
  )
}

export default App