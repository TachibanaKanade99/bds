import React from 'react';
// import { MDBDataTableV5 } from 'mdbreact';
import { CircularProgress, Typography } from "@material-ui/core";
import MUIDataTable from "mui-datatables";
import { Row, Col } from "reactstrap";
import axios from 'axios';


class Table extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            // pagination:
            limit: 1,
            offset: 1,
            prevPage: null,
            nextPage: null,

            page: 1,
            count: 1,
            rowsPerPage: 5,
            sortOrder: {},
            columns: [
                {
                    label: 'Url',
                    name: 'url',
                    // width: 200,
                },
                {
                    label: 'Post Title',
                    name: 'post_title',
                    // width: 270,
                },
                {
                    label: 'Price Unit',
                    name: 'price_unit',
                    // width: 200,
                },
                {
                    label: 'Price',
                    name: 'price',
                    // sort: 'asc',
                    // width: 150,
                },
                {
                    label: 'Total Site Area',
                    name: 'total_site_area',
                    // sort: 'disabled',
                    // width: 200,
                },
                {
                    label: 'Property Name',
                    name: 'property_name',
                    // sort: 'disabled',
                    // width: 200,
                },
                {
                    label: 'Address ID',
                    name: 'address_id',
                    // width: 200,
                },
                {
                    label: 'Number of Bedrooms',
                    name: 'number_of_bedrooms',
                    // width: 200,
                },
                {
                    label: 'Number of Bathrooms',
                    name: 'number_of_bathrooms',
                    // width: 220,
                },
                {
                    label: 'Project ID',
                    name: 'project_id',
                    // width: 200,
                },
                {
                    label: 'Project Size',
                    name: 'project_size',
                    // width: 200,
                },
                {
                    label: 'Post Author',
                    name: 'post_author',
                    // width: 200,
                },
                {
                    label: 'Property Code',
                    name: 'property_code',
                    // width: 200,
                },
                {
                    label: 'Full Description',
                    name: 'full_description',
                    // width: 200,
                },
                {
                    label: 'Phone Number',
                    name: 'phone_number',
                    // width: 200,
                },
                {
                    label: 'Email',
                    name: 'email',
                    // width: 200,
                },
                {
                    label: 'Property Type ID',
                    name: 'property_type_id',
                    // width: 200,
                },
                {
                    label: 'Property Sub Type ID',
                    name: 'property_sub_type_id',
                    // width: 200,
                },
                {
                    label: 'Block Code',
                    name: 'block_code',
                    // width: 200,
                },
                {
                    label: 'Block Name',
                    name: 'block_name',
                    // width: 200,
                },
                {
                    label: 'Number of Floors',
                    name: 'number_of_floors',
                    // width: 200,
                },
                {
                    label: 'Floor',
                    name: 'floor',
                    // width: 200,
                },
                {
                    label: 'House Design',
                    name: 'house_design',
                    // width: 200,
                },
                {
                    label: 'Direction',
                    name: 'direction',
                    // width: 200,
                },
                {
                    label: 'Building Area',
                    name: 'building_area',
                    // width: 200,
                },
                {
                    label: 'Carpet Areas',
                    name: 'carpet_areas',
                    // width: 200,
                },
                {
                    label: 'Unit of Measure ID',
                    name: 'unit_of_measure_id',
                    // width: 200,
                },
                {
                    label: 'Owner is Author',
                    name: 'owner_is_author',
                    // width: 200,
                },
                {
                    label: 'Owner ID',
                    name: 'owner_id',
                    // width: 200,
                },
                {
                    label: 'Longitude',
                    name: 'longitude',
                    // width: 200,
                },
                {
                    label: 'Latitude',
                    name: 'latitude',
                    // width: 200,
                },
                {
                    label: 'Legal Info',
                    name: 'legal_info',
                    // width: 200,
                },
                {
                    label: 'Internal Facility',
                    name: 'internal_facility',
                    // width: 200,
                },
                {
                    label: 'Near Facility',
                    name: 'near_facility',
                    // width: 200,
                },
                {
                    label: 'Front Length',
                    name: 'front_length',
                    // width: 200,
                },
                {
                    label: 'Route Length',
                    name: 'route_length',
                    // width: 200,
                },
                {
                    label: 'Updated Datetime',
                    name: 'updated_datetime',
                    // width: 200,
                },
                {
                    label: 'Created Datetime',
                    name: 'created_datetime',
                    // width: 200,
                },
                {
                    label: 'Expired Datetime',
                    name: 'expired_datetime',
                    // width: 200,
                },
                {
                    label: 'Is Called API',
                    name: 'is_called_api',
                    // width: 200,
                },
                {
                    label: 'Images',
                    name: 'images',
                    // width: 200,
                },
                {
                    label: 'City',
                    name: 'city',
                    // width: 200,
                },
                {
                    label: 'District',
                    name: 'district',
                    // width: 200,
                },
                {
                    label: 'Ward Commune',
                    name: 'ward_commune',
                    // width: 200,
                },
                {
                    label: 'Street',
                    name: 'street',
                    // width: 200,
                },
                {
                    label: 'Match Location',
                    name: 'match_location',
                    // width: 200,
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
                params: {
                    limit: this.state.limit,
                    offset: this.state.offset,
                }
            })
            .then(res => this.setState(
                { 
                    data: res.data.results,
                    isLoading: false,
                    count: res.data.count, 
                }
            ))
            .catch(err => console.log(err));
    };

    changePage = (page) => {
        console.log("Go to page", page);

        this.setState({ isLoading: true, offset: this.state.offset + 1 });
        axios
            .get("api/bdss/", {
                params: {
                    limit: this.state.limit,
                    offset: this.state.offset,
                }
            })
            .then(res => this.setState(
                { 
                    data: res.data.results,
                    isLoading: false,
                    count: res.data.count
                }
            ))
            .catch(err => console.log(err));
    }

    render() {
        const { page, count, isLoading } = this.state;

        const options = {
            filterType: 'dropdown',
            filter: true,
            responsive: 'vertical',
            serverSide: true,
            rowsPerPage: 1,
            rowsPerPageOptions: [1],
            count: count,
            page: page,
            onTableChange: (action, tableState) => {
                if (action === "changePage"){
                    this.changePage(tableState.page);
                }
            },
            // sortOrder: sortOrder,
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