import React, { Component } from 'react';
import { Redirect, Link } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'js-cookie';

// Reactstrap:
import {
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
  // NavbarText,
  Dropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem,
  // Button,
  // ButtonGroup
} from 'reactstrap';

// React-router:
import { NavLink as rNavLink } from 'react-router-dom';

// Import Component:
import Login from './../../pages/login/Login';

// Import CSS:
import './styles.css';

class WebNavbar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isOpen: false,
      isLogout: false,
      message: '',

      // dropdown:
      dropdownOpen: false,
    }
    this.toggleDropdown = this.toggleDropdown.bind(this);
    this.toggleOpen = this.toggleOpen.bind(this);
    this.handleClick = this.handleClick.bind(this);
  }

  componentDidMount() {
    // this.getCurrentUser();
  }

  // getCurrentUser = () => {
  //   if (this.props.name !== "Login" && this.props.name !== "Register") {
  //     let self = this;
  //     axios
  //       .get("/bds/current_user/")
  //       .then((res) => {
  //         // console.log(res);
  //         self.setState({ isSuperUser: res.data.is_superuser })

  //         if (res.data.is_superuser === true) {
  //           self.setState({ adminNavItemClass: null })
  //         }
  //       })
  //       .catch((err) => {
  //         console.log(err);
  //       })
  //   }
  // }

  toggleDropdown = () => {
    this.setState(state => ({
      dropdownOpen: !state.dropdownOpen
    }))
  }

  toggleOpen = () => {
    this.setState(state => ({
      isOpen: !state.isOpen
    }))
  }

  handleClick = (selected) => {
    let self = this;
    axios
      .post("/bds/api/logout/", 
      {}, 
      {
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
        }
      }
      )
      .then(function(response) {
        console.log(response);
        self.setState({ isLogout: true })
      })
      .catch(function(errors) {
        console.log(errors);
        self.setState({ message: "Logout Failed!" });
      })
  }

  render() {
    if (this.state.isLogout) {
      return <Redirect exact="true" to="/login" component={<Login message="Logout successfully!" />} />
    }
    
    if (this.props.name === "Login") {
      return (
        <div className="bg-white" id="customNavbar">
          <Navbar expand="md">
            <NavbarBrand href="/" className="text-blue">{this.props.name}</NavbarBrand>
            <NavbarToggler onClick={this.toggleOpen} />
            <Collapse isOpen={this.state.isOpen} navbar>
              <Nav className="mr-auto" navbar></Nav>
              <NavLink 
                tag={rNavLink} 
                to={{ pathname: "/register"}}
                activeStyle={{ color: "#3C5999" }}
              >Register</NavLink>
            </Collapse>
          </Navbar>
        </div>
      )
    }

    else if (this.props.name === "Register") {
      return (
        <div className="bg-white" id="customNavbar">
          <Navbar expand="md">
            <NavbarBrand href="/" className="text-blue">{this.props.name}</NavbarBrand>
            <NavbarToggler onClick={this.toggleOpen} />
            <Collapse isOpen={this.state.isOpen} navbar>
              <Nav className="mr-auto" navbar></Nav>
              <NavLink 
                tag={rNavLink} 
                to={{ pathname: "/login"}} 
                activeStyle={{ color: "#3C5999" }}
              >Login</NavLink>
            </Collapse>
          </Navbar>
        </div>
      )
    }

    else if (this.props.name === "Admin Page") {
      return (
        <div className="bg-white" id="customNavbar">
          <Navbar expand="md">
            <NavbarBrand href="/" className="text-blue">{this.props.name}</NavbarBrand>
            <NavbarToggler onClick={this.toggleOpen} />
            <Collapse isOpen={this.state.isOpen} navbar>
              <Nav className="mr-auto" navbar>
                <NavLink 
                  tag={rNavLink} 
                  to={{ pathname: "/admin_page/:users", state: { isAuthenticated: true, isSuperUser: this.props.is_superuser }}} 
                  activeStyle={{ color: "#3C5999" }}
                >
                  Users
                </NavLink>

                <NavLink 
                  tag={rNavLink} 
                  to={{ pathname: "/admin_page/:models", state: { isAuthenticated: true, isSuperUser: this.props.is_superuser }}}
                  activeStyle={{ color: "#3C5999" }}
                >
                  Models
                </NavLink>

                <NavLink 
                  tag={rNavLink} 
                  to={{ pathname: "/dashboard"}}
                  activeStyle={{ color: "#3C5999" }}
                >
                  Back to Main Page
                </NavLink>

              </Nav>

              <NavLink href="#" className="user-text text-dark">
                <Dropdown isOpen={this.state.dropdownOpen} toggle={this.toggleDropdown}>
                  <DropdownToggle tag="span" data-toggle="dropdown" aria-expanded={this.state.dropdownOpen} className="text-dark">
                    {this.props.current_user}
                  </DropdownToggle>
                  <DropdownMenu>
                    <DropdownItem>
                      <Link exact="true" to="/login" className="text-dark text-decoration-none" onClick={() => this.handleClick("logout")}>Logout</Link>
                    </DropdownItem>
                  </DropdownMenu>
                </Dropdown>
              </NavLink>

            </Collapse>
          </Navbar>
        </div>
      )
    }

    else {
      return(
        <div className="bg-white" id="customNavbar">
          <Navbar expand="md">
            <NavbarBrand href="/" className="text-blue">{this.props.name}</NavbarBrand>
            <NavbarToggler onClick={this.toggleOpen} />
            <Collapse isOpen={this.state.isOpen} navbar>
              <Nav className="mr-auto" navbar>
                <NavItem>
                  <NavLink 
                    tag={rNavLink} 
                    to={{ pathname: "/dashboard", state: { isAuthenticated: true, isSuperUser: this.props.is_superuser } }}
                    activeStyle={{ color: "#3C5999" }}
                  >Dashboard</NavLink>
                </NavItem>
                
                <NavItem>
                  <NavLink 
                    tag={rNavLink} 
                    to={{ pathname: "/data", state: { isAuthenticated: true, isSuperUser: this.props.is_superuser } }}
                    activeStyle={{ color: "#3C5999" }}
                  >Data</NavLink>
                </NavItem>

                <NavItem>
                  <NavLink 
                    tag={rNavLink} 
                    to={{ pathname: "/price_prediction", state: { isAuthenticated: true, isSuperUser: this.props.is_superuser } }}
                    activeStyle={{ color: "#3C5999" }}
                  >Price Prediction</NavLink>
                </NavItem>

                <NavItem className={this.props.is_superuser === true ? null : "d-none"}>
                  <NavLink
                    tag={rNavLink} 
                    to={{ pathname: "/admin_page/:users", state: { isAuthenticated: true, isSuperUser: this.props.is_superuser } }}
                    activeStyle={{ color: "#3C5999" }}
                  >Admin</NavLink>
                </NavItem>
                
                {/* <NavItem>
                  <NavLink tag={rNavLink} exact to="/register" activeClassName="active" onClick={() => this.handleClick("register")}>Register</NavLink>
                </NavItem>

                <NavItem>
                  <NavLink tag={rNavLink} exact to="/login" activeClassName="active" onClick={() => this.handleClick("login")}>Login</NavLink>
                </NavItem> */}

                {/* <NavItem>
                  <NavLink tag={rNavLink} exact to="/logout" activeClassName="active" onClick={() => this.handleClick("logout")}>Logout</NavLink>
                  <NavLink onClick={() => this.handleClick("logout")}>Logout</NavLink>
                </NavItem> */}
              </Nav>

              {/* <ButtonGroup>
                <Button color="light" onClick={() => this.handleClick("register")}>Register</Button>
                <Button color="light" onClick={() => this.handleClick("login")}>Login</Button>
              </ButtonGroup> */}
              <NavLink href="#" className="user-text text-dark">
                <Dropdown isOpen={this.state.dropdownOpen} toggle={this.toggleDropdown}>
                  <DropdownToggle tag="span" data-toggle="dropdown" aria-expanded={this.state.dropdownOpen} className="text-dark">
                    {this.props.current_user}
                  </DropdownToggle>
                  <DropdownMenu>
                    <DropdownItem>
                      <Link exact="true" to="/login" className="text-dark text-decoration-none" onClick={() => this.handleClick("logout")}>Logout</Link>
                    </DropdownItem>
                  </DropdownMenu>
                </Dropdown>
              </NavLink>
            </Collapse>
          </Navbar>
        </div>
      )
    }
  }
}

export default WebNavbar;