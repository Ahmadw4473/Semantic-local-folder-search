import './App.css';
import React, { useState } from 'react';

function App() {

  const [text, setText] = useState('');
  const [imgPath, setImagePath] = useState('');

  const handleChange = (event) => {
    setText(event.target.value);
  };

  async function fetchImages(query) {
    const response = await fetch('http://127.0.0.1:8000/getImage', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text: query
      })
    })
    const data = await response.json()
    if (data) {
      setImagePath(data.image)
    }
  }

  return (
    <>
      <input
        id="user-input"
        type="text"
        value={text}
        onChange={handleChange}
        placeholder="Type something..."
      />
      <button type="submit" onClick={() => fetchImages(text)}>Click Me</button>
      <div className="App">
        {imgPath && <img src={`http://127.0.0.1:8000/image?path=${encodeURIComponent(imgPath)}`} />}
      </div>

    </>
  );

}

export default App;
