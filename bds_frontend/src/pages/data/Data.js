import { Fragment } from 'react';

import WebNavbar from './../../components/layout/WebNavbar';
import Table from './Table';
import { useHistory } from 'react-router-dom';


// class Data extends Component {

//   render() {
//     return (
//       <Fragment>
//         <WebNavbar />
//         <div className="text-center h4 font-weight-bold">
//           <p>This is data page</p>
//         </div>
//         <Table />
//       </Fragment>
//     )
//   }
// }

function Data() {

  let history = useHistory();
  console.log(history);

  return (
    <Fragment>
      <WebNavbar />
      <div className="text-center h4 font-weight-bold">
        <p>This is data page</p>
      </div>
      <Table />
    </Fragment>
  )
}

export default Data; 