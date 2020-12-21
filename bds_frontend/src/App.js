import { Component } from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';
import axios from 'axios';

import Dashboard from './pages/dashboard/Dashboard';
import Data from './pages/data/Data';
import Register from './pages/register/Register';
import Login from './pages/login/Login';
import Logout from './pages/logout/Logout';

// CSS:
import '../node_modules/bootstrap/dist/css/bootstrap.min.css'
import './App.css';

// CSRF-Token:
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
var csrftoken = getCookie('csrftoken');

// Configure axios:
axios.defaults.headers.common['X-CSRFToken'] = csrftoken;

class App extends Component {
  render() {
    return (
      <div>
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
