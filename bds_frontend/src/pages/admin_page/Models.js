import { Component, Fragment } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';

// react-select:
import Select from 'react-select';

// reactstrap:
import { FormGroup, Label, Form, } from 'reactstrap';

// import CSS:
import './styles.css';

export default class Models extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isMenuOpen: false,

      // property states:
      property_type: null,
      district: null,

      ward_lst: [],
      ward: null,

      street_lst: [],
      street: null,

      // train - test r2 score:
      // train_score: null,
      // test_score: null,

      img: null,
    }

    this.handleChoosePropertyType = this.handleChoosePropertyType.bind(this);
    this.handleSelectMenuOpen = this.handleSelectMenuOpen.bind(this);
    this.getWardLst = this.getWardLst.bind(this);
    this.getStreetLst = this.getStreetLst.bind(this);
    this.convertIntoOptions = this.convertIntoOptions.bind(this);
    this.handleChooseDistrictType = this.handleChooseDistrictType.bind(this);
    this.handleChooseWardType = this.handleChooseWardType.bind(this);
    this.handleChooseStreetType = this.handleChooseStreetType.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentDidMount() {
    this.getWardLst(null);
    this.getStreetLst(null, null);
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

  handleChoosePropertyType = (selectedOption) => {
    this.setState({ property_type: selectedOption.value })
  }

  handleSelectMenuOpen = () => {
    this.setState({ isMenuOpen: !this.state.isMenuOpen })
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
      .post("/bds/api/realestatedata/train_model/", {
        property_type: self.state.property_type,
        street: self.state.street,
        ward: self.state.ward,
        district: self.state.district
      },
      {
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
        }
      })
      .then((res) => {
        console.log(res);
        self.setState({ img: 'data:image/png;base64,' + res.data })
      })
      .catch((err) => {
        console.log(err);
      })
  }

  render() {

    const propertyTypes = [
      { label: "Lands", value: "Bán đất" },
      { label: "Houses", value: "Bán nhà riêng" },
      { label: "Departments", value: "Bán căn hộ chung cư" }
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
        <div className="mt-5 ml-5 pt-5 h4 font-weight-bold">Admin can retrain model in specific locations here</div>
        <hr />

        <div className="row">
          <div className="col-12 col-md-5">
            <Form onSubmit={this.handleSubmit}>
              <div className="row">
                <div className="col-1 col-md-1"></div>
                <div className="col-10 col-md-6">
                  <FormGroup className="mt-4">
                    <Label className="control-label">Property Type</Label>
                    <Select
                      // className="customSelect"
                      options={propertyTypes}
                      defaultValue={""}
                      onChange={this.handleChoosePropertyType}
                      onMenuOpen={this.handleSelectMenuOpen}
                    />
                  </FormGroup>
                </div>
              </div>

              <div className="row">
                <div className="col-1 col-md-1"></div>
                <div className="col-10 col-md-6">
                  <FormGroup className="mt-4">
                    <Label className="control-label">District</Label>
                    <Select
                      options={districtTypes}
                      name="district"
                      placeholder="Choose district"
                      defaultValue={""}
                      onChange={this.handleChooseDistrictType}
                      onMenuOpen={this.handleSelectMenuOpen}
                    />
                  </FormGroup>
                </div>
              </div>

              <div className="row">
                <div className="col-1 col-md-1"></div>
                <div className="col-10 col-md-6">
                  <FormGroup className="mt-4">
                    <Label className="control-label">Ward</Label>
                    <Select
                      options={this.state.ward_lst}
                      name="ward"
                      defaultValue={""}
                      placeholder="Choose ward"
                      onChange={this.handleChooseWardType}
                      onMenuOpen={this.handleSelectMenuOpen}
                    />
                  </FormGroup>
                </div>
              </div>

              <div className="row">
                <div className="col-1 col-md-1"></div>
                <div className="col-10 col-md-6">
                  <FormGroup className="mt-4">
                    <Label className="control-label">Street</Label>
                    <Select
                      options={this.state.street_lst}
                      name="street"
                      defaultValue={""}
                      placeholder="Choose street"
                      onChange={this.handleChooseStreetType}
                      onMenuOpen={this.handleSelectMenuOpen}
                    />
                  </FormGroup>
                </div>
              </div>

              <div className="row">
                <div className="col-1 col-md-1"></div>
                <div className="col-10 col-md-6 text-center">
                  <button type="submit" className="mt-4 btn btn-primary">Train model</button>
                </div>
              </div>

            </Form>
          </div>
          <div className="col-12 col-md-7 text-center">
            <img src={this.state.img} alt='image of trained model' />
          </div>
        </div>
      </Fragment>
    )
  }
}