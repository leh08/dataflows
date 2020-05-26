import React from 'react';
import { compose } from 'redux';
import { connect } from 'react-redux';
import { Field, reduxForm } from 'redux-form';
import flows from '../../apis/flows';
import { logIn, logOut } from '../../actions';


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

    renderError(error) {
        return (
            <div className="ui error message">
                <div className="header">{error}</div>
            </div>
        );
    }

    renderInput = ({ input, label, type, autoComplete, meta }) => {
        const className = `field ${meta.error && meta.touched ? 'error': ''}`
        return (
            <div className={className}>
                <label>{label}</label>
                <input {...input} type={type} autoComplete={autoComplete}/>
                {(meta.touched && meta.error) ? this.renderError(meta.error): ""}
            </div>
        );
    }

    onSubmit = (formProps) => {
        this.props.onSubmit(formProps);
    }

    render() {
        const { handleSubmit } = this.props;
        return (
            <form onSubmit={handleSubmit(this.onSubmit)} className="ui form error">
                <Field
                    name="email"
                    component={this.renderInput}
                    type="text"
                    label="Email"
                    autoComplete="on"
                />
                <Field
                    name="password"
                    type="password"
                    component={this.renderInput}
                    label="Password"
                    autoComplete="off"
                />
                {(this.props.errorMessage) ? this.renderError(this.props.errorMessage): ""}
                <button className="ui button primary">Submit</button>
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
    reduxForm({ form: 'authForm', validate })
)(AuthForm);