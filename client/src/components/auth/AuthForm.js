import React from 'react';
import { compose } from 'redux';
import { connect } from 'react-redux';
import { Field, reduxForm } from 'redux-form';
import flows from '../../apis/flows';
import { logIn, logOut } from '../../actions';

import { TextField, Button } from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';

const useStyles = theme => ({
    root: {
        '& .MuiTextField-root': {
          margin: theme.spacing(1.25),
          width: 450,
        },
    },
});


class AuthForm extends React.Component {
    componentDidMount() {
        try {
            flows.get('/user', { headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.props.accessToken}`
            } })
        } catch {
            flows.post('/refresh', { headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.props.refreshToken}`
            } }).then(response => console.log(response.data))
        }
    }

    onAuthChange = (isSignedIn) => {
        if (isSignedIn) {
            this.props.logIn(this.auth.currentUser.get().getId());
        } else {
            this.props.logOut();
        }
    }

    renderInput = ({ input, type, label, meta }) => {
        if (meta.error && meta.touched) {
            return (
                <div>
                    <TextField error helperText={meta.error} id="standard-error-helper-text" type={type} label={label} {...input} />
                </div>
            );
        } else {
            return (
                <div>
                    <TextField id="standard-basic" type={type} label={label} {...input} />
                </div>
            );
        }
    }

    onSubmit = (formProps) => {
        this.props.onSubmit(formProps);
    }

    render() {
        const { classes, handleSubmit } = this.props;

        return (
            <form onSubmit={handleSubmit(this.onSubmit)} className={classes.root} noValidate>
                <Field
                    name="email"
                    component={this.renderInput}
                    type="text"
                    label="Email"
                />
                <Field
                    name="password"
                    type="password"
                    component={this.renderInput}
                    label="Password"
                />
                <Button type="submit" variant="contained" size="large" color="primary">
                    Submit
                </Button>
            </form>
        );
    }
}

const validate = (formValues) => {
    const errors = {};
    if (!formValues.email) {
        errors.email = "You must enter an email"
    }
    
    if (!formValues.password) {
        errors.password = "You must enter a password"
    }

    return errors
};

function mapStateToProps(state) {
    return { errorMessage: state.auth.errorMessage, accessToken: state.auth.accessToken, refreshToken: state.auth.refreshToken }
}

export default compose(
    connect(mapStateToProps , { logIn, logOut }),
    reduxForm({ form: 'authForm', validate }),
    withStyles(useStyles)
)(AuthForm);