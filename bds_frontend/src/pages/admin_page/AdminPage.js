import { Fragment, Component } from 'react';
import axios from 'axios';

// React router dom:
import { Switch, Route, Redirect, } from "react-router-dom";

// import CSS:
import './styles.css'

// Local components:
import WebNavbar from '../../components/layout/WebNavbar';
import Users from './Users';
import Models from './Models';

export default class AdminPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      current_user: null
    }
    this.getCurrentUser = this.getCurrentUser.bind(this);
  }

  componentDidMount() {
    this.getCurrentUser();
  }

  getCurrentUser = () => {
    let self = this;
    axios
      .get("/bds/current_user/")
      .then((res) => {
        // console.log(res);
        self.setState({ current_user: res.data.username })
      })
      .catch((err) => {
        console.log(err);
      })
  }

  render() {
    return (

      <Fragment>
        <WebNavbar name="Admin Page" current_user={this.state.current_user} />

        <Route 
          path="/admin_page/:users"
          render={({ match }) => {
            // Do something
            if (this.props.location.pathname === "/admin_page/:users") {
              let isAuthenticated = this.props.location.state.isAuthenticated;
              let isSuperUser = this.props.location.state.isSuperUser;

              if (isAuthenticated) {
                if (isSuperUser) {
                  return <Users />
                }
                else {
                  <Redirect to={{ pathname: '/dashboard', state: { isAuthenticated: true, isSuperUser: isSuperUser, message: "You need to be an admin to access this service!" } }} />
                }
              }
              else {
                <Redirect to={{ pathname: '/login', state: { message: "You need to login to use this service!" } }} />
              }
            }
          }}
        />

        <Route 
          path="/admin_page/:models"
          render={({ match }) => {
            // Do something
            if (this.props.location.pathname === "/admin_page/:models") {
              let isAuthenticated = this.props.location.state.isAuthenticated;
              let isSuperUser = this.props.location.state.isSuperUser;

              if (isAuthenticated) {
                if (isSuperUser) {
                  return <Models />
                }
                else {
                  <Redirect to={{ pathname: '/dashboard', state: { isAuthenticated: true, isSuperUser: isSuperUser, message: "You need to be an admin to access this service!" } }} />
                }
              }
              else {
                <Redirect to={{ pathname: '/login', state: { message: "You need to login to use this service!" } }} />
              }
            }
          }}
        />

      </Fragment>
    )
  }
}