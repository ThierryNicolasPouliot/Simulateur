import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const StockUpdates = () => {
    const { topic } = useParams();
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        const socket = new WebSocket(`ws://localhost:8000/ws/stocks/${topic}/`);

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setMessages((prevMessages) => [...prevMessages, data.message]);
        };

        return () => {
            socket.close();
        };
    }, [topic]);

    return (
        <div>
            <h2>Stock Updates for {topic}</h2>
            <ul>
                {messages.map((message, index) => (
                    <li key={index}>{message}</li>
                ))}
            </ul>
        </div>
    );
};

export default StockUpdates;
