import React from 'react';
import { compose } from 'redux';
import { connect } from 'react-redux';
import { logIn } from '../../actions';
import AuthForm from './AuthForm';

import { Typography } from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';

const useStyles = theme => ({
    root: {
        margin: "15px",
        width: '100%',
        maxWidth: 500,
    },
});


class LogIn extends React.Component {
    onSubmit = (formProps) => {
        this.props.logIn(formProps);
    }

    render() {
        const { classes } = this.props;

        return (
            <div className={classes.root}>
                <Typography variant="h5" gutterBottom>
                    Log In
                </Typography>
                <AuthForm onSubmit={this.onSubmit} />
            </div>
        );
    }
}

export default compose(
    connect(
        null,
        { logIn }
    ),
    withStyles(useStyles)
)(LogIn);