import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import Modal from '../Modal';
import history from '../../history';
import { fetchFlow, deleteFlow } from '../../actions';


class FlowDelete extends React.Component {
    componentDidMount() {
        this.props.fetchFlow(this.props.match.params.id);
    }

    renderActions() {
        const { id } = this.props.match.params

        return (
            <React.Fragment>
                <button 
                    onClick={() => this.props.deleteFlow(id) } 
                    className="ui button negative"
                >
                    Delete
                </button>
                <Link to='/' className="ui button">Cancel</Link>
            </React.Fragment>
        );
    }

    renderContent() {
        if (!this.props.flow) {
            return 'Are you sure you want to delete this flow?'
        }

        return `Are you sure you want to delete this flow with name: ${this.props.flow.name}?`
    }

    render () {
        return (
            <Modal 
                header="Delete Flow"
                content={this.renderContent()}
                actions={this.renderActions()}
                onDismiss= {() => history.push("/")}
            />
        );
    }
}

const mapStateToProps = (state, ownProps) =>{
    return { flow: state.flows[ownProps.match.params.id] };
};

export default connect(mapStateToProps, { fetchFlow, deleteFlow })(FlowDelete);