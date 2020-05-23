import React from 'react';
import { connect } from 'react-redux';
import { logIn } from '../../actions';
import AuthForm from './AuthForm';


class LogIn extends React.Component {
    onSubmit = (formProps) => {
        this.props.logIn(formProps);
    }

    render() {
        return (
            <div>
                <h3>Log In</h3>
                <AuthForm onSubmit={this.onSubmit} />
            </div>
        );
    }
}

export default connect(null, { logIn } )(LogIn);