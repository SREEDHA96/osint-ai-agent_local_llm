import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [report, setReport] = useState('');
  const [evaluation, setEvaluation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const stored = JSON.parse(localStorage.getItem('osintHistory')) || [];
    setHistory(stored);
  }, []);

  useEffect(() => {
    localStorage.setItem('osintHistory', JSON.stringify(history));
  }, [history]);

  const submitQuery = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setReport('');
    setEvaluation(null);
    try {
      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });

      if (!response.ok) throw new Error('Failed to fetch report');

      const data = await response.json();
      setReport(data.report);
      setEvaluation(data.evaluation || null);
      setHistory([{ query, timestamp: new Date().toISOString() }, ...history.slice(0, 9)]);
    } catch (err) {
      setReport(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const downloadReport = () => {
    const blob = new Blob([report], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'osint_report.txt';
    link.click();
    window.URL.revokeObjectURL(url);
  };

  const suggestions = [
    'Investigate Elon Musk’s recent business ventures',
    'Background of OpenAI’s board members',
    'Trace financial records of FTX founders',
    'Search for public appearances of Julian Assange'
  ];

  return (
    <div className="container">
      <h1>OSINT Intelligence Agent</h1>
      <div className="form">
        <input
          type="text"
          className="input"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter an OSINT investigation query..."
        />
        <button className="button" onClick={submitQuery} disabled={loading}>
          {loading ? 'Analyzing...' : 'Submit'}
        </button>
      </div>

      <div className="suggestions">
        <h3>Try a sample query:</h3>
        <ul>
          {suggestions.map((sug, idx) => (
            <li key={idx} onClick={() => setQuery(sug)}>{sug}</li>
          ))}
        </ul>
      </div>

      {report && (
        <div className="report">
          <h2>Generated Report</h2>
          <div className="report-text">{report}</div>
          <button className="button download-button" onClick={downloadReport}>
            Download Report
          </button>
        </div>
      )}

      {evaluation && (
        <div className="evaluation">
          <h2>Evaluation Results</h2>
          <ul>
            <li><strong>Score:</strong> {evaluation.score}</li>
            <li><strong>Accuracy:</strong> {evaluation.accuracy}</li>
            <li><strong>Coherence:</strong> {evaluation.coherence}</li>
            <li><strong>Completeness:</strong> {evaluation.completeness}</li>
            <li><strong>Reliability:</strong> {evaluation.reliability}</li>
            <li><strong>Verdict:</strong> {evaluation.verdict}</li>
          </ul>
        </div>
      )}

      {history.length > 0 && (
        <div className="history">
          <h2>Previous Queries</h2>
          <ul>
            {history.map((item, idx) => (
              <li key={idx}>{item.query} — {new Date(item.timestamp).toLocaleString()}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
