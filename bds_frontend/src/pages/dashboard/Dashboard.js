import { Component, Fragment } from 'react';

// reactstrap
import { Card, CardBody, FormGroup, Label, Button, } from 'reactstrap';

// datepicker:
import DayPickerInput from 'react-day-picker/DayPickerInput';
import 'react-day-picker/lib/style.css';
// moment js:
import 'moment/locale/vi';

import MomentLocaleUtils, { formatDate, parseDate, } from 'react-day-picker/moment';

// font awesome
import './../../../node_modules/@fortawesome/fontawesome-free/css/all.css';

import { Link } from "react-router-dom";

// axios
import axios from 'axios';
// cookie
import Cookies from 'js-cookie';

// multiple select
// import Select from 'react-select';

// import components:
import WebNavbar from './../../components/layout/WebNavbar';
import WebChart from '../../components/charts/WebChart';

// CSS:
import './styles.css'

class Dashboard extends Component {

  constructor(props) {
    super(props);
    this.state = {
      count: {
        all: 0,
        lands: 0,
        houses: 0,
        departments: 0,
        others: 0,
        belong_to_projects: 0,
        has_policy: 0,
        new_updates: 0,
        has_furniture: 0,
      },
      chart: null,
      startDate: new Date().toLocaleDateString(),
      endDate: new Date().toLocaleDateString(),
    }

    this.handleCount = this.handleCount.bind(this);
    this.handleStartDate = this.handleStartDate.bind(this);
    this.handleEndDate = this.handleEndDate.bind(this);
    this.submitFilter = this.submitFilter.bind(this);
  }

  componentDidMount() {
    this.handleCount();
  }

  handleCount = () => {
    let self = this
    axios
      .get("/bds/api/realestatedata/count/")
      .then(function(res) {
        // console.log(res);
        self.setState({
          count: {
            all: res.data.all,
            lands: res.data.lands,
            houses: res.data.houses,
            departments: res.data.departments,
            others: res.data.others,
            belong_to_projects: res.data.belong_to_projects,
            has_policy: res.data.has_policy,
            new_updates: res.data.new_updates,
            has_furniture: res.data.has_furniture
          },
          chart: <WebChart className="mx-2" categories={['All', 'Lands', 'Houses', 'Departments', 'Others']} series={[ { name: '', data: [res.data.all, res.data.lands, res.data.houses, res.data.departments, res.data.others]} ]} />
        })
      })
      .catch(function(err){
        // console.log(err);
      })
  }

  handleStartDate = (date) => {
    this.setState({ startDate: date.toLocaleDateString()})
    console.log(this.state.startDate);
  }

  handleEndDate = (date) => {
    this.setState({ endDate: date.toLocaleDateString()})
  }

