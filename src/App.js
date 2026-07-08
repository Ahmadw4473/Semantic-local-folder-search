import './App.css';
import React, { useState } from 'react';
import backgroundImage from './assets/images/images.jpg';

function App() {
  const [text, setText] = useState('');
  const [imgPath, setImagePath] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (event) => {
    setText(event.target.value);
  };

  async function fetchImages(query) {
    if (!query.trim()) return;

    try {
      setLoading(true);

      const response = await fetch('http://127.0.0.1:8000/getImage', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: query,
        }),
      });

      const data = await response.json();

      if (data) {
        setImagePath(data.image);
      }
    } catch (error) {
      console.log('Error fetching image:', error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      className="page"
      style={{ backgroundImage: `url(${backgroundImage})` }}
    >
      <div className="search-card">

        <h1>Semantic Folder Search Engine</h1>

        <p className="subtitle">
          Searching local images by meaning
        </p>

        <div className="search-box">
          <input
            id="user-input"
            type="text"
            value={text}
            onChange={handleChange}
            placeholder='Search anything...'
            onKeyDown={(e) => {
              if (e.key === 'Enter') fetchImages(text);
            }}
          />

          <button onClick={() => fetchImages(text)}>
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>

        <div className="result-area">
          {!imgPath && !loading && (
            <div className="empty-state">
              {/* <div className="empty-icon">🔍</div> */}
              <p>Your search result will appear here</p>
            </div>
          )}

          {loading && (
            <div className="loading-state">
              <div className="loader"></div>
              <p>Searching through embeddings...</p>
            </div>
          )}

          {imgPath && !loading && (
            <div className="image-result">
              <img
                src={`http://127.0.0.1:8000/image?path=${encodeURIComponent(imgPath)}`}
                alt="Search result"
              />

              <div className="image-info">
                <p>Matched Result</p>
                <span>{imgPath}</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;