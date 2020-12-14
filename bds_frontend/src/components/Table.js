import React from 'react';
// import { MDBDataTableV5 } from 'mdbreact';
import { CircularProgress, Typography } from "@material-ui/core";
import MUIDataTable from "mui-datatables";
// import { createMuiTheme, MuiThemeProvider } from '@material-ui/core/styles';
import { Row, Col } from "reactstrap";
import axios from 'axios';


class Table extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            // pagination:
            
            // page: 1,
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
                    label: 'Post Title',
                    name: 'post_title',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "600px", maxWidth: "1600px" } })
                    }
                },
                {
                    label: 'Price Unit',
                    name: 'price_unit',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "100px", maxWidth: "1000px" } })
                    }
                },
                {
                    label: 'Price',
                    name: 'price',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Total Site Area',
                    name: 'total_site_area',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Property Name',
                    name: 'property_name',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Address ID',
                    name: 'address_id',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "250px", maxWidth: "2500px" } })
                    }
                },
                {
                    label: 'Number of Bedrooms',
                    name: 'number_of_bedrooms',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "100px", maxWidth: "1000px" } })
                    }
                },
                {
                    label: 'Number of Bathrooms',
                    name: 'number_of_bathrooms',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "100px", maxWidth: "1000px" } })
                    }
                },
                {
                    label: 'Project ID',
                    name: 'project_id',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Project Size',
                    name: 'project_size',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Post Author',
                    name: 'post_author',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Property Code',
                    name: 'property_code',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Full Description',
                    name: 'full_description',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "1800px", maxWidth: "1800px" } })
                    }
                },
                {
                    label: 'Phone Number',
                    name: 'phone_number',
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
                    label: 'Property Type ID',
                    name: 'property_type_id',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Property Sub Type ID',
                    name: 'property_sub_type_id',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Block Code',
                    name: 'block_code',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Block Name',
                    name: 'block_name',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Number of Floors',
                    name: 'number_of_floors',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Floor',
                    name: 'floor',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'House Design',
                    name: 'house_design',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Direction',
                    name: 'direction',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Building Area',
                    name: 'building_area',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Carpet Areas',
                    name: 'carpet_areas',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Unit of Measure ID',
                    name: 'unit_of_measure_id',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Owner is Author',
                    name: 'owner_is_author',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Owner ID',
                    name: 'owner_id',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Longitude',
                    name: 'longitude',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Latitude',
                    name: 'latitude',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Legal Info',
                    name: 'legal_info',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Internal Facility',
                    name: 'internal_facility',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Near Facility',
                    name: 'near_facility',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Front Length',
                    name: 'front_length',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Route Length',
                    name: 'route_length',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Updated Datetime',
                    name: 'updated_datetime',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Created Datetime',
                    name: 'created_datetime',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Expired Datetime',
                    name: 'expired_datetime',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Is Called API',
                    name: 'is_called_api',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
                {
                    label: 'Images',
                    name: 'images',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "800px", maxWidth: "800px" } })
                    }
                },
                {
                    label: 'City',
                    name: 'city',
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
                    label: 'Ward Commune',
                    name: 'ward_commune',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
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
                    label: 'Match Location',
                    name: 'match_location',
                    options: {
                        setCellProps: () => ({ style: { minWidth: "150px", maxWidth: "1500px" } })
                    }
                },
            ],
            data: [["Loading data ..."]],
            isLoading: false,
        };
        this.changePage = this.changePage.bind(this);
    }

    componentDidMount() {
        this.getData();
    }

    getData = () => {
        this.setState({ isLoading: true });
        axios
            .get("/api/bdss/", {
                // params: {
                //     limit: this.state.limit,
                //     offset: this.state.offset,
                // }
            })
            .then(res => this.setState(
                { 
                    data: res.data.results,
                    isLoading: false,
                    count: res.data.count, 
                }
            ))
            // .catch(err => console.log(err));
    };

    changePage = (page) => {
        console.log("Go to page", page);

        this.setState({ isLoading: true, });
        axios
            .get("api/bdss/", {
                params: {
                    page: page+1,
                    // offset: this.state.offset,
                }
            })
            .then(res => this.setState(
                { 
                    data: res.data.results,
                    isLoading: false,
                    count: res.data.count
                }
            ))
            // .catch(err => console.log(err));
    }

    changeRowsPerPage = (page, rows) => {
        console.log("Current rows", rows)

        this.setState({ isLoading: true, })
        axios
            .get("api/bdss/", {
                params: {
                    page: page+1,
                    page_size: rows
                }
            })
            .then(res => this.setState(
                {
                    data: res.data.results,
                    isLoading: false,
                    count: res.data.count,
                }
            ))
            // .catch(err => console.log(err));
    }

    render() {
        const { count, isLoading, } = this.state;

        const options = {
            filter: true,
            filterType: 'dropdown',
            responsive: 'standard',
            serverSide: true,
            rowsPerPageOptions: [5, 10, 20, 30, 50, 100],
            selectableRows: false,
            count: count,
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
                        console.log('action not handled.');
                }
            },
            search: true,
        }

        return (
            <div className="mt-5">
                <Row>
                    <Col md="1"></Col>
                    <Col md="10">
                    <MUIDataTable
                        title={
                            <Typography variant="h6">
                                Real Estate Data
                                {isLoading && (
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
                    </Col>
                    <Col md="1"></Col>
                </Row>
            </div>
        )
    }
}

export default Table;