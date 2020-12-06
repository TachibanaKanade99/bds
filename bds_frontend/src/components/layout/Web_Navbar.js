import React, { Component } from 'react';
import {
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
  Button,
  ButtonGroup
} from 'reactstrap';

class Web_Navbar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isOpen: false,
      cmd: "hi",
    }
    this.toggle = this.toggle.bind(this);
    this.handleClick = this.handleClick.bind(this);
  }

  toggle(){
    this.setState(state => ({
      isOpen: !state.isOpen
    }))
  }

  handleClick(selected) {
    if (selected === "login") {
      this.setState({ cmd: "login" })
    }
    else {
      this.setState({ cmd: "register "})
    }
  }

  render() {
    return(
      <div>
        <Navbar color="light" light expand="md">
          <NavbarBrand href="/">Crawling Website</NavbarBrand>
          <NavbarToggler onClick={this.toggle} />
          <Collapse isOpen={this.state.isOpen} navbar>
            <Nav className="mr-auto" navbar>
              <NavItem>
                <NavLink href="/dashboard/">Dashboard</NavLink>
              </NavItem>
              
              <NavItem>
                <NavLink active href="/data/">Data</NavLink>
              </NavItem>
              
              <NavItem>
                <NavLink href="/report/">Report</NavLink>
              </NavItem>
            </Nav>

            <ButtonGroup>
              <Button color="light" onClick={() => this.handleClick("register")}>Register</Button>
              <Button color="light" onClick={() => this.handleClick("login")}>Login</Button>
            </ButtonGroup>
          </Collapse>
        </Navbar>

      <p>Result: {this.state.cmd}</p>
    </div>
    );
  }
}

export default Web_Navbar;