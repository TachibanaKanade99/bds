import React, { Component } from 'react';
import Chart from 'react-apexcharts';

class WebChart extends Component {
  constructor(props) {
    super(props);
    this.state = {
      options: {
        // colors: ['#343a40', '#007bff', '#dc3545', '#ffc107', '#17a2b8'],
        theme: {
          palette: 'palette1' // upto palette10
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
            show: false,
          },
          fontFamily: 'Helvetica, Arial, sans-serif',
        },
        plotOptions: {
          bar: {
            dataLabels: {
              position: 'top',
            }
          },
        },
        dataLabels: {
          enabled: true,
          style: {
            colors: ['#343a40']
          },
          offsetY: -20,
          dropShadow: {
            enabled: false,
          }
        },
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
        labels: this.props.labels
      },

      categories: [],
      series: [],
    }
  }

  render() {
    // console.log(this.props.series);
    return (
      <Chart 
        options={this.state.options}
        series={this.props.series}
        // labels={this.props.labels}
        categories={this.props.categories}
        type={this.props.type}
        width={this.props.width}
        height={this.props.height}
      />
    )
  }
}

export default WebChart;