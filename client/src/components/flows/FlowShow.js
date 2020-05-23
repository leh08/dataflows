import React from 'react';
import { connect } from 'react-redux';
import { fetchFlow } from '../../actions';

class FlowShow extends React.Component {
    componentDidMount() {
        this.props.fetchFlow(this.props.match.params.id)
    }

    render() {
        if (!this.props.flow) {
            return <div>Loading...</div>
        }

        const { name, report } = this.props.flow

        return (
            <div>
                <h1>{name}</h1>
                <h5>{report}</h5>
            </div>
        );
    };
};

const mapStateToProps = (state, ownProps) => {
    return { flow: state.flows[ownProps.match.params.id] }
};

export default connect(mapStateToProps, { fetchFlow })(FlowShow);