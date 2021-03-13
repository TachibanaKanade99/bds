import { Fragment, Component } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';

import WebNavbar from './../../components/layout/WebNavbar';
import { Redirect } from 'react-router-dom';
import Login from './../login/Login';

// MUI Datatable:
import { CircularProgress, Typography } from "@material-ui/core";
import { createMuiTheme, MuiThemeProvider } from '@material-ui/core/styles';
import MUIDataTable from "mui-datatables";
// import Table from './Table';

// reactstrap
import { FormGroup, Label, Button, } from 'reactstrap';

// react-select:
import Select from "react-select";

// Import CSS:
import './styles.css';

class Data extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isLogged: null,

      // Table state:
      count: 1,
      rowsPerPage: 10,
      sortOrder: {},
      columns: [
        {
          label: 'Url',
          name: 'url',
          options: {
            setCellProps: () => ({ style: { minWidth: "600px", maxWidth: "1600px" } })
          }
        },
        {
          label: 'Content',
          name: 'content',
          options: {
            setCellProps: () => ({ style: { minWidth: "600px", maxWidth: "1600px" } })
          }
        },
        {
          label: 'Price',
          name: 'price',
          options: {
            setCellProps: () => ({ style: { minWidth: "100px", maxWidth: "1000px" } })
          }
        },
        {
          label: 'Area',
          name: 'area',
          options: {
            setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
          }
        },
        {
          label: 'Location',
          name: 'location',
          options: {
            setCellProps: () => ({ style: { minWidth: "600px", maxWidth: "1600px" } })
          }
        },
        {
          label: 'Post Author',
          name: 'posted_author',
          options: {
            setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
          }
        },
        {
          label: 'Phone',
          name: 'phone',
          options: {
            setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
          }
        },
        {
          label: 'Posted Date',
          name: 'posted_date',
          options: {
            setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
          }
        },
        {
          label: 'Expired Date',
          name: 'expired_date',
          options: {
            setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
          }
        },
        {
          label: 'Item Code',
          name: 'item_code',
          options: {
            setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "200px" } })
          }
        },
        // {
        //     label: 'Images',
        //     name: 'image_urls',
        //     options: {
        //         setCellProps: () => ({ style: { minWidth: "800px", maxWidth: "800px" } })
        //     }
        // },
        {
          label: 'Post Type',
          name: 'post_type',
          options: {
            setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
          }
        },
        {
          label: 'Email',
          name: 'email',
          options: {
            setCellProps: () => ({ style: { minWidth: "200px", maxWidth: "200px" } })
          }
        },
        {
          label: 'Facade',
          name: 'facade',
          options: {
            setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
          }
        },
        {
          label: 'Entrance',
          name: 'entrance',
          options: {
            setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
          }
        },
        {
          label: 'Orientation',
          name: 'orientation',
          options: {
            setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
          }
        },
        {
          label: 'Balcony Orientation',
          name: 'balcony_orientation',
          options: {
            setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
          }
        },
        {
          label: 'Number of floors',
          name: 'number_of_floors',
          options: {
            setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
          }
        },
        {
          label: 'Number of bedrooms',
          name: 'number_of_bedrooms',
          options: {
            setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
          }
        },
        {
          label: 'Number of toilets',
          name: 'number_of_toilets',
          options: {
            setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
          }
        },
        // {
        //     label: 'Latitude',
        //     name: 'latitude',
        //     options: {
        //         setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
        //     }
        // },
        // {
        //     label: 'Longitude',
        //     name: 'longitude',
        //     options: {
        //         setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
        //     }
        // },
        {
          label: 'Furniture',
          name: 'furniture',
          options: {
            setCellProps: () => ({ style: { minWidth: "250px", maxWidth: "1500px" } })
          }
        },
        {
          label: 'Policy',
          name: 'policy',
          options: {
            setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "500px" } })
          }
        },
        {
          label: 'Project Name',
          name: 'project_name',
          options: {
            setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "500px" } })
          }
        },
        {
          label: 'Street',
          name: 'street',
          options: {
            setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
          }
        },
        {
          label: 'Ward',
          name: 'ward',
          options: {
            setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
          }
        },
        {
          label: 'District',
          name: 'district',
          options: {
            setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
          }
        },
        {
          label: 'Province',
          name: 'province',
          options: {
            setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
          }
        },
      ],
      data: [["Loading data ..."]],
      isLoading: false,
      message: null,

      // select state:
      isMenuOpen: false,
      price: "0-max",
      website: "",
      post_type: "",
    }

    this.isAuthorized = this.isAuthorized.bind(this);

    this.getData = this.getData.bind(this);
    this.formatDataForImage = this.formatDataForImage.bind(this);
    this.changePage = this.changePage.bind(this);
    this.changeRowsPerPage = this.changeRowsPerPage.bind(this);

    this.handleSelectMenuOpen = this.handleSelectMenuOpen.bind(this);
    this.handleWebsiteChange = this.handleWebsiteChange.bind(this);
    this.handleChangeRowsPerPage = this.handleChangeRowsPerPage.bind(this);
    this.handleChangePrice = this.handleChangePrice.bind(this);
    this.handleChangePostType = this.handleChangePostType.bind(this);

    // Submit:
    this.submitData = this.submitData.bind(this);
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
        self.getData();
      })
      .catch(function(errors) {
          console.log(errors)
          self.setState({ isLogged: false })
      })
  }

  getMuiTheme = () => createMuiTheme({
    overrides: {
    }
  })

  formatDataForImage = (res, url) => {
    let self = this
    // console.log(res.data.results[0].image_urls[0])
    let results = res.data.results
    
    for (let i = 0; i < results.length; i++) {
      let image_urls = results[i].image_urls
      if (image_urls.length > 0) {
        for (let j = 0; j < image_urls.length; j++) {
            image_urls[j] = <img className="col-4 col-md-4 my-1" src={image_urls[j]} alt="this-is-img" srcset=""/>
        }
        results[i].image_urls = image_urls
      }
    }
    self.setState(
      {
        data: results,
        isLoading: false,
        count: res.data.count,
        url: url
      }
    )
  }

  getData = () => {
    let self = this
    self.setState({ isLoading: true });
    axios
      .get("/bds/api/realestatedata/", 
        {}, 
        {
          headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
          }
        }
      )
      .then(function(res){
        self.formatDataForImage(res, "/bds/api/realestatedata/");
      })
      .catch(function(errors) {
        // console.log(errors)
        self.setState({ message: "You need to login to view content!" })
      });
  };

  changePage = (page) => {
    // console.log("Go to page", page);
    this.setState({ isLoading: true, });
    let self = this;
    
    if (self.state.url === "/bds/filter/") {
      axios
        .get(self.state.url, {
          params: {
              page: page+1,
              website: self.state.website,
              price: self.state.price,
              post_type: self.post_type,
              rowsPerPage: self.state.rowsPerPage
              // offset: this.state.offset,
          },
        },
        {
          headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
          }
        }
      )
      .then(function(res){
          self.formatDataForImage(res, self.state.url);
      })
      .catch(function(errors) {
          console.log(errors)
          self.setState({ message: "Unable to change page! "})
      });
    }
    else {
      axios
        .get(self.state.url, {
          params: {
              page: page+1,
              // offset: this.state.offset,
          }
        },
        {
          headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
          }
        }
      )
      .then(function(res){
          self.formatDataForImage(res, self.state.url);
      })
      .catch(function(errors) {
          console.log(errors)
          self.setState({ message: "Unable to change page! "})
      });
      }
  }

  changeRowsPerPage = (page, rows) => {
    // console.log("Current rows", rows)
    this.setState(
      { 
        isLoading: true,
        rowsPerPage: rows,
      }
    )

    let self = this
    axios
      .get(self.state.url, 
        {
          params: {
            page: page+1,
            page_size: rows
          }
        },
        {
          headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
          }
        }
      )
      .then(function(res) {
          self.formatDataForImage(res, self.state.url);
      })
      // .catch(err => console.log(err));
  }

  handleSelectMenuOpen = () => {
    this.setState({ isMenuOpen: !this.state.isMenuOpen })
  }

  handleWebsiteChange = selectedOption => {
    this.setState({ website: selectedOption.value })
  }

  handleChangeRowsPerPage = selectedOption => {
    this.setState({ rowsPerPage: selectedOption.value })
  }

  handleChangePrice = selectedOption => {
    this.setState({ price: selectedOption.value })
  }

  handleChangePostType = selectedOption => {
    this.setState({ post_type: selectedOption.value })
  }

  submitData = (e) => {
    // e.preventDefault();
    let self = this
    axios
      .get('/bds/filter/', {
        params: {
          website: self.state.website,
          price: self.state.price,
          post_type: self.state.post_type,
          page_size: self.state.rowsPerPage
        }
      }, 
      {
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
        }
      }
      )
      .then(function(res) {
        console.log(res);
        self.setState(
          {
            message: 'Successful!',
            url: "/bds/filter/"
          }
        )
        self.formatDataForImage(res, self.state.url)
      })
      .catch(function(err) {
        // console.log(err);
        self.setState(
          {
            message: 'Failed to load filtered data'
          }
        )
      })
  }

  render() {

    if (this.state.isLogged === false) {
      // return <Login message="You need to login before view contents!" />
      return <Redirect exact to="/login" component={<Login message="You need to login before view contents!" />} />
    }

    // Table variables:
    const options = {
      filterType: 'dropdown',
      tableBodyHeight: '430px',
      tableBodyMaxHeight: '100%',
      responsive: 'vertical',
      jumpToPage: false,
      serverSide: true,
      rowsPerPageOptions:{},
      rowsPerPage: this.state.rowsPerPage,
      // rowsPerPageOptions: [10, 50, 100, 200, 500, 1000],
      download: false,
      filter: false,
      print: false,
      search: false,
      selectableRows: "none",
      count: this.state.count,
      // page: page,
      onTableChange: (action, tableState) => {
        // console.log(action, tableState);

        // a developer could react to change on an action basis or
        // examine the state as a whole and do whatever they want

        switch (action) {
          case 'changePage':
            this.changePage(tableState.page);
            break;
          case 'changeRowsPerPage':
            // console.log(tableState.rowsPerPage);
            this.changeRowsPerPage(tableState.page, tableState.rowsPerPage);
            break;
          default:
                // console.log('action not handled.');
        }
      },
    }

    // Buttons state:
    const chooseWebPage = [
      { label: "All", value: "" },
      { label: "https://batdongsan.com.vn/", value: "https://batdongsan.com.vn" },
      { label: "https://propzy.vn/", value: "https://propzy.vn/" },
      { label: "https://homedy.com/", value: "https://homedy.com/" }
    ];

    const rowsPerPage = [
      { label: "10", value: 10 },
      { label: "20", value: 20 },
      { label: "50", value: 50 },
      { label: "100", value: 100 },
      { label: "150", value: 150 },
    ];

    const choosePrice = [
      { label: "All", value: "0-max" },
      { label: "<5 billion", value: "0-5" },
      { label: "5-10 billion", value: "5-10" },
      { label: "10-20 billion", value: "10-20" },
      { label: "20-30 billion", value: "20-30" },
      { label: ">30 billion", value: "30-max" }
    ];

    const choosePostType = [
      { label: "All", value: "" },
      { label: "Bán đất", value: "Bán đất" },
      { label: "Bán đất nền dự án", value: "Bán đất nền dự án" },
      { label: "Bán nhà riêng", value: "Bán nhà riêng" },
      { label: "Bán nhà mặt phố", value: "Bán nhà mặt phố" },
      { label: "Bán nhà biệt thự, liền kề", value: "Bán nhà biệt thự" },
      { label: "Bán căn hộ chung cư", value: "Bán căn hộ chung cư" },
      { label: "Bán kho, nhà xưởng", value: "Bán kho nhà xưởng" },
      { label: "Bán loại đất động sản khác", value: "Bán loại bất động sản khác" }
    ]

    return (
      <Fragment>
        <WebNavbar name="Crawling Website" />
        
        <div className="container-fluid mt-5">
          <div className="row mt-5">
            <div className="col-1 col-md-1 bg-light"></div>
            <div className="col-10 col-md-10">
      
              <div className="row">
                <div className="col-3 col-md-3">
                  <FormGroup className="mt-4">
                      <Label className="control-label">Choose website</Label>
                      <Select
                        // className="customSelect"
                        options={chooseWebPage}
                        defaultValue={chooseWebPage[0]}
                        onChange={this.handleWebsiteChange}
                        onMenuOpen={this.handleSelectMenuOpen}
                      />
                  </FormGroup>
                </div>

                <div className="col-2 col-md-2">
                  <FormGroup className="mt-4">
                      <Label className="control-label">Choose Price</Label>
                      <Select
                        // className="customSelect"
                        options={choosePrice}
                        defaultValue={choosePrice[0]}
                        onChange={this.handleChangePrice}
                        onMenuOpen={this.handleSelectMenuOpen}
                      />
                  </FormGroup>
                </div>

                <div className="col-2 col-md-2">
                  <FormGroup className="mt-4">
                      <Label className="control-label">Choose Post Type</Label>
                      <Select
                        // className="customSelect"
                        options={choosePostType}
                        defaultValue={choosePostType[0]}
                        onChange={this.handleChangePostType}
                        onMenuOpen={this.handleSelectMenuOpen}
                      />
                  </FormGroup>
                </div>

                <div className="col-3 col-md-3">
                  <Button color="primary" className="ml-3 mt-5" onClick={this.submitData}>Submit</Button>
                </div>
              </div>
              
              <div className="row">
                <div className="col-2 col-md-2">
                  <FormGroup>
                      <Label className="control-label">Rows per Page</Label>
                      <Select
                        // className="customSelect"
                        options={rowsPerPage}
                        defaultValue={{ label: "10", value: 10 }}
                        onChange={this.handleChangeRowsPerPage}
                      />
                  </FormGroup>
                </div>
              </div>

              {/* Table */}
              <div className="mt-2">
                {/* <div className="text-center mb-4">{this.state.message}</div> */}
                <div className="row data-table">
                  {/* <div class="col-1 col-md-1 px-0"></div> */}
                  <div className="col-12 col-md-12 px-0">
                    <MuiThemeProvider theme={this.getMuiTheme()}>
                      <MUIDataTable
                        title={
                          <Typography variant="h6">
                            Real Estate Data
                            {this.state.isLoading && (
                              <CircularProgress
                              size={24}
                              style={{ marginLeft: 15, position: "relative", top: 4 }}
                              />
                            )}
                          </Typography>
                        }
                        columns = { this.state.columns }
                        data = { this.state.data }
                        options = { options }
                      />
                    </MuiThemeProvider>
                  </div>
                  {/* <div className="col-1 col-md-1 px-0"></div> */}
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

export default Data; 