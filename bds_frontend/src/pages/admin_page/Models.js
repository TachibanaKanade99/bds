import { Component, Fragment } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';

// react-select:
import Select from 'react-select';

// reactstrap:
import { FormGroup, Label, Form, } from 'reactstrap';

// @material-ui:
import Switch from '@material-ui/core/Switch';

// import CSS:
import './styles.css';

export default class Models extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isMenuOpen: false,

      // property states:
      request_page: "predict",
      property_type: null,
      district: null,

      ward_lst: [],
      ward: null,

      street_lst: [],
      street: null,

      isEnableLOF: false,
      
      message: null,
      model_name: null,
      degree: null,
      model_coef: "",
      model_intercept: "",
      train_rmse: null,
      test_rmse: null,
      train_r2_score: null,
      test_r2_score: null,
      figure: null,
    }

    this.handleChoosePropertyType = this.handleChoosePropertyType.bind(this);
    this.handleSelectMenuOpen = this.handleSelectMenuOpen.bind(this);
    this.getWardLst = this.getWardLst.bind(this);
    this.getStreetLst = this.getStreetLst.bind(this);
    this.convertIntoOptions = this.convertIntoOptions.bind(this);
    this.handleChooseDistrictType = this.handleChooseDistrictType.bind(this);
    this.handleChooseWardType = this.handleChooseWardType.bind(this);
    this.handleChooseStreetType = this.handleChooseStreetType.bind(this);
    this.handleChangeEnableLOF = this.handleChangeEnableLOF.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentDidMount() {
    this.getWardLst(this.state.district);
    this.getStreetLst(this.state.district, this.state.ward);
  }

  convertIntoOptions = (value, index, array) => {
    return { "label": value, "value": value }
  }

  getWardLst = (district) => {
    let self = this;
    axios
      .post("/bds/api/realestatedata/ward_lst/", {
        request_page: self.state.request_page,
        property_type: self.state.property_type,
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
        property_type: self.state.property_type,
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

  handleChangeEnableLOF = (e) => {
    this.setState({  isEnableLOF: e.target.checked })
  }

  handleSubmit = (e) => {
    e.preventDefault();
    let self = this;

    axios
      .post("/bds/api/realestatedata/train_model/", {
        property_type: self.state.property_type,
        district: self.state.district,
        ward: self.state.ward,
        street: self.state.street,
        isEnableLOF: self.state.isEnableLOF
      },
      {
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
        }
      })
      .then((res) => {
        console.log(res);
        
        self.setState({
          message: res.data.message,
          model_name: res.data.model_name,
          degree: res.data.degree,
          model_coef: res.data.model_coef,
          model_intercept: res.data.model_intercept,
          train_rmse: res.data.train_rmse,
          test_rmse: res.data.test_rmse,
          train_r2_score: res.data.train_r2_score,
          test_r2_score: res.data.test_r2_score,
          figure: 'data:image/png;base64,' + res.data.figure 
        })
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
      <div className="container-fluid">
        <Fragment>
          <div className="mt-5 mx-auto pt-5 h4 font-weight-bold">Admin can retrain model in specific locations here</div>
          <hr />

          <div className="row">
            <div className="col-12 col-md-5">
              <div className="row">
                <div className="col-10 col-md-6">
                  <Form onSubmit={this.handleSubmit}>
                    <div className="row">
                      <div className="col-10 col-md-10 pl-4">
                        <FormGroup className="mt-4">
                          <Label className="control-label">Property Type</Label>
                          <Select
                            // className="customSelect"
                            options={propertyTypes}
                            defaultValue={null}
                            onChange={this.handleChoosePropertyType}
                            onMenuOpen={this.handleSelectMenuOpen}
                          />
                        </FormGroup>
                      </div>

                      <div className="col-10 col-md-10 pl-4">
                        <FormGroup className="mt-4">
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

                      <div className="col-10 col-md-10 pl-4">
                        <FormGroup className="mt-4">
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

                      <div className="col-10 col-md-10 pl-4">
                        <FormGroup className="mt-4">
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

                      <div className="col-10 col-md-10 pl-4">
                        <FormGroup className="mt-4">
                          <Label className="control-label">Use Local Outlier Factor</Label>
                          <Switch
                            checked={this.state.isEnableLOF}
                            onChange={this.handleChangeEnableLOF} 
                            color="primary"
                            name="isEnableLOF"
                            inputProps={{ 'aria-label': 'primary checkbox' }}
                          />
                        </FormGroup>
                      </div>

                      <div className="col-10 col-md-10 text-center">
                        <button type="submit" className="mt-3 btn btn-primary">Train model</button>
                      </div>
                    </div>
                  </Form>
                </div>

                <div className="col-10 col-md-6">
                  <p>{this.state.message}</p>
                  
                  <p>
                    <span className="font-weight-bold">Model used to train data: </span>
                    <span>{this.state.model_name}</span> 
                  </p>
                  
                  <p>
                    <span className="font-weight-bold">Degree: </span>
                    <span>{this.state.degree}</span>
                  </p>
                  
                  <hr />

                  <div>
                    <p className="font-weight-bold">Model Coefficients: </p>
                    <span className="auto-newline">{"[" + this.state.model_coef.toString() + "]"}</span>
                  </div>

                  <br />

                  <div>
                    <p className="font-weight-bold">Model Intercept: </p>
                    <span>{"[" + this.state.model_intercept.toString() + "]"}</span>
                  </div>

                  <hr />

                  <p>
                    <span className="font-weight-bold">Train RMSE: </span>
                    <span>{this.state.train_rmse}</span>  
                  </p>
                  
                  <p>
                    <span className="font-weight-bold">Test RMSE: </span>
                    <span>{this.state.test_rmse}</span>
                  </p>
                  
                  <p>
                    <span className="font-weight-bold">Train R2 score: </span>
                    <span>{this.state.train_r2_score}</span>
                  </p>
                  
                  <p>
                    <span className="font-weight-bold">Test R2 score: </span>
                    <span>{this.state.test_r2_score}</span>
                  </p>
                </div>

              </div>
            </div>
            <div className="col-12 col-md-7 text-center">
              <img alt="train model" src={this.state.figure} />
            </div>
          </div>
        </Fragment>
      </div>
    )
  }
}