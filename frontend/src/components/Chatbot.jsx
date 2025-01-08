import React, { useState } from 'react';
import axios from 'axios';
import './Chatbot.css';

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [moodHistory, setMoodHistory] = useState([]);

    const sendMessage = async () => {
        if (!input.trim()) return;

        const userMessage = { sender: "user", text: input };
        setMessages((prev) => [...prev, userMessage]);

        try {
            // ✅ Update the URL here to match your backend server
            const response = await axios.post('http://127.0.0.1:5000/chat', {
                message: input
            });
            const botMessage = {
                sender: "bot",
                text: response.data.response,
                sentiment: response.data.sentiment
            };
            setMessages((prev) => [...prev, botMessage]);
            setMoodHistory((prev) => [...prev, response.data.sentiment]);
        } catch (error) {
            console.error("Error sending message:", error);
        }
        setInput("");
    };

    return (
        <div className="chat-container">
            <h2>Mental Health Chatbot</h2>
            <div className="chat-box">
                {messages.map((msg, index) => (
                    <p key={index} className={msg.sender}>
                        <strong>{msg.sender === "user" ? "You: " : "Bot: "}</strong>
                        {msg.text} {msg.sentiment && <span>({msg.sentiment})</span>}
                    </p>
                ))}
            </div>
            <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your message..."
            />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
};

export default Chatbot;
