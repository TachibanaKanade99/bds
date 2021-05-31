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
import PricePrediction from './pages/price_prediction/PricePrediction';
import AdminPage from './pages/admin_page/AdminPage';

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
      isSuperUser: false,
    }

    this.checkAuthentication = this.checkAuthentication.bind(this);
    this.getCurrentUser = this.getCurrentUser.bind(this);
  }

  componentDidMount() {
    this.checkAuthentication();
    this.getCurrentUser();
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

  getCurrentUser = () => {
    let self = this;
    axios
      .get("/bds/current_user/")
      .then((res) => {
        self.setState({ isSuperUser: res.data.is_superuser })
      })
      .catch((err) => {
        console.log(err);
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

          <Route path="/price_prediction" render={(props) => {
            let auth = this.state.isAuthenticated;
            if (props.location.state !== null && props.location.state !== undefined) {
              auth = props.location.state.isAuthenticated;
            }
            return auth === true ? <PricePrediction {...props} /> : <Redirect to={{ pathname: '/login', state: { message: "You need to login to use this service!" } }} />
          }}>
          </Route>

          <Route path="/admin_page" render={(props) => {
            let auth = this.state.isAuthenticated;
            let isAdmin = this.state.isSuperUser;

            if (props.location.state !== null && props.location.state !== undefined) {
              auth = props.location.state.isAuthenticated;
              isAdmin = props.location.state.isSuperUser;
            }

            if (auth === true) {
              if (isAdmin === true) {
                return <AdminPage {...props} />
              }
              else {
                return <Redirect to={{ pathname: '/dashboard', state: { isAuthenticated: true, message: "You need to be an admin to access this service!" } }} />
              }
            }
            else{
              return <Redirect to={{ pathname: '/login', state: { message: "You need to login to use this service!" } }} />
            }

            // return (auth && isAdmin) === true ? <AdminPage {...props} /> : <Redirect to={{ pathname: '/login', state: { message: "You need to be an admin to access this service!" } }} />
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
