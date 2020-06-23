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
            <nav class="bp3-navbar">
                <div style={{margin: '0 auto'}}>
                    <div class="bp3-navbar-group bp3-align-left">
                        <Link to="/" className="bp3-button bp3-minimal bp3-navbar-heading">
                            Data Warehouse
                        </Link>
                        <span class="bp3-navbar-divider"></span>
                        <Link to="/flows" className="bp3-button bp3-minimal bp3-navbar-heading">
                            Flow
                        </Link>
                    </div>
                    <div class="bp3-navbar-group bp3-align-right">
                        {this.renderAuth()}
                    </div>
                </div>
            </nav>
        );
    }
}

function mapStateToProps(state) {
    return { isSignedIn: state.auth.isSignedIn, };
}

export default connect(mapStateToProps)(Header);