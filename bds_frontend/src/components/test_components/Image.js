import { Component } from 'react';
import axios from 'axios';
import { ThumbUpTwoTone } from '@material-ui/icons';

class Image extends Component {
    constructor(props) {
        super(props);
        this.state = {
            image_url: null,
        }
    }

    componentDidMount() {
        this.getImage();
    }

    getImage = () => {
        axios({
            method: 'get',
            url: '/api/image/',
        })
        .then(res => this.setState(
            {
                image_url: res.data.results[0]["images"],
            }
        ))
    }

    render() {
        console.log(this.state.image_url);
        return (
            <img src={ this.state.image_url } alt="this-is-new-img" />
        )
    }
}

export default Image;