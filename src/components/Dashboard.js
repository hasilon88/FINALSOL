import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useLocation, useNavigate } from 'react-router-dom';

function humanReadableDate(isoDate) {
    const dateObject = new Date(isoDate);
    return dateObject.toLocaleString('en-US', {
        year: 'numeric',
        month: 'long',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
    });
}

const Dashboard = () => {
    const [recipientId, setRecipientId] = useState('');
    const [messageContent, setMessageContent] = useState('');
    const [sentMessages, setSentMessages] = useState([]);
    const [receivedMessages, setReceivedMessages] = useState([]);

    const location = useLocation();
    const navigate = useNavigate();
    const { email, password } = location.state || {};

    useEffect(() => {
        const fetchMessages = async () => {
            try {
                const response = await fetch(`http://localhost:8000/get_convo/${email}/${password}`);

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const data = await response.json();

                setSentMessages(data.sent_messages || []);
                setReceivedMessages(data.received_messages || []);

            } catch (error) {
                console.error('Error fetching messages:', error);
            }
        };

        fetchMessages();
        const intervalId = setInterval(fetchMessages, 3000);

        return () => clearInterval(intervalId);

    }, [email, password, messageContent]);

    const handleSendMessage = async () => {
        try {
            const response = await fetch('http://localhost:8000/create_message/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "email": email,
                    "receiverId": recipientId,
                    "content": messageContent
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            alert("Message sent successfully!");
            setRecipientId('');
            setMessageContent('');

        } catch (error) {
            console.error('There was an error sending the message:', error);
            alert('There was an error sending the message');
        }
    };

    return (
        <div className="container">
            <div className="d-flex justify-content-end mb-4">
                <button onClick={() => navigate("/login")} className="btn btn-danger">
                    Logout
                </button>
            </div>
            <h1>Welcome to the Dashboard</h1>
            <br/>
            <div className="row">
                <div className="col-md-6 mb-4">
                    <div className="box p-4 border rounded shadow-sm bg-white">
                        <h4 className="border-bottom pb-3 mb-3">Messages</h4>
                        <h5 className="mb-3">Sent</h5>
                        <ul className="list-group mb-4">
                            {sentMessages.slice().reverse().map((msg, index) => (
                                <li key={index} className="list-group-item">
                                     <div className='text-secondary'>{humanReadableDate(msg.datetime)}</div> <b>To {msg.receiver_name}:</b> {msg.content}
                                </li>
                            ))}
                        </ul>

                        <h5 className="mb-3">Received</h5>
                        <ul className="list-group">
                            {receivedMessages.slice().reverse().map((msg, index) => (
                                <li key={index} className="list-group-item">
                                    <div className='text-secondary'>{humanReadableDate(msg.datetime)}</div> <b>From {msg.sender_name}:</b> {msg.content}
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>

                <div className="col-md-6">
                    <div className="box p-4 border rounded shadow-sm bg-white">
                        <h4 className="border-bottom pb-3 mb-3">Send Message</h4>
                        <div className="mb-3">
                            <label className="form-label">Recipient ID</label>
                            <input
                                type="text"
                                placeholder="Recipient ID"
                                value={recipientId}
                                onChange={(e) => setRecipientId(e.target.value)}
                                className="form-control"
                            />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Message</label>
                            <textarea
                                rows="4"
                                placeholder="Your message..."
                                value={messageContent}
                                onChange={(e) => setMessageContent(e.target.value)}
                                className="form-control"
                            />
                        </div>
                        <button className="btn btn-primary" onClick={handleSendMessage}>
                            Send
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
