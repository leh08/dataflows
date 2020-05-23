import _ from 'lodash';
import React from 'react';
import { connect } from 'react-redux';
import { fetchFlow, editFlow } from '../../actions';
import FlowForm from './FlowForm';


class FlowEdit extends React.Component {
    componentDidMount() {
        this.props.fetchFlow(this.props.match.params.id);
    }

    onSubmit = (formValues) => {
        this.props.editFlow(this.props.match.params.id, formValues)
    };

    render() {
        if (!this.props.flow) {
            return <div>Loading</div>;
        }
        
        return (
            <div>
                <h3>Edit a Flow</h3>
                <FlowForm
                    initialValues={_.pick(this.props.flow, 'name', 'report')}
                    onSubmit={this.onSubmit}
                />
            </div>
        );
    }
}

const mapStateToProps = (state, ownProps) => {
    return { flow: state.flows[ownProps.match.params.id] };
};

export default connect(
    mapStateToProps,
    { fetchFlow, editFlow }
)(FlowEdit);