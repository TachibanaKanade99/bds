import { Component, Fragment } from 'react';

// import components:
import WebNavbar from './../../components/layout/WebNavbar';

class Dashboard extends Component {
  render() {
    return(
      <Fragment>
        <WebNavbar name="Crawling Website" />
        <div className="text-center h4 font-weight-bold">
          {/* <p>This is dashboard page!</p> */}
        </div>
      </Fragment>
    )
  }
}

export default Dashboard;