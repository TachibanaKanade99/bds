import { Component } from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';

// axios:
import axios from 'axios';

// cookie:
import Cookies from 'js-cookie';

// import components:
import Login from './pages/login/Login';
import Register from './pages/register/Register';

import Dashboard from './pages/dashboard/Dashboard';
import Data from './pages/data/Data';

// CSS:
import '../node_modules/bootstrap/dist/css/bootstrap.min.css'
import './App.css';

// CSRF-Token:
// function getCookie(name) {
//   let cookieValue = null;
//   if (document.cookie && document.cookie !== '') {
//       const cookies = document.cookie.split(';');
//       for (let i = 0; i < cookies.length; i++) {
//           const cookie = cookies[i].trim();
//           // Does this cookie string begin with the name we want?
//           if (cookie.substring(0, name.length + 1) === (name + '=')) {
//               cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//               break;
//           }
//       }
//   }
//   return cookieValue;
// }
// var csrftoken = getCookie('csrftoken');

// Configure axios:
// axios.defaults.headers.common['X-CSRFToken'] = csrftoken;

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isAuthenticated: true,
    }

    this.checkAuthentication = this.checkAuthentication.bind(this);
  }

  componentDidMount() {
    this.checkAuthentication();
  }

  checkAuthentication = () => {
    let self = this
    axios
      .get("/bds/check_authentication/", {
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
        }
      })
      .then(function(res) {
        // console.log(res.data.detail);
        self.setState({ isAuthenticated: true })
      })
      .catch(function(err) {
        // console.log(err);
        self.setState({ isAuthenticated: false })
      })
  }

  render() {
    return (
      <div>
        <Switch>
          {/* <Route path="/dashboard"> <Dashboard /> </Route> */}
          {/* <Route path="/data"> <Data /> </Route> */}
          <Route path="/dashboard" render={(props) => {
            let auth = this.state.isAuthenticated;
            if (props.location.state !== null && props.location.state !== undefined) {
              auth = props.location.state.isAuthenticated;
            }
            return auth === true ? <Dashboard {...props} /> : <Redirect to={{ pathname: '/login', state: { message: "You need to login to view content!" } }} />
          }}>
          </Route>

          <Route path="/data" render={(props) => {
            let auth = this.state.isAuthenticated;
            // console.log(props.location.state);
            if (props.location.state !== null && props.location.state !== undefined) {
              auth = props.location.state.isAuthenticated;
            }
            return auth === true ? <Data {...props} /> : <Redirect to={{ pathname: '/login', state: { message: "You need to login to view content!" } }} />
          }}>
          </Route>

          <Route path="/register">
            <Register />
          </Route>

          <Route path="/login" render={(props) => <Login {...props} /> }>
          </Route>

          {/* <Route path="/logout">
            <Logout />
          </Route> */}

          {/* Set default page: */}
          <Route exact path="/">
            <Redirect to="/dashboard" />
          </Route>
        </Switch>
      </div>
    )
  }
}

export default App;
