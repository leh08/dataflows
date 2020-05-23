import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';


class Header extends React.Component {   
    renderAuth() {
        if (this.props.isSignedIn) {
            return (
                <React.Fragment>
                    <Link to="/logout" className="item">
                        Log Out
                    </Link>
                </React.Fragment>
            );
        } else {
            return (
                <React.Fragment>
                    <Link to="/signup" className="item">
                        Sign Up
                    </Link>
                    <Link to="/login" className="item">
                        Log In
                    </Link>
                </React.Fragment>
            );
        }
    }

    render() {
        return (
            <div className="ui secondary pointing menu">
                <Link to="/" className="item">
                    Data Warehouse
                </Link>
                <Link to="/flows" className="item">
                    Flow
                </Link>
                <div className="right menu">
                    {this.renderAuth()}
                </div>
            </div>
        );
    }
}

function mapStateToProps(state) {
    return { isSignedIn: state.auth.isSignedIn, };
}

export default connect(mapStateToProps)(Header);