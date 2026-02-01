
import { useRef, useState } from 'react';
import './topsisai.css';

function Spinner() {
  return (
    <div className="spinner">
      <div className="loader" />
    </div>
  );
}

function SuccessState({ message }) {
  return (
    <div className="success-state">
      <svg className="checkmark" viewBox="0 0 52 52"><circle cx="26" cy="26" r="25" fill="none" stroke="#3fffa8" strokeWidth="3"/><path fill="none" stroke="#3fffa8" strokeWidth="4" d="M14 28l7 7 17-17"/></svg>
      <span>{message}</span>
    </div>
  );
}

function ErrorState({ message }) {
  return <div className="error-state">{message}</div>;
}

function App() {
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');
  const [form, setForm] = useState({ weights: '', impacts: '', email: '' });
  const fileRef = useRef();

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setError('');
    setSuccess(false);
    setLoading(true);
    const file = fileRef.current.files[0];
    if (!file) {
      setError('Please upload a CSV file.');
      setLoading(false);
      return;
    }
    if (!form.weights.trim() || !form.impacts.trim() || !form.email.trim()) {
      setError('All fields are required.');
      setLoading(false);
      return;
    }
    const data = new FormData();
    data.append('file', file);
    data.append('weights', form.weights);
    data.append('impacts', form.impacts);
    data.append('email', form.email);
    try {
      const res = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        body: data,
      });
      if (!res.ok) throw new Error('Server error.');
      const result = await res.json();
      if (result.success) {
        setSuccess(true);
      } else {
        setError(result.error || 'Unknown error.');
      }
    } catch (err) {
      setError('Failed to connect to server.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <main>
        <div className="glass-card">
          <div className="form-title">TOPSIS AI Analyzer</div>
          <form className="topsis-form" onSubmit={handleSubmit} autoComplete="off">
            <label className="input-label" htmlFor="file">Upload CSV</label>
            <input className="input-file" type="file" accept=".csv" id="file" ref={fileRef} required disabled={loading || success} />

            <label className="input-label" htmlFor="weights">Weights (comma-separated)</label>
            <input className="input-field" type="text" id="weights" name="weights" placeholder="e.g. 1,2,3,4" value={form.weights} onChange={handleChange} required disabled={loading || success} />

            <label className="input-label" htmlFor="impacts">Impacts (comma-separated, + or -)</label>
            <input className="input-field" type="text" id="impacts" name="impacts" placeholder="e.g. +,-,+,+" value={form.impacts} onChange={handleChange} required disabled={loading || success} />

            <label className="input-label" htmlFor="email">Email</label>
            <input className="input-field" type="email" id="email" name="email" placeholder="your@email.com" value={form.email} onChange={handleChange} required disabled={loading || success} />

            <button className="primary-btn" type="submit" disabled={loading || success}>Generate Ranking</button>
          </form>
          {loading && <Spinner />}
          {success && <SuccessState message="Ranking generated and emailed!" />}
          {error && <ErrorState message={error} />}
        </div>
        <footer className="footer">© {new Date().getFullYear()} TOPSIS AI Analyzer &middot; Built with React + Flask</footer>
      </main>
    </>
  );
}

export default App;
