import { Fragment, Component } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';

// MUI Datatable:
import { CircularProgress, Typography } from "@material-ui/core";
import { createMuiTheme, MuiThemeProvider } from '@material-ui/core/styles';
import MUIDataTable from "mui-datatables";

// reactstrap
import { FormGroup, Label, Button, } from 'reactstrap';

// react-select:
import Select from 'react-select';

// datepicker:
import DayPickerInput from 'react-day-picker/DayPickerInput';
import 'react-day-picker/lib/style.css';

// moment js:
import 'moment/locale/vi';
import MomentLocaleUtils, { formatDate, parseDate, } from 'react-day-picker/moment';

// Import CSS:
import './styles.css';

// Local components:
import WebNavbar from './../../components/layout/WebNavbar';

export default class Data extends Component {
  constructor(props) {
    super(props);
    this.state = {
      current_user: null,

      // Table state:
      count: null,
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
            setCellProps: () => ({ style: { minWidth: "200px", maxWidth: "1500px" } })
          }
        },
        {
          label: 'Email',
          name: 'email',
          options: {
            setCellProps: () => ({ style: { minWidth: "300px", maxWidth: "600px" } })
          }
        },
        {
          label: 'Facade',
          name: 'facade',
          options: {
            setCellProps: () => ({ style: { minWidth: "200px", maxWidth: "500px" } })
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
        {
            label: 'Latitude',
            name: 'latitude',
            options: {
                setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
            }
        },
        {
            label: 'Longitude',
            name: 'longitude',
            options: {
                setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
            }
        },
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

      // Filter options:
      website: null,
      price: "0-max",
      post_type: null,
      page_size: 10,
      startDate: new Date(2020, 7, 31).toLocaleDateString(),
      endDate: new Date().toLocaleDateString(),

      request_page: "data",
      district: null,

      ward_lst: [],
      ward: null,

      street_lst: [],
      street: null,
    }

    this.getCurrentUser = this.getCurrentUser.bind(this);
    this.getData = this.getData.bind(this);
    this.formatDataForImage = this.formatDataForImage.bind(this);
    this.changePage = this.changePage.bind(this);
    this.changeRowsPerPage = this.changeRowsPerPage.bind(this);

    this.handleSelectMenuOpen = this.handleSelectMenuOpen.bind(this);
    this.handleWebsiteChange = this.handleWebsiteChange.bind(this);
    this.handleChangeRowsPerPage = this.handleChangeRowsPerPage.bind(this);
    this.handleChangePrice = this.handleChangePrice.bind(this);
    this.handleChangePostType = this.handleChangePostType.bind(this);
    this.handleStartDate = this.handleStartDate.bind(this);
    this.handleEndDate = this.handleEndDate.bind(this);

    this.getWardLst = this.getWardLst.bind(this);
    this.getStreetLst = this.getStreetLst.bind(this);
    this.convertIntoOptions = this.convertIntoOptions.bind(this);

    this.handleChooseDistrictType = this.handleChooseDistrictType.bind(this);
    this.handleChooseWardType = this.handleChooseWardType.bind(this);
    this.handleChooseStreetType = this.handleChooseStreetType.bind(this);

    // Submit:
    this.submitData = this.submitData.bind(this);
  }

  componentDidMount() {
    this.getCurrentUser();
    this.getData();
    this.getWardLst(this.state.district);
    this.getStreetLst(this.state.district, this.state.ward);
  }

  convertIntoOptions = (value, index, array) => {
    return { "label": value, "value": value }
  }

  getCurrentUser = () => {
    let self = this;
    axios
      .get("/bds/current_user/")
      .then(function(res) {
        // console.log(res);
        self.setState({ current_user: res.data.username })
      })
      .catch(function(err) {
        console.log(err);
      })
  }

