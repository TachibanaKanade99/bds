import { Fragment, Component } from 'react';
import axios from 'axios';

import WebNavbar from './../../components/layout/WebNavbar';
import { Redirect } from 'react-router-dom';
import Login from './../login/Login';
import Table from './Table';

class Data extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isLogged: null,
      data: '',
      isLoading: false,
      count: null,
    }
  }

  componentDidMount() {
    this.isAuthorized();
  }

  isAuthorized = () => {
    let self = this
    axios
      .get("/bds/api/bdss/")
      .then(function(res) {
        console.log(res);
      })
      .catch(function(errors) {
          console.log(errors)
          self.setState({ isLogged: false })
      })
  }

  render() {

    if (this.state.isLogged === false) {
      // return <Login message="You need to login before view contents!" />
      return <Redirect exact to="/login" component={<Login message="You need to login before view contents!" />} />
    }

    return (
      <Fragment>
        <WebNavbar />
        <div className="text-center mt-5">
          <p className="h4 font-weight-bold">This is data page</p>
        </div>
        <Table />
      </Fragment>
    )
  }
}

// function Data() {

//   return (
//     <Fragment>
//       <WebNavbar />
//       <div className="text-center h4 font-weight-bold">
//         <p>This is data page</p>
//       </div>
//       <Table />
//     </Fragment>
//   )
// }

export default Data; 