import { Component, Fragment } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'js-cookie';

// Import Component:
import WebNavbar from './../../components/layout/WebNavbar';

// CSS:
import './styles.css';

class Register extends Component {
  constructor(props) {
    super(props);
    this.state = {
      // first_name: '',
      // last_name: '',
      // email: '',
      username: '',
      password: '',
      message: '',
    }
    
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
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
    // alert("Form submitted with " + this.state.firstName + " " + this.state.lastName);
    e.preventDefault();
    axios
      .post('/bds/register/', {
        // first_name: this.state.first_name,
        // last_name: this.state.last_name,
        // email: this.state.email,
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
      })
      .catch(function (error) {
        console.log(error);
      })
  }

  render() {
    return(
      <Fragment>
        <WebNavbar name="Register" />
        <div className="text-center register-contents">
          {/* <p className="h4 font-weight-bold">This is register page!</p> */}
          <p>{this.state.message}</p>
        </div>

        <div className="row mt-5">
          <div className="col-3 col-md-4"></div>
          <form className="col-6 col-md-4 bg-light p-3" onSubmit={this.handleSubmit}>
            <h3>Register</h3>

            {/* <div className="form-group">
              <label>First name</label>
              <input
                type="text"
                name="first_name"  
                value={this.state.first_name}
                onChange={this.handleChange}
                className="form-control" 
                placeholder="First name" 
              />
            </div>

            <div className="form-group">
              <label>Last name</label>
              <input 
                type="text" 
                name="last_name" 
                value={this.state.last_name}
                onChange={this.handleChange}
                className="form-control" 
                placeholder="Last name" 
              />
            </div> */}

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

            {/* <div className="form-group">
              <label>Email address</label>
              <input 
                type="email" 
                name="email"
                value={this.state.email}
                onChange={this.handleChange}
                className="form-control" 
                placeholder="Enter email" 
              />
            </div> */}

            <div className="form-group">
              <label>Password</label>
              <input 
                type="password" 
                name="password"
                value={this.state.password}
                onChange={this.handleChange}
                autocomplete="new-password"
                className="form-control" 
                placeholder="Enter password" 
              />
            </div>

            <div className="form-group">
              <label>Reenter Password</label>
              <input 
                type="password" 
                className="form-control" 
                placeholder="Reenter password" 
              />
            </div>

            <button 
              type="submit"
              className="btn btn-primary btn-block"
              defaultValue="Submit"
            >
              Sign Up
            </button>
            <p className="forgot-password text-right">
              Already registered 
              <Link exact to="/login"> sign in?</Link>
            </p>
          </form>
          <div className="col-3 col-md-4"></div>
        </div>
      </Fragment>
    )
  }
}

export default Register;