  getWardLst = (district) => {
    let self = this;
    axios
      .post("/bds/api/realestatedata/ward_lst/", {
        request_page: self.state.request_page,
        property_type: null,
        district: district
      },
      {
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
        }
      }
      )
      .then((res) => {
        console.log(res);
        self.setState({ ward_lst: res.data.map(self.convertIntoOptions) })
      })
      .catch((err) => {
        console.log(err);
      })
  }

  getStreetLst = (district, ward) => {
    let self = this;
    axios
      .post("/bds/api/realestatedata/street_lst/", {
        request_page: self.state.request_page,
        property_type: null,
        district: district,
        ward: ward
      },
      {
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
        }
      }
      )
      .then((res) => {
        console.log(res);
        self.setState({ street_lst: res.data.map(self.convertIntoOptions) })
      })
      .catch((err) => {
        console.log(err);
      })
  }

  getMuiTheme = () => createMuiTheme({
    overrides: {
    }
  })

  formatDataForImage = (res) => {
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
        rowsPerPage: results.length
      }
    )
  }

  getData = () => {
    let self = this
    self.setState({ isLoading: true });
    axios
      .get("/bds/api/realestatedata/", 
        {
          params: {
            website: self.state.website,
            price: self.state.price,
            post_type: self.state.post_type,
            page_size: self.state.page_size,
            start_date: self.state.startDate,
            end_date: self.state.endDate,
            district: self.state.district,
            ward: self.state.ward,
            street: self.state.street
          }
        }, 
        {
          headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
          }
        }
      )
      .then(function(res){
        // console.log(res);
        self.formatDataForImage(res);
      })
      .catch(function(err) {
        // console.log(err);
        self.setState({ message: "Failed!" })
      });
  };

  changePage = (page) => {
    // console.log("Go to page", page);
    this.setState({ isLoading: true });
    let self = this;
    
    axios
      .get("/bds/api/realestatedata/", {
        params: {
            page: page+1,
            website: self.state.website,
            price: self.state.price,
            post_type: self.state.post_type,
            page_size: self.state.page_size,
            start_date: self.state.startDate,
            end_date: self.state.endDate,
            district: self.state.district,
            ward: self.state.ward,
            street: self.state.street
        },
      },
      {
        headers: {
        'X-CSRFToken': Cookies.get('csrftoken')
        }
      }
    )
    .then(function(res){
        console.log(res)
        self.formatDataForImage(res);
    })
    .catch(function(err) {
        // console.log(err)
        self.setState({ message: "Unable to change page! "})
    });
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

  handleWebsiteChange = (selectedOption) => {
    this.setState({ website: selectedOption.value })
  }

  handleChangeRowsPerPage = (selectedOption) => {
    this.setState({ page_size: selectedOption.value })
  }

  handleChangePrice = (selectedOption) => {
    this.setState({ price: selectedOption.value })
  }

  handleChangePostType = (selectedOption) => {
    this.setState({ post_type: selectedOption.value })
  }

  handleStartDate = (date) => {
    this.setState({ startDate: date.toLocaleDateString()})
    console.log(this.state.startDate);
  }

  handleEndDate = (date) => {
    this.setState({ endDate: date.toLocaleDateString()})
  }

  handleChooseDistrictType = (selectedOption) => {
    this.setState({ district: selectedOption.value })

    // handle ward_lst:
    this.getWardLst(selectedOption.value);

    // handle street_lst:
    this.getStreetLst(selectedOption.value, this.state.ward);
  }

  handleChooseWardType = (selectedOption) => {
    this.setState({ ward: selectedOption.value })

    this.setState({ street: '' })

    // handle street_lst:
    this.getStreetLst(this.state.district, selectedOption.value);
  }

  handleChooseStreetType = (selectedOption) => {
    this.setState({ street: selectedOption.value })
  }

  submitData = (e) => {
    // e.preventDefault();
    this.getData();
  }

  render() {

    // Table variables:
    const options = {
      filterType: 'dropdown',
      tableBodyHeight: '420px',
      tableBodyMaxHeight: '100%',
      responsive: 'simple',
      jumpToPage: false,
      serverSide: true,
      // rowsPerPageOptions:{},
      rowsPerPage: this.state.rowsPerPage,
      rowsPerPageOptions: [],
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
      { label: "All", value: null },
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
      { label: "All", value: null },
      { label: "Bán đất", value: "Bán đất" },
      { label: "Bán đất nền dự án", value: "Bán đất nền dự án (đất trong dự án quy hoạch)" },
      { label: "Bán nhà riêng", value: "Bán nhà riêng" },
      { label: "Bán nhà mặt phố", value: "Bán nhà mặt phố" },
      { label: "Bán nhà mặt phố (nhà mặt tiền trên các tuyến phố)", value: "Bán nhà mặt phố (nhà mặt tiền trên các tuyến phố)" },
      { label: "Bán nhà biệt thự, liền kề", value: "Bán nhà biệt thự, liệt kề (nhà trong dự án quy hoạch)" },
      { label: "Bán căn hộ chung cư", value: "Bán căn hộ chung cư" },
      { label: "Bán kho, nhà xưởng", value: "Bán kho, nhà xưởng" },
      { label: "Bán trang trại, khu nghỉ dưỡng", value: "Bán trang trại, khu nghỉ dưỡng"},
      { label: "Bán loại đất động sản khác", value: "Bán loại bất động sản khác" }
    ]

    const districtTypes = [
      { label: "1", value: "1" },
      { label: "2", value: "2" },
      { label: "3", value: "3" },
      { label: "4", value: "4" },
      { label: "5", value: "5" },
      { label: "6", value: "6" },
      { label: "7", value: "7" },
      { label: "8", value: "8" },
      { label: "9", value: "9" },
      { label: "10", value: "10" },
      { label: "11", value: "11" },
      { label: "12", value: "12" },
      { label: "Bình Tân", value: "Bình Tân" },
      { label: "Bình Thạnh", value: "Bình Thạnh" },
      { label: "Thủ Đức", value: "Thủ Đức" },
      { label: "Hóc Môn", value: "Hóc Môn" },
      { label: "Tân Bình", value: "Tân Bình" },
      { label: "Bình Chánh", value: "Bình Chánh" },
      { label: "Phú Nhuận", value: "Phú Nhuận" },
      { label: "Gò Vấp", value: "Gò Vấp" },
      { label: "Tân Phú", value: "Tân Phú" },
      { label: "Nhà Bè", value: "Nhà Bè" },
      { label: "Cần Giờ", value: "Cần Giờ" },
      { label: "Củ Chi", value: "Củ Chi" }
    ]

    return (
      <Fragment>
        <WebNavbar name="Crawling WebApp" current_user={this.state.current_user} />
        
        <div className="container-fluid mt-5">
          <div className="row mt-5">
            <div className="col-1 col-md-1 bg-light"></div>
            <div className="col-10 col-md-10">

              <div className="row">
                <div className="col- col-md-10">
                  <div className="row">
                    <div className="col-10 col-md-3">
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

                    <div className="col-10 col-md-2">
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

                    <div className="col-10 col-md-3">
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

                    <div className="col-10 col-md-2">
                      <FormGroup className="mt-4">
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

                    <div className="col-10 col-md-2">
                      <FormGroup className="mt-4">
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
                  </div>

                  <div className="row">
                    <div className="col-10 col-md-2">
                      <FormGroup>
                          <Label className="control-label">Rows per Page</Label>
                          <Select
                            options={rowsPerPage}
                            defaultValue={{ label: "10", value: 10 }}
                            onChange={this.handleChangeRowsPerPage}
                          />
                      </FormGroup>
                    </div>

                    <div className="col-10 col-md-3">
                      <FormGroup>
                        <Label className="control-label">District</Label>
                        <Select
                          options={districtTypes}
                          name="district"
                          placeholder="Choose district"
                          defaultValue={null}
                          onChange={this.handleChooseDistrictType}
                          onMenuOpen={this.handleSelectMenuOpen}
                        />
                      </FormGroup>
                    </div>

                    <div className="col-10 col-md-3">
                      <FormGroup>
                        <Label className="control-label">Ward</Label>
                        <Select
                          options={this.state.ward_lst}
                          name="ward"
                          defaultValue={null}
                          placeholder="Choose ward"
                          onChange={this.handleChooseWardType}
                          onMenuOpen={this.handleSelectMenuOpen}
                        />
                      </FormGroup>
                    </div>

                    <div className="col-10 col-md-3">
                      <FormGroup>
                        <Label className="control-label">Street</Label>
                        <Select
                          options={this.state.street_lst}
                          name="street"
                          defaultValue={null}
                          placeholder="Choose street"
                          onChange={this.handleChooseStreetType}
                          onMenuOpen={this.handleSelectMenuOpen}
                        />
                      </FormGroup>
                    </div>

                  </div>
                </div>
                <div className="col- col-md-2 pl-0">
                  <Button className="ml-3 mt-5 web-btn text-left" onClick={this.submitData}>Filter</Button>
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