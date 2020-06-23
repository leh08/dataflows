import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';


class Header extends React.Component {   
    renderAuth() {
        if (this.props.isSignedIn) {
            return (
                <React.Fragment>
                    <Link to="/logout" className="bp3-button bp3-minimal">
                        Log Out
                    </Link>
                </React.Fragment>
            );
        } else {
            return (
                <React.Fragment>
                    <Link to="/signup" className="bp3-button bp3-minimal">
                        Sign Up
                    </Link>
                    <Link to="/login" className="bp3-button bp3-minimal">
                        Log In
                    </Link>
                </React.Fragment>
            );
        }
    }

    render() {
        return (
            <div class="bp3-navbar">
                <div class="bp3-navbar-group bp3-align-left">
                    <Link to="/" className="bp3-button bp3-minimal bp3-navbar-heading">
                        Data Warehouse
                    </Link>
                    <div class="bp3-navbar-divider"/>
                    <Link to="/flows" className="bp3-button bp3-minimal bp3-navbar-heading">
                        Flow
                    </Link>
                </div>
                <div class="bp3-navbar-group bp3-align-right">
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