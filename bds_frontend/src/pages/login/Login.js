import { Component, Fragment } from 'react';

// CSS:
import './styles.css';

class Login extends Component {
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
          <p>This is login page!</p>
        </div>

        <div className="row mt-5">
          <div className="col-4 col-md-4"></div>
          <form className="col-4 col-md-4 bg-light p-3">
            <h3>Login</h3>

            <div className="form-group">
                <label>Email address</label>
                <input type="email" className="form-control" placeholder="Enter email" />
            </div>

            <div className="form-group">
                <label>Password</label>
                <input type="password" className="form-control" placeholder="Enter password" />
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
      </Fragment>
    )
  }
}

export default Login;