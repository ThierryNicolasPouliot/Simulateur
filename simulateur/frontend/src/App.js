import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import CompanyForm from './components/CompanyForm';
import ScenarioForm from './components/ScenarioForm';
import StockUpdates from './components/StockUpdates';
import Dashboard from './components/Dashboard';
import Portfolio from './components/Portfolio';
import BuySell from './components/BuySell';
import Signup from './components/Signup';
import Login from './components/Login';

const App = () => {
    const [user, setUser] = useState(null);

    return (
        <Router>
            <Switch>
                <Route path="/dashboard" component={Dashboard} />
                <Route path="/create-company" component={CompanyForm} />
                <Route path="/create-scenario" component={ScenarioForm} />
                <Route path="/stocks/:topic" component={StockUpdates} />
                <Route path="/portfolio" render={() => <Portfolio userId={user ? user.id : null} />} />
                <Route path="/buy-sell/:stockId" component={BuySell} />
                <Route path="/signup" component={Signup} />
                <Route path="/login" render={() => <Login setUser={setUser} />} />
                <Route path="/" exact component={Dashboard} />
            </Switch>
        </Router>
    );
};

export default App;
