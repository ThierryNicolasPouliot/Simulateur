import React, { useState } from 'react';
import axios from 'axios';

const CompanyForm = () => {
    const [name, setName] = useState('');
    const [backstory, setBackstory] = useState('');
    const [maxShares, setMaxShares] = useState(1000);
    const [priceMaximum, setPriceMaximum] = useState(100);
    const [initialPrice, setInitialPrice] = useState(0.0);

    const handleSubmit = (e) => {
        e.preventDefault();
        const companyData = { 
            name, 
            backstory, 
            max_shares: maxShares, 
            price_maximum: priceMaximum, 
            initial_price: initialPrice
        };
        axios.post('/api/companies/create/', companyData)
            .then(response => {
                alert('Company created successfully!');
            })
            .catch(error => {
                console.error('There was an error creating the company!', error);
            });
    };

    return (
        <div>
            <h2>Create a New Company</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Name:</label>
                    <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
                </div>
                <div>
                    <label>Backstory:</label>
                    <textarea value={backstory} onChange={(e) => setBackstory(e.target.value)} required></textarea>
                </div>
                <div>
                    <label>Max Shares:</label>
                    <input type="number" value={maxShares} onChange={(e) => setMaxShares(e.target.value)} required />
                </div>
                <div>
                    <label>Price Maximum:</label>
                    <input type="number" value={priceMaximum} onChange={(e) => setPriceMaximum(e.target.value)} required />
                </div>
                <div>
                    <label>Initial Price:</label>
                    <input type="number" value={initialPrice} onChange={(e) => setInitialPrice(e.target.value)} required />
                </div>
                <button type="submit">Create Company</button>
            </form>
        </div>
    );
};

export default CompanyForm;
