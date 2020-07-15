import React from 'react';
import { compose } from 'redux';
import { connect } from 'react-redux';
import { signUp } from '../../actions';
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


class SignUp extends React.Component {
    onSubmit = (formProps) => {
        this.props.signUp(formProps);
    }

    render() {
        const { classes } = this.props;

        return (
            <div className={classes.root}>
                <Typography variant="h5" gutterBottom>
                    Sign Up
                </Typography>
                <AuthForm onSubmit={this.onSubmit} />
            </div>
        );
    }
}

export default compose(
    connect(
        null,
        { signUp }
    ),
    withStyles(useStyles)
)(SignUp);