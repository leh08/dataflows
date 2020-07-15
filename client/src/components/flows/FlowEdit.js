import _ from 'lodash';
import React from 'react';
import { compose } from 'redux';
import { connect } from 'react-redux';
import { fetchFlow, editFlow } from '../../actions';
import FlowForm from './FlowForm';

import { Typography } from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';

const useStyles = theme => ({
    root: {
        margin: "15px",
        width: '100%',
        maxWidth: 500,
    },
});

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
        const { classes } = this.props;

        return (
            
            <div className={classes.root}>
                <Typography variant="h5" gutterBottom>
                    Edit a Flow
                </Typography>
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

export default compose(
    connect(
        mapStateToProps,
        { fetchFlow, editFlow }
    ),
    withStyles(useStyles)
)(FlowEdit);