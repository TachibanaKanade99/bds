import { Component, Fragment } from 'react';
import { Redirect, Link } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'js-cookie';

// Import Components:
import WebNavbar from './../../components/layout/WebNavbar';

// CSS:
import './styles.css';

export default class Register extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: '',
      password: '',
      message: null,
      passType: "password",
      passIcon: "fa fa-lg fa-eye"
    }
    
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleShowPassBtn = this.handleShowPassBtn.bind(this);
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
    let self = this
    axios
      .post('/bds/register/', {
        username: this.state.username,
        password: this.state.password
      }, 
      {
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
        }
      }
      )
      .then(function (response) {
        console.log(response);
        self.setState(
          {
            message: "Register Successful!"
          }
        )
      })
      .catch(function (error) {
        console.log(error);
        self.setState(
          {
            message: "Register Failed!"
          }
        )
      })
  }

  render() {

    if (this.state.message === "Register Successful!") {
      return <Redirect to={{ pathname: "/login" }} />
    }

    return(
      <Fragment>
        <WebNavbar name="Register" />

        <div className="text-center register-contents">
          <p>{this.state.message}</p>
        </div>

        <div className="row mt-1 px-0">

          <div className="col-2 col-md-4 px-0"></div>
          <form className="col-8 col-md-4 bg-light p-3" onSubmit={this.handleSubmit}>
            <h3>Register</h3>

            <div className="form-group">
              <label>Username</label>
              <input 
                type="text" 
                name="username"
                value={this.state.username}
                onChange={this.handleChange}
                autocomplete="new-password"
                className="form-control" 
                placeholder="Username" 
              />
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
              <label>Reenter Password</label>
              <div className="d-flex">
                <input 
                  type={this.state.passType}
                  className="form-control" 
                  placeholder="Reenter password" 
                />
                <button type="button" className="ml-1 btn btn-link" aria-label="Toggle Visibility" onClick={this.handleShowPassBtn} >
                  <i aria-hidden="true" className={this.state.passIcon}></i>
                </button>
              </div>
            </div>

            <button 
              type="submit"
              className="btn btn-primary btn-block"
              defaultValue="Submit"
            >
              Sign Up
            </button>
            <p className="forgot-password text-right">
              Already registered? 
              <Link exact to="/login"> Sign in</Link>
            </p>
          </form>
          <div className="col-3 col-md-4"></div>
        </div>
      </Fragment>
    )
  }
}