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
      current_user: null,
      is_superuser: null,
    }
    this.getCurrentUser = this.getCurrentUser.bind(this);
  }

  componentDidMount() {
    this.getCurrentUser();
  }

  getCurrentUser = () => {
    let self = this;
    axios
      .get("/bds/api/current_user/")
      .then((res) => {
        // console.log(res);
        self.setState({ 
          current_user: res.data.username,
          is_superuser: res.data.is_superuser
        })
      })
      .catch((err) => {
        console.log(err);
      })
  }

  render() {
    return (

      <Fragment>
        <WebNavbar name="Admin Page" current_user={this.state.current_user} is_superuser={this.state.is_superuser} />

        <Route 
          path="/:users"
          render={( { match } ) => {
            // Do something
            console.log("Here is users");
            if (this.props.location.pathname === "/admin_page/:users") {
              if (this.props.location.state !== undefined) {
                if (this.props.location.state.isAuthenticated) {
                  if (this.props.location.state.isSuperUser) {
                    return <Users />
                  }
                  else {
                    <Redirect to={{ pathname: '/dashboard', state: { isAuthenticated: true, isSuperUser: false, message: "You need to be an admin to access this service!" } }} />
                  }
                }
                else {
                  <Redirect to={{ pathname: '/login', state: { message: "You need to login to use this service!" } }} />
                }
              }
              else {
                if (this.state.current_user !== null && this.state.is_superuser !== null) {
                  if (this.state.current_user) {
                    if (this.state.is_superuser) {
                      return <Users />
                    }
                    else {
                      <Redirect to={{ pathname: '/dashboard', state: { isAuthenticated: true, isSuperUser: false, message: "You need to be an admin to access this service!" } }} />
                    }
                  }
                  else {
                    <Redirect to={{ pathname: '/login', state: { message: "You need to login to use this service!" } }} />
                  }
                }
                else {
                  return null;
                }
              }
            }
          }}
        />

        <Route 
          path="/admin_page/:models"
          render={( { match } ) => {
            // Do something
            console.log("Here is models");
            if (this.props.location.pathname === "/admin_page/:models") {
              console.log("Here");
              if (this.props.location.state !== undefined) {
                if (this.props.location.state.isAuthenticated) {
                  if (this.props.location.state.isSuperUser) {
                    return <Models />
                  }
                  else {
                    <Redirect to={{ pathname: '/dashboard', state: { isAuthenticated: true, isSuperUser: false, message: "You need to be an admin to access this service!" } }} />
                  }
                }
                else {
                  <Redirect to={{ pathname: '/login', state: { message: "You need to login to use this service!" } }} />
                }
              }
              else {
                if (this.state.current_user !== null && this.state.is_superuser !== null) {
                  if (this.state.current_user) {
                    if (this.state.is_superuser) {
                      return <Models />
                    }
                    else {
                      <Redirect to={{ pathname: '/dashboard', state: { isAuthenticated: true, isSuperUser: false, message: "You need to be an admin to access this service!" } }} />
                    }
                  }
                  else {
                    <Redirect to={{ pathname: '/login', state: { message: "You need to login to use this service!" } }} />
                  }
                }
                else {
                  return null;
                }
              }
            }
          }}
        />

      </Fragment>
    )
  }
}