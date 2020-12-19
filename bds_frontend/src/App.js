import { Component } from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';

import WebNavbar from './components/layout/WebNavbar';
import Dashboard from './pages/dashboard/Dashboard';
import Data from './pages/data/Data';
import Register from './pages/register/Register';
import Login from './pages/login/Login';
import Logout from './pages/logout/Logout';

// CSS:
import '../node_modules/bootstrap/dist/css/bootstrap.min.css'
import './App.css';

class App extends Component {
  render() {
    return (
      <div>
        <WebNavbar />

        <Switch>
          <Route path="/dashboard">
            <Dashboard />
          </Route>

          <Route path="/data">
            <Data />
          </Route>

          <Route path="/register">
            <Register />
          </Route>

          <Route path="/login">
            <Login />
          </Route>

          <Route path="/logout">
            <Logout />
          </Route>

          {/* Set default page: */}
          <Route exact path="/">
            <Redirect to="/data" />
          </Route>
        </Switch>
      </div>
    )
  }
}

export default App;
