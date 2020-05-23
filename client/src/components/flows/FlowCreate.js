import React from 'react';
import { connect } from 'react-redux';
import { createFlow } from '../../actions';
import FlowForm from './FlowForm';


class FlowCreate extends React.Component {
    onSubmit = (formValues) => {
        this.props.createFlow(formValues);
    }

    render() {
        return (
            <div>
                <h3>Create a Flow</h3>
                <FlowForm onSubmit={this.onSubmit} />
            </div>
        );
    }
}

export default connect(
    null,
    { createFlow }
)(FlowCreate);