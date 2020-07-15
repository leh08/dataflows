import React from 'react';
import { compose } from 'redux';
import { connect } from 'react-redux';
import { fetchFlows } from '../../actions';
import { Link } from 'react-router-dom';
import requireAuth from '../requireAuth';

import FlowItem from './FlowItem';
import { ButtonGroup, Button, TableContainer, Paper, Table, TableHead, TableRow, TableCell, TableBody } from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';

const useStyles = theme => ({
    table: {
        minWidth: 650,
    },
});


class FlowList extends React.Component {
    state = { selectedFlow: null };

    componentDidMount() {
        this.props.fetchFlows()
    }

    onFlowSelect = (flow) => {
        this.setState({ selectedFlow: flow });
    };

    renderAdmin(flow) {
        if (this.state.selectedFlow) {
            return (
                <ButtonGroup>
                    <Button component={ Link } to={`/flows/edit/${this.state.selectedFlow.id}`}>Edit</Button>
                    <Button component={ Link } to={`/flows/delete/${this.state.selectedFlow.id}`}>Delete</Button>
                </ButtonGroup>
            );
        }
        return (
            <ButtonGroup>
                <Button disabled>Edit</Button>
                <Button disabled>Delete</Button>
            </ButtonGroup>
        );
    }

    renderList() {
        const { classes } = this.props;
        return (
            <TableContainer component={Paper}>
                <Table className={classes.table} aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell>ID</TableCell>
                        <TableCell>Name</TableCell>
                        <TableCell>Report</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {
                        this.props.flows.map(flow => {
                            return <FlowItem onFlowSelect={this.onFlowSelect} flow={flow} key={flow.id} />})
                    }
                </TableBody>
                </Table>
            </TableContainer>
        );
    }

    render() {
        return (
            <div>
                <ButtonGroup aria-label="outlined primary button group">
                    <Button component={ Link } to="/flows/create">Create Flow</Button>
                    {this.renderAdmin()}
                </ButtonGroup>
                {this.renderList()}
            </div>
        );
    }
};

const mapStateToProps = (state) => {
    return { 
        flows: Object.values(state.flows),
        currentUserId: state.auth.userId,
        isSignedIn: state.auth.isSignedIn,
    };
};

export default compose(
    connect(mapStateToProps, { fetchFlows }),
    requireAuth,
    withStyles(useStyles)
)(FlowList);
