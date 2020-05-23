import React from 'react';
import { connect } from 'react-redux';
import { signUp } from '../../actions';
import AuthForm from './AuthForm';


class SignUp extends React.Component {
    onSubmit = (formProps) => {
        this.props.signUp(formProps);
    }

    render() {
        return (
            <div>
                <h3>Sign Up</h3>
                <AuthForm onSubmit={this.onSubmit} />
            </div>
        );
    }
}

export default connect(null, { signUp } )(SignUp);