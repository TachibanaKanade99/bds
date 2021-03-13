import React from 'react';
import { CircularProgress, Typography } from "@material-ui/core";
import MUIDataTable from "mui-datatables";
import axios from 'axios';
import Cookies from 'js-cookie';

class Table extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            count: 1,
            rowsPerPage: 10,
            sortOrder: {},
            columns: [
                {
                    label: 'Url',
                    name: 'url',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "600px", maxWidth: "1600px" } })
                    }
                },
                {
                    label: 'Content',
                    name: 'content',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "600px", maxWidth: "1600px" } })
                    }
                },
                {
                    label: 'Price',
                    name: 'price',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "100px", maxWidth: "1000px" } })
                    }
                },
                {
                    label: 'Area',
                    name: 'area',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Location',
                    name: 'location',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "600px", maxWidth: "1600px" } })
                    }
                },
                {
                    label: 'Post Author',
                    name: 'posted_author',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Phone',
                    name: 'phone',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Posted Date',
                    name: 'posted_date',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Expired Date',
                    name: 'expired_date',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Item Code',
                    name: 'item_code',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "200px" } })
                    }
                },
                // {
                //     label: 'Images',
                //     name: 'image_urls',
                //     options: {
                //         setCellProps: () => ({ style: { minWidth: "800px", maxWidth: "800px" } })
                //     }
                // },
                {
                    label: 'Post Type',
                    name: 'post_type',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Email',
                    name: 'email',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "200px", maxWidth: "200px" } })
                    }
                },
                {
                    label: 'Facade',
                    name: 'facade',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Entrance',
                    name: 'entrance',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Orientation',
                    name: 'orientation',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Balcony Orientation',
                    name: 'balcony_orientation',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Number of floors',
                    name: 'number_of_floors',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Number of bedrooms',
                    name: 'number_of_bedrooms',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Number of toilets',
                    name: 'number_of_toilets',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                // {
                //     label: 'Latitude',
                //     name: 'latitude',
                //     options: {
                //         setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                //     }
                // },
                // {
                //     label: 'Longitude',
                //     name: 'longitude',
                //     options: {
                //         setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                //     }
                // },
                {
                    label: 'Furniture',
                    name: 'furniture',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "250px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Policy',
                    name: 'policy',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "500px" } })
                    }
                },
                {
                    label: 'Project Name',
                    name: 'project_name',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "500px" } })
                    }
                },
                {
                    label: 'Street',
                    name: 'street',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Ward',
                    name: 'ward',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'District',
                    name: 'district',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Province',
                    name: 'province',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
            ],
            data: [["Loading data ..."]],
            isLoading: false,
            // modal: false,
            // picture: null,
        };
        // this.toggleModal = this.toggleModal.bind(this);
        this.formatDataForImage = this.formatDataForImage.bind(this);
        this.changePage = this.changePage.bind(this);
        this.changeRowsPerPage = this.changeRowsPerPage.bind(this);
    }

    componentDidMount() {
        this.getData();
    }

    formatDataForImage = (res) => {
        let self = this
        console.log(res.data.results[0].image_urls[0])
        let results = res.data.results
        
        for (let i = 0; i < results.length; i++) {
            let image_urls = results[i].image_urls
            if (image_urls.length > 0) {
                for (let j = 0; j < image_urls.length; j++) {
                    image_urls[j] = <img className="col-4 col-md-4 my-1" src={image_urls[j]} alt="this-is-img" srcset=""/>
                }
                results[i].image_urls = image_urls
            }
        }
        self.setState(
            {
                data: results,
                isLoading: false,
                count: res.data.count,
            }
        )

        // Update csrf token:
        // console.log(axios.defaults.headers.common['X-CSRFToken'], Cookies.get('csrftoken'));
        
        // let axios_csrftoken = axios.defaults.headers.common['X-CSRFToken'];
        // let cookie_csrftoken = Cookies.get('csrftoken');
        // let isChanged = axios_csrftoken === cookie_csrftoken;
        // if (isChanged === false) {
        //     axios.defaults.headers.common['X-CSRFToken'] = cookie_csrftoken;
        // }
        
        // console.log("After:");
        // console.log(axios.defaults.headers.common['X-CSRFToken'], Cookies.get('csrftoken'));
    }

    getData = () => {
        let self = this
        self.setState({ isLoading: true });
        axios
            .get("/bds/api/realestatedata/", 
            {}, 
            {
                headers: {
                'X-CSRFToken': Cookies.get('csrftoken')
                }
            }
            )
            .then(function(res){
                self.formatDataForImage(res);
            })
            .catch(function(errors) {
                console.log(errors)
                self.setState({ message: "You need to login to view content!" })
            });
    };

    changePage = (page) => {
        // console.log("Go to page", page);

        this.setState({ isLoading: true, });
        let self = this;
        axios
            .get("/bds/api/realestatedata/", {
                params: {
                    page: page+1,
                    // offset: this.state.offset,
                }
            },
            {
                headers: {
                'X-CSRFToken': Cookies.get('csrftoken')
                }
            }
            )
            .then(function(res){
                self.formatDataForImage(res);
            })
            .catch(function(errors) {
                console.log(errors)
                self.setState({ message: "Unable to change page! "})
            });
    }

    changeRowsPerPage = (page, rows) => {
        // console.log("Current rows", rows)

        this.setState(
            { 
                isLoading: true,
                rowsPerPage: rows,
            }
        )

        let self = this
        axios
            .get("/bds/api/realestatedata/", {
                params: {
                    page: page+1,
                    page_size: rows
                }
            },
            {
                headers: {
                'X-CSRFToken': Cookies.get('csrftoken')
                }
            }
            )
            .then(function(res) {
                self.formatDataForImage(res);
            })
            // .catch(err => console.log(err));
    }

    render() {
        // const { count, isLoading, rowsPerPage} = this.state;

        const options = {
            filterType: 'dropdown',
            tableBodyHeight: '40%',
            tableBodyMaxHeight: '50%',
            responsive: 'scroll',
            jumpToPage: false,
            serverSide: true,
            rowsPerPage: this.state.rowsPerPage,
            rowsPerPageOptions: [10, 50, 100, 200, 500, 1000],
            download: false,
            filter: false,
            print: false,
            search: false,
            selectableRows: "none",
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
            <div className="mt-2">
                {/* <div className="text-center mb-4">{this.state.message}</div> */}
                <div className="row data-table">
                    {/* <div class="col-1 col-md-1 px-0"></div> */}
                    <div className="col-12 col-md-12 px-0">
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
                    </div>
                    {/* <div className="col-1 col-md-1 px-0"></div> */}
                </div>
            </div>
        )
    }
}

export default Table;