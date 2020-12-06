/* eslint-disable react/jsx-pascal-case */
import React, { Component } from 'react';
import Web_Navbar from './components/layout/Web_Navbar';
import Table from './components/Table';

// CSS:
import '../node_modules/bootstrap/dist/css/bootstrap.min.css'
import './App.css';

class App extends Component {
  render() {
    return (
      <React.Fragment>
        <Web_Navbar />
        <Table />
      </React.Fragment>
    )
  }
}

export default App;
