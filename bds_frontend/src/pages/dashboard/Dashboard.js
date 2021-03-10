import { Component, Fragment } from 'react';

// reactstrap
import { Card, CardBody, } from 'reactstrap';

// import components:
import WebNavbar from './../../components/layout/WebNavbar';
// font awesome
import './../../../node_modules/@fortawesome/fontawesome-free/css/all.css';

import { Link } from "react-router-dom";

// axios
import axios from 'axios';

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
    }

    this.handleCount = this.handleCount.bind(this);
  }

  componentDidMount() {
    this.handleCount();
  }

  handleCount = () => {
    let self = this
    axios
      .get("/bds/count/")
      .then(function(res) {
        console.log(res);
        self.setState({
          all: res.data.all,
          lands: res.data.lands,
          houses: res.data.houses,
          departments: res.data.departments,
          others: res.data.others,
          belong_to_projects: res.data.belong_to_projects,
          has_policy: res.data.has_policy,
          new_updates: res.data.new_updates,
          has_furniture: res.data.has_furniture,
        })
      })
      .catch(function(err){
        console.log(err);
      })
  }

  render() {
    return(
      <Fragment>
        <WebNavbar name="Crawling Website" />
        
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
                              {this.state.all}
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
                              {this.state.lands}
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
                              {this.state.houses}
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
                              {this.state.departments}
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
                              {this.state.others}
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
              <p className="font-weight-bold h4">Details</p>
              <div className="row">
                <div className="col-6 col-md-6">
                  <Card>
                    <CardBody>
                      <div className="mail-list mt-3">
                        <Link to="#">
                          <span className="mdi mdi-arrow-right-drop-circle text-success float-right mt-1  ml-2">{this.state.belong_to_projects}</span>
                          Belong to projects
                        </Link>
                        
                        <Link to="#">
                          <span className="mdi mdi-arrow-right-drop-circle text-primary float-right mt-1 ml-2">{this.state.has_policy}</span>
                          Has policy
                        </Link>
                        
                        <Link to="#">
                          <span className="mdi mdi-arrow-right-drop-circle text-info float-right mt-1 ml-2">{this.state.new_updates}</span>
                          New updates
                        </Link>
                        
                        <Link to="#">
                          <span className="mdi mdi-arrow-right-drop-circle text-warning float-right mt-1 ml-2">{this.state.has_furniture}</span>
                          Has furniture
                        </Link>
                        
                        {/* <Link to="#">
                          <span className="mdi mdi-arrow-right-drop-circle text-danger float-right mt-1  ml-2">0</span>
                          Nhà đất 247
                        </Link> */}
                      </div>
                    </CardBody>
                  </Card>
                </div>

                {/* <div className="col-6 col-md-6">
                  <Card>
                    <CardBody>
                      <div className="mail-list mt-3">
                        <Link to="#">
                          <span className="mdi mdi-arrow-right-drop-circle text-success float-right mt-1  ml-2">0</span>
                          Propzy
                        </Link>
                        
                        <Link to="#">
                          <span className="mdi mdi-arrow-right-drop-circle text-primary float-right mt-1 ml-2">0</span>
                          Bất động sản
                        </Link>
                        
                        <Link to="#">
                          <span className="mdi mdi-arrow-right-drop-circle text-info float-right mt-1 ml-2">0</span>
                          Chợ tốt
                        </Link>
                        
                        <Link to="#">
                          <span className="mdi mdi-arrow-right-drop-circle text-warning float-right mt-1 ml-2">0</span>
                          Homedy
                        </Link>
                        
                        <Link to="#">
                          <span className="mdi mdi-arrow-right-drop-circle text-danger float-right mt-1  ml-2">0</span>
                          Nhà đất 247
                        </Link>
                      </div>
                    </CardBody>
                  </Card>
                </div> */}
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