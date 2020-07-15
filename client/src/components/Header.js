import React from 'react';
import {compose } from 'redux';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { AppBar, Toolbar, Tabs, Tab, IconButton, Button } from '@material-ui/core';
import MenuIcon from '@material-ui/icons/Menu';
import { withStyles } from '@material-ui/core/styles';

const useStyles = theme => ({
    root: {
        flexGrow: 1,
      },
    menuButton: {
        marginRight: theme.spacing(2),
    },
    logo: {
        width: 100,
        height: 50,
    },
    tabs: {
        flexGrow: 1,
    },
});


class Header extends React.Component { 
    state = { value: 0 }

    renderAuth() {
        if (this.props.isSignedIn) {
            return (
                <Button color="inherit" component={ Link } to="/logout">Log Out</Button>
            );
        } else {
            return (
                <React.Fragment>
                    <Button color="inherit" component={ Link } to="/signup">Sign Up</Button>
                    <Button color="inherit" component={ Link } to="/login">Log In</Button>
                </React.Fragment>
            );
        }
    }

    a11yProps(index) {
        return {
          id: `simple-tab-${index}`,
          'aria-controls': `simple-tabpanel-${index}`,
        };
    }

    handleChange = (event, newValue) => {
        this.setState({ value: newValue });
    };
    
    render() { 
        const { classes } = this.props;   

        return (
            <div className={classes.root}>
                <AppBar position="static">
                    <Toolbar>
                        <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu">
                            <MenuIcon />
                        </IconButton>
                        <Tabs value={this.state.value} onChange={this.handleChange} aria-label="simple tabs example" className={classes.tabs}>
                            <Tab label="Home" component={ Link } to="/" color="inherit" {...this.a11yProps(0)}/>
                            <Tab label="Visualize" component={ Link } to="/flows" color="inherit" {...this.a11yProps(1)}/>
                            <Tab label="Analyze" component={ Link } to="/flows" color="inherit" {...this.a11yProps(2)}/>
                            <Tab label="Flow" component={ Link } to="/flows" color="inherit" {...this.a11yProps(3)}/>
                        </Tabs>
                        {this.renderAuth()}
                    </Toolbar>
                </AppBar>
            </div>
        );
    }
}

function mapStateToProps(state) {
    return { isSignedIn: state.auth.isSignedIn, };
}

export default compose(
    connect(mapStateToProps),
    withStyles(useStyles)  
)(Header);