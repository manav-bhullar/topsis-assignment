import { useState, useRef } from 'react';
import './App.css';

function Spinner() {
  return (
    <div className="spinner-container">
      <div className="spinner"></div>
      <div className="spinner-text">Analyzing your data...</div>
    </div>
  );
}

function SuccessMessage() {
  return (
    <div className="success-container">
      <div className="checkmark-icon">
        <svg viewBox="0 0 52 52" xmlns="http://www.w3.org/2000/svg">
          <circle cx="26" cy="26" r="25" fill="none" stroke="currentColor" strokeWidth="3" style={{ color: '#3fffff' }} />
          <path d="M14.1 27.2l7.1 7.2 16.7-16.8" fill="none" stroke="currentColor" strokeWidth="3" style={{ color: '#3fffff' }} strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </div>
      <div className="success-text">Analysis complete! Check your email for the results.</div>
    </div>
  );
}

function ErrorMessage({ message }) {
  return (
    <div className="error-container">
      <div className="error-text">{message}</div>
    </div>
  );
}

function App() {
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    weights: '',
    impacts: '',
    email: ''
  });
  const fileInputRef = useRef();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess(false);
    setLoading(true);

    const file = fileInputRef.current?.files?.[0];

    if (!file) {
      setError('Please select a CSV file to upload.');
      setLoading(false);
      return;
    }

    if (!formData.weights.trim() || !formData.impacts.trim() || !formData.email.trim()) {
      setError('Please fill in all fields.');
      setLoading(false);
      return;
    }

    const data = new FormData();
    data.append('file', file);
    data.append('weights', formData.weights);
    data.append('impacts', formData.impacts);
    data.append('email', formData.email);

    try {
      console.log('[DEBUG] Sending request to http://localhost:5001/analyze');
      const response = await fetch('http://localhost:5001/analyze', {
        method: 'POST',
        body: data,
      });

      const result = await response.json();
      console.log('[DEBUG] Response:', result);

      if (result.success) {
        setSuccess(true);
        // Reset form after 2 seconds
        setTimeout(() => {
          setFormData({ weights: '', impacts: '', email: '' });
          if (fileInputRef.current) fileInputRef.current.value = '';
          setSuccess(false);
        }, 3000);
      } else {
        setError(result.error || 'An error occurred during analysis.');
      }
    } catch (err) {
      console.error('[DEBUG] Fetch error:', err);
      setError('Failed to connect to the backend server. Make sure it\'s running on http://localhost:5001');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="glass-card">
        <h1 className="app-title">TOPSIS AI Analyzer</h1>
        <p className="app-subtitle">Analyze and rank your data intelligently</p>

        <form className="topsis-form" onSubmit={handleSubmit} autoComplete="off">
          <div className="form-group">
            <label htmlFor="file" className="form-label">Upload CSV File</label>
            <input
              type="file"
              id="file"
              accept=".csv"
              ref={fileInputRef}
              className="form-file"
              disabled={loading || success}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="weights" className="form-label">Weights (comma-separated)</label>
            <input
              type="text"
              id="weights"
              name="weights"
              placeholder="e.g., 1,2,3,4,5"
              className="form-input"
              value={formData.weights}
              onChange={handleInputChange}
              disabled={loading || success}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="impacts" className="form-label">Impacts (comma-separated, + or -)</label>
            <input
              type="text"
              id="impacts"
              name="impacts"
              placeholder="e.g., +,-,+,+,+"
              className="form-input"
              value={formData.impacts}
              onChange={handleInputChange}
              disabled={loading || success}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="email" className="form-label">Email Address</label>
            <input
              type="email"
              id="email"
              name="email"
              placeholder="your@email.com"
              className="form-input"
              value={formData.email}
              onChange={handleInputChange}
              disabled={loading || success}
              required
            />
          </div>

          <button
            type="submit"
            className="btn-primary"
            disabled={loading || success}
          >
            {loading ? 'Analyzing...' : 'Generate Ranking'}
          </button>
        </form>

        {loading && <Spinner />}
        {success && <SuccessMessage />}
        {error && <ErrorMessage message={error} />}
      </div>

      <footer className="app-footer">
        <p>© 2025 TOPSIS AI Analyzer • Built with React + Flask</p>
      </footer>
    </div>
  );
}

export default App;
