import { Component, Fragment } from 'react';
import { Redirect } from 'react-router-dom';
import Data from './../data/Data';
import axios from 'axios';

// CSS:
import './styles.css';

class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: '',
      password: '',
      message: '',
    }

    this.handleChange = this.handleChange.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
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
      .post('/login/', {
        username: this.state.username,
        password: this.state.password
      })
      .then(function(response) {
        console.log(response);
        self.setState(
          {
            message: 'successful'
          }
        )
      })
      .catch(function(error) {
        console.log(error);
        self.setState(
          {
            message: 'Your username or password is not correct! Try again!'
          }
        )
      })
  }

  render() {
    if (this.state.message === "successful") {
      return <Redirect exact to='/data/' component={<Data />} />   
    }

    return(
      <Fragment>
        <div className="text-center h4 font-weight-bold mt-5">
          <p>This is login page!</p>
        </div>

        <div className="row mt-5">
          <div className="col-4 col-md-4"></div>
          <form className="col-4 col-md-4 bg-light p-3" onSubmit={this.handleSubmit}>
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
            <p className="forgot-password text-right">
                Forgot <a href="/">password?</a>
            </p>
          </form>
          <div className="col-4 col-md-4"></div>
        </div>
        <div>{this.state.message}</div>
      </Fragment>
    )
  }
}

export default Login;