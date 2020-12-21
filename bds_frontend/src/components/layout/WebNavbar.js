import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import axios from 'axios';

// Reactstrap:
import {
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
  // Button,
  // ButtonGroup
} from 'reactstrap';

// React-router:
import { NavLink as rNavLink } from 'react-router-dom';

class WebNavbar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isOpen: false,
      isLogout: false,
      message: '',
    }
    this.toggleOpen = this.toggleOpen.bind(this);
    this.handleClick = this.handleClick.bind(this);
  }

  toggleOpen = () => {
    this.setState(state => ({
      isOpen: !state.isOpen
    }))
  }

  handleClick = (selected) => {
    let self = this;
    axios
      .post("/logout/")
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
      return <Redirect exact to="/logout/" />
    }

    return(
      <div>
        <Navbar color="light" light expand="md">
          <NavbarBrand href="/">Crawling Website</NavbarBrand>
          <NavbarToggler onClick={this.toggleOpen} />
          <Collapse isOpen={this.state.isOpen} navbar>
            <Nav className="mr-auto" navbar>
              <NavItem>
                <NavLink tag={rNavLink} exact to="/dashboard" activeClassName="active">Dashboard</NavLink>
              </NavItem>
              
              <NavItem>
                <NavLink tag={rNavLink} exact to="/data" activeClassName="active">Data</NavLink>
              </NavItem>
              
              <NavItem>
                <NavLink tag={rNavLink} exact to="/register" activeClassName="active" onClick={() => this.handleClick("register")}>Register</NavLink>
              </NavItem>

              <NavItem>
                <NavLink tag={rNavLink} exact to="/login" activeClassName="active" onClick={() => this.handleClick("login")}>Login</NavLink>
              </NavItem>

              <NavItem>
                {/* <NavLink tag={rNavLink} exact to="/logout" activeClassName="active" onClick={() => this.handleClick("logout")}>Logout</NavLink> */}
                <NavLink onClick={() => this.handleClick("logout")}>Logout</NavLink>
              </NavItem>
            </Nav>

            {/* <ButtonGroup>
              <Button color="light" onClick={() => this.handleClick("register")}>Register</Button>
              <Button color="light" onClick={() => this.handleClick("login")}>Login</Button>
            </ButtonGroup> */}
          </Collapse>
        </Navbar>

        <p>Result: {this.state.message}</p>
    </div>
    );
  }
}

export default WebNavbar;