import { Component, Fragment } from 'react';
import { Redirect, Link } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'js-cookie';

// @material-ui
import { FormControlLabel, Checkbox } from '@material-ui/core';

// Import Components:
import WebNavbar from './../../components/layout/WebNavbar';

// CSS:
import './styles.css';

export default class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: '',
      password: '',
      rememberMe: false,
      message: null,
      passType: "password",
      passIcon: "fa fa-lg fa-eye",
    }

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChangeCheckbox = this.handleChangeCheckbox.bind(this);
    this.handleShowPassBtn = this.handleShowPassBtn.bind(this);
  }

  componentDidMount() {
    if (this.props.location.state !== undefined) {
      console.log(this.props.location.state.message);
      this.setState({ message: this.props.location.state.message })
    }

    // Handle value from localStorage:
    const rememberMe = localStorage.getItem('rememberMe') === 'true';
    const username = rememberMe ? localStorage.getItem('username') : '';
    const password = rememberMe ? localStorage.getItem('password') : '';

    this.setState({ username, password, rememberMe })
  }

  handleChange = (e) => {
    const name = e.target.name;
    const value = e.target.value;
    // console.log(name, value)
    this.setState(
      {
        [name]: value
      }
    )
  }

  handleChangeCheckbox = (e) => {
    const name = e.target.name;
    const checked = e.target.checked;
    this.setState({ [name]: checked })
  }

  handleShowPassBtn = () => {
    if (this.state.passType === "password") {
      this.setState({ passType: "text", passIcon: "fa fa-lg fa-eye-slash" })
    }
    else {
      this.setState({ passType: "password", passIcon: "fa fa-lg fa-eye" })
    }
  }

  handleSubmit = (e) => {
    e.preventDefault();
    
    // Handle remember me function:
    const { username, password, rememberMe } = this.state;
    localStorage.setItem('username', rememberMe ? username : '');
    localStorage.setItem('password', rememberMe ? password : '');
    localStorage.setItem('rememberMe', rememberMe);

    let self = this
    axios
      .post('/bds/login/', {
        username: self.state.username,
        password: self.state.password
      }, 
      {
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
        }
      }
      )
      .then(function(res) {
        console.log(res);
        self.setState(
          {
            message: 'Successful!'
          }
        )
        
      })
      .catch(function(err) {
        console.log(err);
        self.setState(
          {
            message: 'Your username or password is not correct! Try again!'
          }
        )
      })
  }

  render() {
    if (this.state.message === "Successful!") {
      return <Redirect to={{ pathname: "/dashboard", state: { isAuthenticated: true } }} />
    }

    return(
      <div className="container-fluid">
        <Fragment>
          <WebNavbar name="Login" />

          <div className="text-center login-contents">
            <p className="font-weight-bold text-danger">{this.state.message}</p>
          </div>

          <div className="row mt-1 px-0">

            <div className="col-2 col-md-4 px-0"></div>
            <form className="col-8 col-md-4 bg-light p-3" onSubmit={this.handleSubmit}>
              <h3>Login</h3>

              <div className="form-group">
                  <label>Username</label>
                  <input 
                    type="text"
                    name="username"
                    value={this.state.username}
                    onChange={this.handleChange}
                    className="form-control" 
                    placeholder="Enter username" />
              </div>

              <div className="form-group">
                  <label>Password</label>
                  <div className="d-flex">
                    <input 
                      type={this.state.passType}
                      name="password"
                      value={this.state.password}
                      onChange={this.handleChange}
                      className="form-control" 
                      placeholder="Enter password" 
                    />
                    <button type="button" className="ml-1 btn btn-link" aria-label="Toggle Visibility" onClick={this.handleShowPassBtn} >
                        <i aria-hidden="true" className={this.state.passIcon}></i>
                    </button>
                  </div>
              </div>

              <div className="form-group">
                {/* <input
                  id="rememberMe-checkbox"
                  type="checkbox" 
                  name="rememberMe"
                  checked={this.state.rememberMe} 
                  onClick={this.handleChangeCheckbox} 
                /> */}
                
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={this.state.rememberMe}
                      onChange={this.handleChangeCheckbox}
                      name="rememberMe"
                      color="primary"
                    />
                  }
                  label="Remember me"
                />
              </div>

              <div className="text-center">
                <button type="submit" className="btn col-6 col-md-2" id="login-btn">Login</button>
              </div>

              <div className="row justify-content-between">
                <div className="col-6 col-md-6">
                  <span className="forgot-password">
                      Don't have account? Register 
                      <Link to="/register"> here</Link>
                  </span>
                </div>
                <div className="col-4 col-md-3">
                  <span className="forgot-password">
                      Forgot <a href="/">password?</a>
                  </span>
                </div>
              </div>
            </form>
            <div className="col-2 col-md-4"></div>
          </div>
        </Fragment>
      </div>
    )
  }
}