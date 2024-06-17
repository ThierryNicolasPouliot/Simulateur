import React, { useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const BuySell = () => {
    const { stockId } = useParams();
    const [amount, setAmount] = useState(0);
    const [price, setPrice] = useState(0.0);

    const handleBuy = () => {
        axios.post('/api/buy_stock/', { stock_id: stockId, amount, price })
            .then(response => {
                alert('Buy order placed successfully!');
            })
            .catch(error => {
                console.error('There was an error placing the buy order!', error);
            });
    };

    const handleSell = () => {
        axios.post('/api/sell_stock/', { stock_id: stockId, amount, price })
            .then(response => {
                alert('Sell order placed successfully!');
            })
            .catch(error => {
                console.error('There was an error placing the sell order!', error);
            });
    };

    return (
        <div>
            <h2>Buy/Sell Stock</h2>
            <div>
                <label>Amount:</label>
                <input type="number" value={amount} onChange={(e) => setAmount(e.target.value)} />
            </div>
            <div>
                <label>Price:</label>
                <input type="number" value={price} onChange={(e) => setPrice(e.target.value)} />
            </div>
            <button onClick={handleBuy}>Buy</button>
            <button onClick={handleSell}>Sell</button>
        </div>
    );
};

export default BuySell;
