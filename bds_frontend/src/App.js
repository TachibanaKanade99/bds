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
      isAuthenticated: null,
      username: null,
      isSuperUser: null,
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
      .get("/bds/api/check_authentication/", {
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
        }
      })
      .then(function(res) {
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
      .get("/bds/api/current_user/")
      .then((res) => {
        self.setState({
          username: res.data.username,
          isSuperUser: res.data.is_superuser 
        })
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
            // let auth = this.state.isAuthenticated;
            if (props.location.state) {
              // auth = props.location.state.isAuthenticated;
              return props.location.state.isAuthenticated === true ? <Dashboard {...props} /> : <Redirect to={{ pathname: '/login', state: { message: "You need to login to view content" } }} />
            }

            if (this.state.isAuthenticated !== null) {
              return this.state.isAuthenticated === true ? <Dashboard {...props} /> : <Redirect to={{ pathname: '/login', state: { message: "You need to login to view content!" } }} />
            }
            else{
              return null;
            }
          }}>
          </Route>

          <Route path="/data" render={(props) => {
            // let auth = this.state.isAuthenticated;
            if (props.location.state) {
              // auth = props.location.state.isAuthenticated;
              return props.location.state.isAuthenticated === true ? <Data {...props} /> : <Redirect to={{ pathname: '/login', state: { message: "You need to login to view content" } }} />
            }
            
            if (this.state.isAuthenticated !== null) {
              return this.state.isAuthenticated === true ? <Data {...props} /> : <Redirect to={{ pathname: '/login', state: { message: "You need to login to view content!" } }} />
            }
            else {
              return null;
            }
          }}>
          </Route>

          <Route path="/price_prediction" render={(props) => {
            // let auth = this.state.isAuthenticated;
            if (props.location.state) {
              // auth = props.location.state.isAuthenticated;
              return props.location.state.isAuthenticated === true ? <PricePrediction {...props} /> : <Redirect to={{ pathname: '/login', state: { message: "You need to login to view content" } }} />
            }
            
            if (this.state.isAuthenticated !== null) {
              return this.state.isAuthenticated === true ? <PricePrediction {...props} /> : <Redirect to={{ pathname: '/login', state: { message: "You need to login to use this service!" } }} />
            }
            else {
              return null;
            }
          }}>
          </Route>

          <Route path="/admin_page" render={(props) => {
            // let auth = this.state.isAuthenticated;
            // let isSuperUser = this.state.isSuperUser;

            // if (props.location.state !== null && props.location.state !== undefined) {
            //   if (props.location.state.isAuthenticated !== null && props.location.state.isAuthenticated !== undefined){
            //     if (props.location.state.isAuthenticated === true) {
            //       if (props.location.state.isSuperUser !== null && props.location.state.isSuperUser !== undefined) {
            //         return props.location.state.isSuperUser === true ? <AdminPage {...props} /> : <Redirect to={{ pathname: '/dashboard', state: { isAuthenticated: true, isSuperUser: props.location.state.isSuperUser, message: "You need to be an admin to access this service!" } }} />
            //       }
            //     }
            //   }
            // }

            // if (props.location.state) {

            // }
            
            if (this.state.isAuthenticated !== null) {
              if (this.state.isAuthenticated === true) {
                if (this.state.isSuperUser) {
                  return <AdminPage {...props} />;
                }
                else if (this.state.isSuperUser === false) {
                  return <Redirect to={{ 
                    pathname: '/dashboard', 
                    state: { 
                      isAuthenticated: true, 
                      isSuperUser: this.state.isSuperUser, 
                      message: "You need to be an admin to access this service!" 
                    } 
                  }} />;
                }
                else {
                  return null;
                }
              }
              else {
                return <Redirect to={{ pathname: '/login', state: { message: "You need to login to use this service!" } }} />
              }
            }
            else {
              return null;
            }

            // if (auth === true) {
            //   if (isSuperUser === true) {
            //     return <AdminPage {...props} />
            //   }
            //   else {
            //     return <Redirect to={{ pathname: '/dashboard', state: { isAuthenticated: true, isSuperUser: isSuperUser, message: "You need to be an admin to access this service!" } }} />
            //   }
            // }
            // else{
            //   return <Redirect to={{ pathname: '/login', state: { message: "You need to login to use this service!" } }} />
            // }
          }}>
          </Route>

          <Route path="/register" render={(props) => <Register {...props} />}>
          </Route>

          <Route path="/login" render={(props) => <Login {...props} /> }>
          </Route>

          {/* <Route path="/logout">
            <Logout />
          </Route> */}

          {/* Set default route: */}
          <Route exact path="/">
            <Redirect to="/dashboard" />
          </Route>
        </Switch>
      </div>
    )
  }
}

export default App;
