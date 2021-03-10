import { Fragment, Component } from 'react';
import axios from 'axios';

import WebNavbar from './../../components/layout/WebNavbar';
import { Redirect } from 'react-router-dom';
import Login from './../login/Login';
import Table from './Table';

// reactstrap
import { Button, ButtonGroup, FormGroup, Label, } from 'reactstrap';

// react-select:
import Select from "react-select";

// Import CSS:
import './styles.css';

class Data extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isLogged: null,
      data: '',
      isLoading: false,
      count: null,

      // select state:
      isMenuOpen: false,
      // filter:
      selectedWebsite: null,
    }

    this.isAuthorized = this.isAuthorized.bind(this);
    this.handleSelectMenuOpen = this.handleSelectMenuOpen.bind(this);
    this.handleWebsiteChange = this.handleWebsiteChange.bind(this);
    this.handleRowsPerPage = this.handleRowsPerPage.bind(this);
  }

  componentDidMount() {
    this.isAuthorized();
  }

  isAuthorized = () => {
    let self = this
    axios
      .get("/bds/api/realestatedata/")
      .then(function(res) {
        // console.log(res);
      })
      .catch(function(errors) {
          console.log(errors)
          self.setState({ isLogged: false })
      })
  }

  handleSelectMenuOpen = () => {
    this.setState({ isMenuOpen: !this.state.isMenuOpen })
  }

  handleWebsiteChange = () => {
    return null
  }

  handleRowsPerPage = () => {
    return null
  }

  render() {

    if (this.state.isLogged === false) {
      // return <Login message="You need to login before view contents!" />
      return <Redirect exact to="/login" component={<Login message="You need to login before view contents!" />} />
    }

    // Buttons state:
    const rowsPerPage = [
      { label: "10", value: 10 },
      { label: "20", value: 20 },
      { label: "50", value: 50 },
      { label: "100", value: 100 },
      { label: "150", value: 150 },
    ];

    const chooseWebPage = [
      { label: "--", value: "--" },
      { label: "https://batdongsan.com.vn/", value: "https://batdongsan.com.vn" },
      { label: "https://propzy.vn/", value: "https://propzy.vn/" },
      { label: "https://homedy.com/", value: "https://homedy.com/" }
    ];

    return (
      <Fragment>
        <WebNavbar name="Crawling Website" />
        
        <div className="container-fluid mt-5">
          <div className="row mt-5">
            <div className="col-1 col-md-1 bg-light"></div>
            <div className="col-10 col-md-10">
      
              <div className="row">
                <div className="col-3 col-md-3">
                  <FormGroup className="mt-3">
                      <Label className="control-label">Choose website</Label>
                      <Select
                        // className="customSelect"
                        options={chooseWebPage}
                        defaultValue={{ label: "--", value: "--" }}
                        onChange={this.handleWebsiteChange}
                        onMenuOpen={this.handleSelectMenuOpen}
                      />
                  </FormGroup>
                </div>
              </div>
              
              <div className="row">
                <div className="col-2 col-md-2">
                  <FormGroup>
                      <Label className="control-label">Choose Rows per Page</Label>
                      <Select
                        // className="customSelect"
                        options={rowsPerPage}
                        defaultValue={{ label: "10", value: 10 }}
                        onChange={this.handleRowsPerPage}
                      />
                  </FormGroup>
                </div>
              </div>

              <Table />
            </div>
            <div className="col-1 col-md-1 bg-light"></div>
          </div>
        </div>
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