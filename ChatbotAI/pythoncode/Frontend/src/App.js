import { Button, Container, TextField, Typography } from "@mui/material";
import axios from "axios";
import React, { useEffect, useRef, useState } from "react";
import './App.css';

function App() {
  const [query, setQuery] = useState("");
  const [history, setHistory] = useState([]);
  const [isSubmitting, setIsSubmitting] = useState(false); 
  const chatContainerRef = useRef(null);

  // Handle submitting the user's query to the backend
  const handleSubmit = async () => {
    if (query.trim() === "" || isSubmitting) return; 

    setIsSubmitting(true); 

    // Add the query to the chat history immediately
    setHistory((prevHistory) => [
      ...prevHistory,
      { query, response: "..." } 
    ]);

    try {
      // Call the backend API
      const res = await axios.post("http://localhost:8000/chat", { user_input: query });

      // Extract and format the response from the backend
      const { response } = res.data;

      // Update the chat history with the response
      setHistory((prevHistory) => {
        const updatedHistory = [...prevHistory];
        updatedHistory[updatedHistory.length - 1] = { query, response }; 
        return updatedHistory;
      });
    } catch (error) {
      console.error(error);
      setHistory((prevHistory) => {
        const updatedHistory = [...prevHistory];
        updatedHistory[updatedHistory.length - 1] = { query, response: "Error fetching data." }; // Handle error
        return updatedHistory;
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  // Handle pressing Enter to submit the query
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault(); 
      handleSubmit(); 
    }
  };

  // Auto-scroll to the bottom of the chat container when history changes
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [history]);

  return (
    <Container className="chat-container">
      <Typography variant="h4" gutterBottom className="chat-title">
        Welcome to the Chatbot
      </Typography>

      <div className="chat-box" ref={chatContainerRef} style={{ maxHeight: '350px', overflowY: 'auto' }}>
        {/* Display chat history (queries and responses) */}
        {history.map((item, index) => (
          <div key={index} className="message">
            <div className="user-message">
              <Typography variant="body1">{`Q: ${item.query}`}</Typography>
            </div>
            <div className="bot-response">
              <Typography variant="body1">{`Ans: ${item.response}`}</Typography>
            </div>
          </div>
        ))}
      </div>

      {/* Input field for user query */}
      <TextField
        label="Enter your query"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="text-field"
        variant="outlined"
        fullWidth
        style={{ marginBottom: "10px" }}
        onKeyDown={handleKeyDown}
        disabled={isSubmitting} 
      />

      {/* Submit button */}
      <Button
        variant="contained"
        className="submit-button"
        onClick={handleSubmit}
        style={{ marginTop: "10px" }}
        disabled={isSubmitting} 
      >
        {isSubmitting ? "Processing..." : "Submit"} {/* Show "Processing..." while submitting */}
      </Button>
    </Container>
  );
}

export default App;
