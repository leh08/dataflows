import React from 'react';
import { connect } from 'react-redux';
import { logOut } from '../../actions';

class LogOut extends React.Component {
    componentDidMount() {
        this.props.logOut();
    }

    render() {
        return <div>You have logged out!</div>
    }
}

export default connect(null, { logOut })(LogOut);