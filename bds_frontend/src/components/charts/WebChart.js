import React, { Component } from 'react';
import Chart from 'react-apexcharts';

class WebChart extends Component {
  constructor(props) {
    super(props);
    this.state = {
      options: {
        // colors: ['#343a40', '#007bff', '#dc3545', '#ffc107', '#17a2b8'],
        theme: {
          palette: 'palette8' // upto palette10
        },
        chart: {
          animations: {
            enabled: true,
            easing: 'easeinout',
            speed: 500,
            animateGradually: {
              enabled: true,
              delay: 100,
            },
            dynamicAnimation: {
              enabled: true,
              speed: 350,
            }
          },
          zoom: {
            enabled: true,
          },
          toolbar: {
            show: true,
          },
          fontFamily: 'Helvetica, Arial, sans-serif',
        },
        type: 'bar',
        stroke: {
          curve: 'smooth',
          width: 2,
        },
        grid: {
          borderColor: '#f8f8fa',
          row: {
              colors: ['transparent', 'transparent'], // takes an array which will be repeated on columns
              opacity: 0.5
          },
        },
        noData: {
          text: 'Loading...',
        },
        xaxis: {
          categories: this.props.categories
        }
      },

      series: [
        {
          name: '',
          data: this.props.data,
        },
      ],
    }
  }

  render() {
    console.log(this.props.series);
    return (
      <Chart 
        options={this.state.options}
        series={this.props.series}
        type="bar"
        width="100%"
        height="450"
      />
    )
  }
}

export default WebChart;