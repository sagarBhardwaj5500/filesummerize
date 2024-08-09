
import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState('');

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = () => {
    const formData = new FormData();
    formData.append('file', file);

    axios.post('http://localhost:8000/upload', formData)
      .then((response) => {
        console.log(response.data);
        axios.post('http://localhost:8000/summarize', formData)
          .then((response) => {
            setSummary(response.data.summary);
          })
          .catch((error) => {
            console.error(error);
          });
      })
      .catch((error) => {
        console.error(error);
      });
  };

  

  return (
    <div className="container centered">
      <h1>Document Summarizer</h1>
      <input type="file" onChange={handleFileChange} />
      <button className="upload-button highlighted-button" onClick={handleUpload}>Upload and Summarize</button>
      <p>Summary:</p>
      <textarea value={summary} readOnly />
    </div>
  );
}

export default App;