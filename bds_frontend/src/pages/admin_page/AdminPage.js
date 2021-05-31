import { Fragment, Component } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';

// import CSS:
import './styles.css'

// Local components:
import WebNavbar from '../../components/layout/WebNavbar';

export default class AdminPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      current_user: null,
    }
    this.getCurrentUser = this.getCurrentUser.bind(this);
  }

  componentDidMount() {
    this.getCurrentUser();
  }

  getCurrentUser = () => {
    let self = this;
    axios
      .get("/bds/current_user/")
      .then((res) => {
        console.log(res);
        self.setState({ current_user: res.data.username })
      })
      .catch((err) => {
        console.log(err);
      })
  }

  render() {
    return (
      <Fragment>
        <WebNavbar name="Crawling WebApp" current_user={this.state.current_user} />
      </Fragment>
    )
  }
}