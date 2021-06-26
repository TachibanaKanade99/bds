import { Fragment, Component } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';

// MUI Datatable:
import { CircularProgress, Typography, } from "@material-ui/core";
import { createMuiTheme, MuiThemeProvider } from '@material-ui/core/styles';
import MUIDataTable from "mui-datatables";

export default class Users extends Component {
  constructor(props) {
    super(props);
    this.state = {
      count: null,
      rowsPerPage: 10,
      sortOrder: {},
      columns: [
        {
          label: 'Username',
          name: 'username',
          options: {
            setCellProps: () => ({ style: { minWidth: "250px", maxWidth: "500px" } })
          }
        },
        {
          label: 'Is SuperUser',
          name: 'is_superuser',
          options: {
            filter: true,
            setCellProps: () => ({ style: { minWidth: "200px", maxWidth: "500px" } }),
            customBodyRender: (value, tableMeta, updateValue) => {
              return (
                <div>
                  <i 
                    class={value ? "fas fa-check-square" : "far fa-square"}>
                  </i>
                </div>
              );
            }
          }
        },
        {
          label: 'Last Login',
          name: 'last_login',
          options: {
            setCellProps: () => ({ style: { minWidth: "350px", maxWidth: "600px" } })
          }
        },
        {
          label: 'Is Active',
          name: 'is_active',
          options: {
            filter: true,
            setCellProps: () => ({ style: { minWidth: "200px", maxWidth: "500px" } }),
            customBodyRender: (value, tableMeta, updateValue) => {
              // let checked = value;

              return (
                <div>
                  <i 
                    class={value ? "fas fa-check-square" : "far fa-square"}>
                  </i>
                </div>
              );
            }
        },
      },
      {
        label: 'Date Joined',
        name: 'date_joined',
        options: {
          setCellProps: () => ({ style: { minWidth: "350px", maxWidth: "600px" } })
        }
      }
      ],
      data: [["Loading data ... "]],
      isLoading: false,
    }

    this.getMuiTheme = this.getMuiTheme.bind(this);
    this.getUserLst = this.getUserLst.bind(this);
    this.changePage = this.changePage.bind(this);
    this.changeRowsPerPage = this.changeRowsPerPage.bind(this);
  }

  componentDidMount() {
    this.getUserLst();
  }

  getMuiTheme = () => createMuiTheme({
    overrides: {
    }
  })

  getUserLst = () => {
    let self = this;
    axios
      .get("/bds/api/user_lst/", {
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
          }
      })
      .then((res) => {
        console.log(res);
        self.setState({
          count: res.data.count,
          data: res.data.results,
          isLoading: false,
          rowsPerPage: res.data.count,
        })
      })
      .catch((err) => {
        console.log(err);
      })
  }

  changePage = (page) => {
    this.setState({ isLoading: true });
    
    let self = this;
    axios
      .get("/bds/api/user_lst/", {
        params: {
          page: page+1,
        }
      },
      {
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
          }
      })
      .then((res) => {
        console.log(res);
        self.setState({
          count: res.data.count,
          data: res.data.results,
          isLoading: false,
          rowsPerPage: res.data.count,
        })
      })
      .catch((err) => {
        console.log(err);
      })
  }

  changeRowsPerPage = (page, rows) => {
    this.setState({
      isLoading: true,
      rowsPerPage: rows
    })

    let self = this;
    axios
      .get("/bds/api/user_lst/", {
        params: {
          page: page+1,
          page_size: rows
        }
      },
      {
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
        }
      })
      .then((res) => {
        console.log(res);
        self.setState({
          count: res.data.count,
          data: res.data.results,
          isLoading: false,
          rowsPerPage: res.data.count,
        })
      })
      .catch((err) => {
        console.log(err);
      })
  }

  render() {

    // Table variables:
    const options = {
      filterType: 'dropdown',
      tableBodyHeight: '420px',
      tableBodyMaxHeight: '100%',
      responsive: 'simple',
      jumpToPage: false,
      serverSide: true,
      // rowsPerPage: this.state.rowsPerPage,
      // rowsPerPageOptions: [10, 50, 100, 200, 500, 1000],
      download: false,
      filter: true,
      print: false,
      search: false,
      selectableRows: "multiple",
      count: this.state.count,
      // page: page,
      onTableChange: (action, tableState) => {
        // console.log(action, tableState);

        // a developer could react to change on an action basis or
        // examine the state as a whole and do whatever they want

        switch (action) {
          case 'changePage':
            this.changePage(tableState.page);
            break;
          case 'changeRowsPerPage':
            // console.log(tableState.rowsPerPage);
            this.changeRowsPerPage(tableState.page, tableState.rowsPerPage);
            break;
          default:
                // console.log('action not handled.');
        }
      },
    }

    return (
      <div className="container-fluid">
        <Fragment>
          <div className="mt-5 pt-5 pl-5 font-weight-bold h4">
            List of Users
          </div>

          {/* Table */}
          <div className="mt-5">
            {/* <div className="text-center mb-4">{this.state.message}</div> */}
            <div className="row data-table">
              {/* <div class="col-1 col-md-1 px-0"></div> */}
              <div className="col-11 col-md-11 px-3 ml-5">
                <MuiThemeProvider theme={this.getMuiTheme()}>
                  <MUIDataTable
                    title={
                      <Typography variant="h6">
                        Real Estate Data
                        {this.state.isLoading && (
                          <CircularProgress
                          size={24}
                          style={{ marginLeft: 15, position: "relative", top: 4 }}
                          />
                        )}
                      </Typography>
                    }
                    columns = { this.state.columns }
                    data = { this.state.data }
                    options = { options }
                  />
                </MuiThemeProvider>
              </div>
              {/* <div className="col-1 col-md-1 px-0"></div> */}
            </div>
          </div>

        </Fragment>
      </div>
    )
  }
}