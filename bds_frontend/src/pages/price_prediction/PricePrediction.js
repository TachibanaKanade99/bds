import { Fragment, Component } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';

// reactstrap:
import { Form, FormGroup, Label, Input } from 'reactstrap';

// react-select:
import Select from 'react-select';

// import CSS:
import './styles.css';

// Local components:
import WebNavbar from './../../components/layout/WebNavbar';

export default class PricePrediction extends Component {
  constructor(props) {
    super(props);
    this.state = {
      current_user: null,

      // property states:
      property_type: null,
      area: null,
      district: null,

      ward_lst: [],
      ward: null,
      
      street_lst: [],
      street: null,

      // predicted price:
      predicted_price: null,

      // menu select state:
      isMenuOpen: false,
    }
    
    this.getCurrentUser = this.getCurrentUser.bind(this);
    this.getWardLst = this.getWardLst.bind(this);
    this.getStreetLst = this.getStreetLst.bind(this);
    this.convertIntoOptions = this.convertIntoOptions.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleChoosePropertyType = this.handleChoosePropertyType.bind(this);
    this.handleChooseDistrictType = this.handleChooseDistrictType.bind(this);
    this.handleChooseWardType = this.handleChooseWardType.bind(this);
    this.handleChooseStreetType = this.handleChooseStreetType.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentDidMount() {
    this.getCurrentUser();
    this.getWardLst(null);
    this.getStreetLst(null, null);
  }

  getCurrentUser = () => {
    let self = this;
    axios
      .get("/bds/current_user/")
      .then((res) => {
        self.setState({ current_user: res.data.username })
      })
      .catch((err) => {
        console.log(err);
      })
  }

  convertIntoOptions = (value, index, array) => {
    return { "label": value, "value": value }
  }

  getWardLst = (district) => {
    let self = this;
    axios
      .post("/bds/api/realestatedata/ward_lst/", {
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

  getStreetLst = (ward, district) => {
    let self = this;
    axios
      .post("/bds/api/realestatedata/street_lst/", {
        ward: ward,
        district: district,
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

  handleChange = (e) => {
    const name = e.target.name;
    const value = e.target.value;

    this.setState({
      [name]: value
    })
  }

  handleSelectMenuOpen = () => {
    this.setState({ isMenuOpen: !this.state.isMenuOpen })
  }

  handleChoosePropertyType = (selectedOption) => {
    this.setState({ property_type: selectedOption.value })
  }

  handleChooseDistrictType = (selectedOption) => {
    this.setState({ district: selectedOption.value })

    // handle ward_lst:
    this.getWardLst(selectedOption.value);

    // handle street_lst:
    this.getStreetLst(this.state.ward, selectedOption.value);
  }

  handleChooseWardType = (selectedOption) => {
    this.setState({ ward: selectedOption.value })

    // handle street_lst:
    this.getStreetLst(selectedOption.value, this.state.district);
  }

  handleChooseStreetType = (selectedOption) => {
    this.setState({ street: selectedOption.value })
  }

  handleSubmit = (e) => {
    e.preventDefault();
    let self = this;
    axios
      .post("/bds/api/realestatedata/price_predict/", {
        property_type: self.state.property_type,
        area: self.state.area,
        street: self.state.street,
        ward: self.state.ward,
        district: self.state.district
      },
      {
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
        }
      }
      )
      .then((res) => {
        console.log(res);
        self.setState({ predicted_price: res.data + " billion" })
      })
      .catch((err) => {
        console.log(err);
      })
  }

  render() {

    // property types:

    const propertyTypes = [
      { label: "Lands", value: "Bán đất" },
      { label: "Houses", value: "Bán nhà riêng" },
      { label: "Departments", value: "Bán căn hộ, chung cư" }
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
            <div className="col-1 col-md-2 bg-light"></div>
            <div className="col-10 col-md-8 mt-5 text-center web-body">
              <Form onSubmit={this.handleSubmit}>
                <FormGroup className="row mt-4">
                  <Label className="px-0 col-4 col-md-3 my-2 control-label">Property Type</Label>
                  <Select
                    options={propertyTypes}
                    name="property_type"
                    defaultValue={""}
                    placeholder="Choose property type"
                    onChange={this.handleChoosePropertyType}
                    onMenuOpen={this.handleSelectMenuOpen}
                    className="col-8 col-md-4 px-0"
                  />
                </FormGroup>

                <FormGroup className="row mt-4">
                  <Label for="web-area" className="px-0 col-4 col-md-3 my-2 control-label">Area (m)</Label>
                  <Input 
                    type="text"
                    name="area"
                    pattern="[0-9]*[.][0-9]*"
                    onChange={this.handleChange}
                    className="col-7 col-md-4"
                    id="web-area"
                    placeholder="Enter area"
                  />
                </FormGroup>

                <FormGroup className="row mt-4">
                  <Label className="px-0 col-4 col-md-3 my-2 control-label">District</Label>
                  <Select
                    options={districtTypes}
                    name="district"
                    placeholder="Choose district"
                    defaultValue={""}
                    onChange={this.handleChooseDistrictType}
                    onMenuOpen={this.handleSelectMenuOpen}
                    className="col-7 col-md-4 px-0"
                  />
                </FormGroup>

                <FormGroup className="row mt-4">
                  <Label className="px-0 col-4 col-md-3 my-2 control-label">Ward</Label>
                  <Select
                    options={this.state.ward_lst}
                    name="ward"
                    defaultValue={""}
                    placeholder="Choose ward"
                    onChange={this.handleChooseWardType}
                    onMenuOpen={this.handleSelectMenuOpen}
                    className="col-7 col-md-4 px-0"
                  />
                </FormGroup>

                <FormGroup className="row mt-4">
                  <Label className="px-0 col-4 col-md-3 my-2 control-label">Street</Label>
                  <Select
                    options={this.state.street_lst}
                    name="street"
                    defaultValue={""}
                    placeholder="Choose street"
                    onChange={this.handleChooseStreetType}
                    onMenuOpen={this.handleSelectMenuOpen}
                    className="col-7 col-md-4 px-0"
                  />
                </FormGroup>

                <div className="text-center col-md-8 mt-3">
                  <button type="submit" className="btn col-6 col-md-2 web-btn">Predict</button>
                </div>
              </Form>

              <FormGroup className="row mt-4">
                <Label className="px-0 col-4 col-md-3 my-2 control-label">Predicted Price</Label>
                <span className="my-2 h3 text-primary">{this.state.predicted_price}</span>
              </FormGroup>
            </div>
            <div className="col-1 col-md-2 bg-light"></div>
          </div>
        </div>
      </Fragment>
    )
  }
}