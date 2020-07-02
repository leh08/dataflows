import React from 'react';
import { connect } from 'react-redux';
import { fetchFlows } from '../../actions';
import { Link } from 'react-router-dom';
import requireAuth from '../requireAuth';

import { Cell, Column, Table } from "@blueprintjs/table";


class FlowList extends React.Component {
    componentDidMount() {
        this.props.fetchFlows()
    }

    renderAdmin(flow) {
        return (
            <div className="right floated content">
                <Link to={`/flows/edit/${flow.id}`} className="ui button primary">
                    Edit
                </Link>
                <Link to={`/flows/delete/${flow.id}`} className="ui button negative">
                    Delete
                </Link>
            </div>
        );
    }

    renderList() {
        return this.props.flows.map(flow => {
            return (
                <div className="item" key={flow.id}>
                    {this.renderAdmin(flow)}
                    <div className="content">
                        <Link to={`/flows/${flow.id}`}>
                            {flow.name}
                        </Link>
                        <div className="description">{flow.report}</div>
                    </div>
                </div>
            );
        });
    }

    renderCreate() {
        if (this.props.isSignedIn) {
            return  (
                <div style={{textAlign: 'right'}}>
                    <Link to="/flows/create" className="ui button primary">Create Flow</Link>
                </div>
            );
        }
    }

    render() {
        return (
            <div>
                <h2 className="bp3-heading">Flows</h2>
                <div className="bp3-button-group">
                    <Link to="/flows/create" className="bp3-button bp3-icon-add">Create Flow</Link>
                    <Link to="/flows/edit" className="bp3-button bp3-icon-edit">Edit</Link>
                    <Link to="/flows/delete" className="bp3-button bp3-icon-trash">Delete</Link>
                    <div className="bp3-button bp3-icon-segmented-control">
                        Status <span class="bp3-icon-standard bp3-icon-caret-down bp3-align-right"></span>
                    </div>
                    <div class="bp3-button bp3-icon-walk">Run</div>
                    <div class="bp3-button bp3-icon-history">Log</div>
                </div>
                <div className="ui celled list">{this.renderList()}</div>
                {this.renderCreate()}
            </div>
            
        );
    }
};

const mapStateToProps = (state) => {
    return { 
        flows: Object.values(state.flows),
        currentUserId: state.auth.userId,
        isSignedIn: state.auth.isSignedIn
    };
};

export default connect(mapStateToProps, { fetchFlows })(requireAuth(FlowList));
