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
import './style.css';

class WebNavbar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isOpen: false,
      isLogout: false,
      message: '',
      current_user: '',

      // dropdown:
      dropdownOpen: false,
    }
    this.toggleDropdown = this.toggleDropdown.bind(this);
    this.toggleOpen = this.toggleOpen.bind(this);
    this.handleClick = this.handleClick.bind(this);
  }

  componentDidMount() {
    this.getCurrentUser();
  }

  getCurrentUser = () => {
    let self = this;
    axios
      .get("/bds/current_user/")
      .then(function(response) {
        console.log(response);
        self.setState({ current_user: response.data.username })
      })
      .catch(function(errors) {
        console.log(errors);
      })
  }

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
      .post("/bds/logout/", 
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
      return <Redirect exact to="/login" component={<Login message="Logout successfully!" />} />
    }
    
    if (this.props.name === "Login" || this.props.name === "Register") {
      return (
        <Navbar color="light" light expand="md" fixed="top">
          <NavbarBrand href="/">{this.props.name}</NavbarBrand>
        </Navbar>
      )
    }

    return(
      <div>
        <Navbar color="light" light expand="md" fixed="top">
          <NavbarBrand href="/">{this.props.name}</NavbarBrand>
          <NavbarToggler onClick={this.toggleOpen} />
          <Collapse isOpen={this.state.isOpen} navbar>
            <Nav className="mr-auto" navbar>
              <NavItem>
                <NavLink tag={rNavLink} exact to="/dashboard" activeClassName="active">Dashboard</NavLink>
              </NavItem>
              
              <NavItem>
                <NavLink tag={rNavLink} exact to="/data" activeClassName="active">Data</NavLink>
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
              <DropdownToggle tag="span" data-toggle="dropdown" aria-expanded={this.state.dropdownOpen}>
                {this.state.current_user}
              </DropdownToggle>
              <DropdownMenu>
                <DropdownItem>
                  <Link exact to="/login" className="text-dark text-decoration-none" onClick={() => this.handleClick("logout")}>Logout</Link>
                </DropdownItem>
              </DropdownMenu>
            </Dropdown>
            </NavLink>
          </Collapse>
        </Navbar>

        {/* <p>Result: {this.state.message}</p> */}
    </div>
    );
  }
}

export default WebNavbar;