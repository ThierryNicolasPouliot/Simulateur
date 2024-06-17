import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Portfolio = ({ userId }) => {
    const [portfolio, setPortfolio] = useState(null);

    useEffect(() => {
        axios.get(`/api/portfolio/${userId}/`)
            .then(response => {
                setPortfolio(response.data);
            })
            .catch(error => {
                console.error('Error fetching portfolio:', error);
            });
    }, [userId]);

    if (!portfolio) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h2>Portfolio</h2>
            <h3>Stocks</h3>
            <ul>
                {portfolio.stocks.map(stock => (
                    <li key={stock.id}>{stock.company.name}: {stock.price}</li>
                ))}
            </ul>
            <h3>Cryptocurrencies</h3>
            <ul>
                {portfolio.cryptocurrencies.map(crypto => (
                    <li key={crypto.id}>{crypto.name}: {crypto.price}</li>
                ))}
            </ul>
        </div>
    );
};

export default Portfolio;
