import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ScenarioForm = () => {
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [backstory, setBackstory] = useState('');
    const [difficultyLevel, setDifficultyLevel] = useState('');
    const [duration, setDuration] = useState(0);
    const [companies, setCompanies] = useState([]);
    const [selectedCompanies, setSelectedCompanies] = useState([]);
    const [events, setEvents] = useState([]);
    const [selectedEvents, setSelectedEvents] = useState([]);
    const [triggers, setTriggers] = useState([]);
    const [selectedTriggers, setSelectedTriggers] = useState([]);
    const [customStats, setCustomStats] = useState([]);
    const [selectedCustomStats, setSelectedCustomStats] = useState([]);

    useEffect(() => {
        axios.get('/api/companies/')
            .then(res => setCompanies(res.data))
            .catch(err => console.log(err));

        axios.get('/api/events/')
            .then(res => setEvents(res.data))
            .catch(err => console.log(err));

        axios.get('/api/triggers/')
            .then(res => setTriggers(res.data))
            .catch(err => console.log(err));

        axios.get('/api/custom_stats/')
            .then(res => setCustomStats(res.data))
            .catch(err => console.log(err));
    }, []);

    const handleCompanyChange = (e) => {
        const options = e.target.options;
        const selected = [];
        for (const option of options) {
            if (option.selected) {
                selected.push(option.value);
            }
        }
        setSelectedCompanies(selected);
    };

    const handleEventChange = (e) => {
        const options = e.target.options;
        const selected = [];
        for (const option of options) {
            if (option.selected) {
                selected.push(option.value);
            }
        }
        setSelectedEvents(selected);
    };

    const handleTriggerChange = (e) => {
        const options = e.target.options;
        const selected = [];
        for (const option of options) {
            if (option.selected) {
                selected.push(option.value);
            }
        }
        setSelectedTriggers(selected);
    };

    const handleCustomStatChange = (e) => {
        const options = e.target.options;
        const selected = [];
        for (const option of options) {
            if (option.selected) {
                selected.push(option.value);
            }
        }
        setSelectedCustomStats(selected);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const scenarioData = {
            name, 
            description, 
            backstory, 
            difficulty_level: difficultyLevel,
            duration,
            companies: selectedCompanies, 
            events: selectedEvents,
            triggers: selectedTriggers,
            custom_stats: selectedCustomStats
        };
        axios.post('/api/scenarios/create/', scenarioData)
            .then(response => {
                alert('Scenario created successfully!');
            })
            .catch(error => {
                console.error('There was an error creating the scenario!', error);
            });
    };

    return (
        <div>
            <h2>Create a New Scenario</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Name:</label>
                    <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
                </div>
                <div>
                    <label>Description:</label>
                    <textarea value={description} onChange={(e) => setDescription(e.target.value)} required></textarea>
                </div>
                <div>
                    <label>Backstory:</label>
                    <textarea value={backstory} onChange={(e) => setBackstory(e.target.value)} required></textarea>
                </div>
                <div>
                    <label>Difficulty Level:</label>
                    <input type="text" value={difficultyLevel} onChange={(e) => setDifficultyLevel(e.target.value)} required />
                </div>
                <div>
                    <label>Duration (in seconds):</label>
                    <input type="number" value={duration} onChange={(e) => setDuration(e.target.value)} required />
                </div>
                <div>
                    <label>Select Companies:</label>
                    <select multiple onChange={handleCompanyChange}>
                        {companies.map(company => (
                            <option key={company.id} value={company.id}>{company.name}</option>
                        ))}
                    </select>
                </div>
                <div>
                    <label>Select Events:</label>
                    <select multiple onChange={handleEventChange}>
                        {events.map(event => (
                            <option key={event.id} value={event.id}>{event.name}</option>
                        ))}
                    </select>
                </div>
                <div>
                    <label>Select Triggers:</label>
                    <select multiple onChange={handleTriggerChange}>
                        {triggers.map(trigger => (
                            <option key={trigger.id} value={trigger.id}>{trigger.name}</option>
                        ))}
                    </select>
                </div>
                <div>
                    <label>Select Custom Stats:</label>
                    <select multiple onChange={handleCustomStatChange}>
                        {customStats.map(stat => (
                            <option key={stat.id} value={stat.id}>{stat.name}</option>
                        ))}
                    </select>
                </div>
                <button type="submit">Create Scenario</button>
            </form>
        </div>
    );
};

export default ScenarioForm;