  submitFilter = (e) => {
    // e.preventDefault();
    let self = this
    axios
      .post("/bds/api/realestatedata/count/", 
        {
          start_date: self.state.startDate,
          end_date: self.state.endDate
        },
        {
          headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
          }
        } 
      )
      .then(function(res) {
        console.log(res);
        self.setState({
          chart: <WebChart className="mx-2" categories={['All', 'Lands', 'Houses', 'Departments', 'Others']} series={[ { name: '', data: [res.data.all, res.data.lands, res.data.houses, res.data.departments, res.data.others]} ]} />
        })
      })
      .catch(function(err){
        console.log(err);
      })
  }

  render() {
    return(
      <Fragment>
        <WebNavbar name="Crawling WebApp" />
        
        <div className="container-fluid mt-5">
          <div className="row mt-5">
            <div className="col-1 col-md-1 bg-light"></div>
            <div className="col-10 col-md-10">
              <div className="row mt-5 justify-content-center">

                <div className="col-2 col-md-2 mx-2">
                  <Card className="text-white bg-dark">
                      <CardBody>
                          <blockquote className="card-blockquote mb-0">
                            <h1 className="text-center">
                              {this.state.count.all}
                              <i className="fas fa-arrow-up"></i>
                              {/* <i className="fas fa-arrow-down"></i> */}
                            </h1>
                            <br></br>
                            <h5 className="text-center">All</h5>
                          </blockquote>
                      </CardBody>
                  </Card>
                </div>

                <div className="col-2 col-md-2 mx-2">
                  <Card className="text-white bg-primary">
                      <CardBody>
                          <blockquote className="card-blockquote mb-0">
                            <h1 className="text-center">
                              {this.state.count.lands}
                              <i className="fas fa-arrow-up"></i>
                              {/* <i className="fas fa-arrow-down"></i> */}
                            </h1>
                            <br></br>
                            <h5 className="text-center">Lands</h5>
                          </blockquote>
                      </CardBody>
                  </Card>
                </div>

                <div className="col-2 col-md-2 mx-2">
                  <Card className="text-white bg-danger">
                      <CardBody>
                          <blockquote className="card-blockquote mb-0">
                            <h1 className="text-center">
                              {this.state.count.houses}
                              <i className="fas fa-arrow-up"></i>
                              {/* <i className="fas fa-arrow-down"></i> */}
                            </h1>
                            <br></br>
                            <h5 className="text-center">Houses</h5>
                          </blockquote>
                      </CardBody>
                  </Card>
                </div>

                <div className="col-2 col-md-2 mx-2">
                  <Card className="text-white bg-warning">
                      <CardBody>
                          <blockquote className="card-blockquote mb-0">
                            <h1 className="text-center">
                              {this.state.count.departments}
                              <i className="fas fa-arrow-up"></i>
                              {/* <i className="fas fa-arrow-down"></i> */}
                            </h1>
                            <br></br>
                            <h5 className="text-center">Departments</h5>
                          </blockquote>
                      </CardBody>
                  </Card>
                </div>

                <div className="col-2 col-md-2 mx-2">
                  <Card className="text-white bg-info">
                      <CardBody>
                          <blockquote className="card-blockquote mb-0">
                            <h1 className="text-center">
                              {this.state.count.others}
                              <i className="fas fa-arrow-up"></i>
                              {/* <i className="fas fa-arrow-down"></i> */}
                            </h1>
                            <br></br>
                            <h5 className="text-center">Others</h5>
                          </blockquote>
                      </CardBody>
                  </Card>
                </div>
              </div>

              <br/>
              <div className="row">
                <div className="col-7 col-md-7"></div>
                <div className="col-2 col-md-2 float-right">
                  <FormGroup>
                    <Label className="control-label">From Date</Label>
                    <br/>
                    <DayPickerInput
                      formatDate={formatDate}
                      parseDate={parseDate}
                      format="L"
                      placeholder={`${formatDate(this.state.startDate, 'L', 'en')}`}
                      dayPickerProps={{
                        locale: 'en',
                        localeUtils: MomentLocaleUtils,
                      }} 
                      onDayChange={day => this.handleStartDate(day)} 
                    />
                  </FormGroup>
                </div>

                <div className="col-2 col-md-2 float-right">
                  <FormGroup>
                    <Label className="control-label">To Date</Label>
                    <br/>
                    <DayPickerInput
                      formatDate={formatDate}
                      parseDate={parseDate}
                      format="L"
                      placeholder={`${formatDate(this.state.endDate, 'L', 'en')}`}
                      dayPickerProps={{
                        locale: 'en',
                        localeUtils: MomentLocaleUtils,
                      }} 
                      onDayChange={day => this.handleEndDate(day)} 
                    />
                  </FormGroup>
                </div>

                <div className="col-1 col-md-1">
                  <Button className="text-center mt-3 web-btn" onClick={this.submitFilter}>Filter</Button>
                </div>

              </div>

              <hr/>
              <div className="my-3">
                {this.state.chart}
              </div>

              <br/>
              <p className="font-weight-bold h4">Details</p>
              <div className="row mt-2 mb-4">
                <div className="col-6 col-md-6">
                  <Card>
                    <CardBody>
                      <div className="mail-list mt-3">
                        <Link to="#">
                          <span className="mdi mdi-arrow-right-drop-circle text-success float-right mt-1  ml-2">{this.state.count.belong_to_projects}</span>
                          Belong to projects
                        </Link>
                        
                        <Link to="#">
                          <span className="mdi mdi-arrow-right-drop-circle text-primary float-right mt-1 ml-2">{this.state.count.has_policy}</span>
                          Has policy
                        </Link>
                      </div>
                    </CardBody>
                  </Card>
                </div>

                <div className="col-6 col-md-6">
                  <Card>
                    <CardBody>
                      <div className="mail-list mt-3">
                        <Link to="#">
                            <span className="mdi mdi-arrow-right-drop-circle text-info float-right mt-1 ml-2">{this.state.count.new_updates}</span>
                            New updates
                        </Link>
                        
                        <Link to="#">
                          <span className="mdi mdi-arrow-right-drop-circle text-warning float-right mt-1 ml-2">{this.state.count.has_furniture}</span>
                          Has furniture
                        </Link>
                      </div>
                    </CardBody>
                  </Card>
                </div>
              </div>
            </div>
            <div className="col-1 col-md-1 bg-light"></div>
          </div>
        </div>
      </Fragment>
    )
  }
}

export default Dashboard;