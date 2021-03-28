import { Component, Fragment } from 'react';
import { Redirect, Link } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'js-cookie';

// Import Components:
import WebNavbar from './../../components/layout/WebNavbar';
// import Dashboard from './../dashboard/Dashboard';

// CSS:
import './styles.css';

class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: '',
      password: '',
      message: null,
    }

    this.handleChange = this.handleChange.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  componentDidMount() {
    if (this.props.location.state !== undefined) {
      console.log(this.props.location.state.message);
      this.setState({ message: this.props.location.state.message })
    }
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

  handleSubmit = (e) => {
    e.preventDefault();
    let self = this
    axios
      .post('/bds/login/', {
        username: this.state.username,
        password: this.state.password
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
      <Fragment>
        <WebNavbar name="Login" current_user="" />
        <div className="text-center login-contents">
          {/* <p className="h4 font-weight-bold">This is login page!</p> */}
          <p className="font-weight-bold">{this.state.message}</p>
        </div>

        <div className="row mt-5 px-0">

          <div className="col-3 col-md-4 px-0"></div>
          <form className="col-6 col-md-4 bg-light p-3" onSubmit={this.handleSubmit}>
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
                <input 
                type="password"
                name="password"
                value={this.state.password}
                onChange={this.handleChange}
                className="form-control" 
                placeholder="Enter password" />
            </div>

            <div className="form-group">
                <div className="custom-control custom-checkbox">
                    <input type="checkbox" className="custom-control-input" id="customCheck1" />
                    <label className="custom-control-label" htmlFor="customCheck1">Remember me</label>
                </div>
            </div>

            <button type="submit" className="btn btn-primary btn-block">Submit</button>
            <div className="row justify-content-between">
              <div className="col-6">
                <span className="forgot-password">
                    Don't have account? Register 
                    <Link to="/register"> here</Link>
                </span>
              </div>
              <div className="col-4">
                <span className="forgot-password">
                    Forgot <a href="/">password?</a>
                </span>
              </div>
            </div>
          </form>
          <div className="col-3 col-md-4"></div>
        </div>
      </Fragment>
    )
  }
}

export default Login;