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
      current_user: null,
      count: {
        all: 1,
        lands: 1,
        houses: 3,
        departments: 1,
        others: 1,
      },

      land_props: {
        only_lands: 1,
        land_in_projects: 1,
      },

      house_props: {
        villas: 1,
        town_houses: 1,
        individual_houses: 1,
      },

      bds: {
        all: 0,
        lands: 0,
        houses: 0,
        departments: 0,
        others: 0,
      },

      homedy: {
        all: 0,
        lands: 0,
        houses: 0,
        departments: 0,
        others: 0,
      },

      propzy: {
        all: 0,
        lands: 0,
        houses: 0,
        departments: 0,
        others: 0,
      },

      belong_to_projects: 0,
      has_policy: 0,
      new_updates: 0,
      has_furniture: 0,

      chart: null,
      lands_chart: null,
      
      startDateChart: new Date(2020, 7, 31).toLocaleDateString(),
      endDateChart: new Date().toLocaleDateString(),

      startDatePieChart: new Date(2020, 7, 31).toLocaleDateString(),
      endDatePieChart: new Date().toLocaleDateString(),
    }

    this.getCurrentUser = this.getCurrentUser.bind(this);

    // handle date filter chart:
    this.handleStartDateChart = this.handleStartDateChart.bind(this);
    this.handleEndDateChart = this.handleEndDateChart.bind(this);

    // handle date filter pie chart:
    this.handleStartDatePieChart = this.handleStartDatePieChart.bind(this);
    this.handleEndDatePieChart = this.handleEndDatePieChart.bind(this);

    this.handleCount = this.handleCount.bind(this);
    this.handleChart = this.handleChart.bind(this);
    this.handlePieChart = this.handlePieChart.bind(this);

    this.filterChart = this.filterChart.bind(this);
    this.filterPieChart = this.filterPieChart.bind(this);
  }

  componentDidMount() {
    this.getCurrentUser();
    this.handleCount();
    this.handleChart();
    this.handlePieChart();
  }

  handleStartDateChart = (date) => {
    this.setState({ startDateChart: date.toLocaleDateString() })
  }

  handleEndDateChart = (date) => {
    this.setState({ endDateChart: date.toLocaleDateString() })
  }

  handleStartDatePieChart = (date) => {
    this.setState({ startDatePieChart: date.toLocaleDateString() })
  }

  handleEndDatePieChart = (date) => {
    this.setState({ endDatePieChart: date.toLocaleDateString() })
  }

  getCurrentUser = () => {
    let self = this;
    axios
      .get("/bds/current_user/")
      .then((res) => {
        // console.log(res);
        self.setState({ current_user: res.data.username })
      })
      .catch((err) => {
        // console.log(err);
      })
  }

  handleCount = () => {
    let self = this
    axios
      .get("/bds/api/realestatedata/count/")
      .then((res) => {
        // console.log(res);
        self.setState({
          count: {
            all: res.data.all,
            lands: res.data.lands,
            houses: res.data.houses,
            departments: res.data.departments,
            others: res.data.others,
          },

          belong_to_projects: res.data.belong_to_projects,
          has_policy: res.data.has_policy,
          new_updates: res.data.new_updates,
          has_furniture: res.data.has_furniture,
        })
      })
      .catch((err) => {
        // console.log(err);
      })
  }

  handleChart = () => {
    let self = this;
    axios
      .get("/bds/api/realestatedata/chart_count/")
      .then((res) => {
        // console.log(res);
        self.setState({
          bds: {
            all: res.data.bds_all,
            lands: res.data.bds_lands,
            houses: res.data.bds_houses,
            departments: res.data.bds_departments,
            others: res.data.bds_others
          },
          homedy: {
            all: res.data.homedy_all,
            lands: res.data.homedy_lands,
            houses: res.data.homedy_houses,
            departments: res.data.homedy_departments,
            others: res.data.homedy_others
          },
          propzy: {
            all: res.data.propzy_all,
            lands: res.data.propzy_lands,
            houses: res.data.propzy_houses,
            departments: res.data.propzy_departments,
            others: res.data.propzy_others
          }
        })
      })
      .catch((err) => {
        // console.log(err);
      })
  }

  filterChart = () => {
    let self = this;
    axios
      .post("/bds/api/realestatedata/chart_count/", 
        {
          start_date: self.state.startDateChart,
          end_date: self.state.endDateChart
        },
        {
          headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
          }
        }
      )
      .then((res) => {
        // console.log(res);
        self.setState({
          bds: {
            all: res.data.bds_all,
            lands: res.data.bds_lands,
            houses: res.data.bds_houses,
            departments: res.data.bds_departments,
            others: res.data.bds_others
          },
          homedy: {
            all: res.data.homedy_all,
            lands: res.data.homedy_lands,
            houses: res.data.homedy_houses,
            departments: res.data.homedy_departments,
            others: res.data.homedy_others
          },
          propzy: {
            all: res.data.propzy_all,
            lands: res.data.propzy_lands,
            houses: res.data.propzy_houses,
            departments: res.data.propzy_departments,
            others: res.data.propzy_others
          }
        })
      })
      .catch((err) => {
        console.log(err);
      })
      
  }

  handlePieChart = () => {
    let self = this;
    axios
      .get("/bds/api/realestatedata/piechart_count/")
      .then((res) => {
        // console.log(res);
        self.setState({ 
          land_props: {
            only_lands: res.data.only_lands,
            land_in_projects: res.data.land_in_projects
          },
          house_props: {
            villas: res.data.villas,
            town_houses: res.data.town_houses,
            individual_houses: res.data.individual_houses
          }
        })
      })
      .catch((err) => {
        console.log(err);
      })

  }

  filterPieChart = (e) => {
    // e.preventDefault();
    let self = this;
    axios
      .post("/bds/api/realestatedata/piechart_count/", 
        {
          start_date: self.state.startDatePieChart,
          end_date: self.state.endDatePieChart
        },
        {
          headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
          }
        }
      )
      .then((res) => {
        // console.log(res);
        self.setState({
          land_props: {
            only_lands: res.data.only_lands,
            land_in_projects: res.data.land_in_projects
          },
          house_props: {
            villas: res.data.villas,
            town_houses: res.data.town_houses,
            individual_houses: res.data.individual_houses
          }
        })
      })
      .catch(function(err){
        // console.log(err);
      })
  }

  render() {
    return(
      <Fragment>
        <WebNavbar name="Crawling WebApp" current_user={this.state.current_user} />
        
        <div className="container-fluid mt-5">
          <div className="row mt-5">
            <div className="col-0 col-md-1 bg-light"></div>
            <div className="col-12 col-md-10">
              <div className="row mt-5 justify-content-center">

                <div className="col-10 col-md-2 mx-2 my-2">
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

                <div className="col-10 col-md-2 mx-2 my-2">
                  <Card className="text-white bg-violet">
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

                <div className="col-10 col-md-2 mx-2 my-2">
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

                <div className="col-10 col-md-2 mx-2 my-2">
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

                <div className="col-10 col-md-2 mx-2 my-2">
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
                <div className="col-12 col-md-7"></div>
                <div className="col-11 col-md-2">
                  <FormGroup>
                    <Label className="control-label dashboard-text">From Date</Label>
                    <br/>
                    <DayPickerInput
                      className="col-4"
                      formatDate={formatDate}
                      parseDate={parseDate}
                      format="L"
                      placeholder={`${formatDate(this.state.startDateChart, 'L', 'en')}`}
                      dayPickerProps={{
                        locale: 'en',
                        localeUtils: MomentLocaleUtils,
                      }} 
                      onDayChange={day => this.handleStartDateChart(day)} 
                    />
                  </FormGroup>
                </div>

                <div className="col-11 col-md-2 pr-0">
                  <FormGroup>
                    <Label className="control-label dashboard-text">To Date</Label>
                    <br/>
                    <DayPickerInput
                      formatDate={formatDate}
                      parseDate={parseDate}
                      format="L"
                      placeholder={`${formatDate(this.state.endDateChart, 'L', 'en')}`}
                      dayPickerProps={{
                        locale: 'en',
                        localeUtils: MomentLocaleUtils,
                      }} 
                      onDayChange={day => this.handleEndDateChart(day)} 
                    />
                  </FormGroup>
                </div>

                <div className="col-2 col-md-1 text-left pr-0">
                  <Button className="mt-3 web-btn" onClick={this.filterChart}>Filter</Button>
                </div>

              </div>

              <hr/>
              <div className="my-3 px-0">
                <WebChart 
                  className="mx-1"
                  type={"bar"}
                  width={"100%"} 
                  height={"450"}
                  labels={['All', 'Lands', 'Houses', 'Departments', 'Others']}
                  series={[
                    {
                      name: 'batdongsan.com.vn',
                      data: [this.state.bds.all, this.state.bds.lands, this.state.bds.houses, this.state.bds.departments, this.state.bds.others]
                    },
                    {
                      name: 'homedy.com',
                      data: [this.state.homedy.all, this.state.homedy.lands, this.state.homedy.houses, this.state.homedy.departments, this.state.homedy.others]
                    },
                    {
                      name: 'propzy.vn',
                      data: [this.state.propzy.all, this.state.propzy.lands, this.state.propzy.houses, this.state.propzy.departments, this.state.propzy.others]
                    }
                  ]}
                />
              </div>
              
              <hr/>
              <br/>

              <p className="font-weight-bold h4 dashboard-text">Details</p>
              
              <div className="row">
                <div className="col-12 col-md-7"></div>
                <div className="col-11 col-md-2">
                  <FormGroup>
                    <Label className="control-label dashboard-text">From Date</Label>
                    <br/>
                    <DayPickerInput
                      className="col-4"
                      formatDate={formatDate}
                      parseDate={parseDate}
                      format="L"
                      placeholder={`${formatDate(this.state.startDatePieChart, 'L', 'en')}`}
                      dayPickerProps={{
                        locale: 'en',
                        localeUtils: MomentLocaleUtils,
                      }} 
                      onDayChange={day => this.handleStartDatePieChart(day)} 
                    />
                  </FormGroup>
                </div>

                <div className="col-11 col-md-2 pr-0">
                  <FormGroup>
                    <Label className="control-label dashboard-text">To Date</Label>
                    <br/>
                    <DayPickerInput
                      formatDate={formatDate}
                      parseDate={parseDate}
                      format="L"
                      placeholder={`${formatDate(this.state.endDatePieChart, 'L', 'en')}`}
                      dayPickerProps={{
                        locale: 'en',
                        localeUtils: MomentLocaleUtils,
                      }} 
                      onDayChange={day => this.handleEndDatePieChart(day)} 
                    />
                  </FormGroup>
                </div>

                <div className="col-2 col-md-1 text-left pr-0">
                  <Button className="mt-3 web-btn" onClick={this.filterPieChart}>Filter</Button>
                </div>

              </div>

              <div className="row mt-2 mb-4">
                <div className="col-12 col-md-6 my-2">
                  <Card>
                    <CardBody>
                      <div className="mail-list mt-3">
                        <div className="font-weight-bold text-center dashboard-text">Lands</div>
                          <div className="pie-chart">
                            <WebChart  
                              type={"pie"} 
                              width={"100%"} 
                              height={"400"} 
                              labels={['Lands', 'Lands in Project']} 
                              series={
                                [
                                  this.state.land_props.only_lands / this.state.count.lands * 100, 
                                  this.state.land_props.land_in_projects / this.state.count.lands * 100
                                ]
                              } 
                            />
                          </div>
                      </div>
                    </CardBody>
                  </Card>
                </div>

                <div className="col-12 col-md-6 my-2">
                  <Card>
                    <CardBody>
                      <div className="mail-list mt-3">
                        <div className="font-weight-bold text-center dashboard-text">Houses</div>
                          <div className="pie-chart">
                            <WebChart 
                              className="mx-2" 
                              type={"pie"} 
                              width={"100%"} 
                              height={"400"} 
                              labels={['Villa', 'Town House', 'Individual House']} 
                              series={
                                [
                                  this.state.house_props.villas / this.state.count.houses * 100, 
                                  this.state.house_props.town_houses / this.state.count.houses * 100, 
                                  this.state.house_props.individual_houses / this.state.count.houses * 100
                                ]
                              } 
                            />
                          </div>
                      </div>
                    </CardBody>
                  </Card>
                </div>
              </div>

              <div className="row mt-3 mb-5">
                <div className="col-6 col-md-6">
                  <Card>
                    <CardBody>
                      <div className="mail-list mt-3">
                        <Link to="#" className="dashboard-text">
                            <span className="mdi mdi-arrow-right-drop-circle text-info float-right mt-1 ml-2">{this.state.belong_to_projects}</span>
                            Belong to projects
                        </Link>
                        
                        <Link to="#" className="dashboard-text">
                          <span className="mdi mdi-arrow-right-drop-circle text-warning float-right mt-1 ml-2">{this.state.has_policy}</span>
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
                        <Link to="#" className="dashboard-text">
                            <span className="mdi mdi-arrow-right-drop-circle text-info float-right mt-1 ml-2">{this.state.new_updates}</span>
                            New updates
                        </Link>
                        
                        <Link to="#" className="dashboard-text">
                          <span className="mdi mdi-arrow-right-drop-circle text-warning float-right mt-1 ml-2">{this.state.has_furniture}</span>
                          Has furniture
                        </Link>
                      </div>
                    </CardBody>
                  </Card>
                </div>
              </div>

            </div>
            <div className="col-0 col-md-1 bg-light"></div>
          </div>
        </div>
      </Fragment>
    )
  }
}

export default Dashboard;