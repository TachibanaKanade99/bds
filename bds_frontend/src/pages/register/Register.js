import { Component, Fragment } from 'react';

// CSS:
import './styles.css';

class Register extends Component {
  constructor(props) {
    super(props);
    this.state = {
      value: '',
    }
  }

  render() {
    return(
      <Fragment>
        <div className="text-center h4 font-weight-bold mt-5">
          <p>This is register page!</p>
        </div>

        <div className="row mt-5">
          <div className="col-4 col-md-4"></div>
          <form className="col-4 col-md-4 bg-light p-3">
            <h3>Login</h3>

            <div className="form-group">
              <label>First name</label>
              <input type="text" className="form-control" placeholder="First name" />
            </div>

            <div className="form-group">
              <label>Last name</label>
              <input type="text" className="form-control" placeholder="Last name" />
            </div>

            <div className="form-group">
              <label>Email address</label>
              <input type="email" className="form-control" placeholder="Enter email" />
            </div>

            <div className="form-group">
              <label>Password</label>
              <input type="password" className="form-control" placeholder="Enter password" />
            </div>

            <button type="submit" className="btn btn-primary btn-block">Sign Up</button>
            <p className="forgot-password text-right">
              Already registered <a href="/">sign in?</a>
            </p>
          </form>
          <div className="col-4 col-md-4"></div>
        </div>
      </Fragment>
    )
  }
}

export default Register;