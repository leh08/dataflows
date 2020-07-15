import React from 'react';
import { TableRow, TableCell } from '@material-ui/core';

const FlowItem = ({ flow, onFlowSelect }) => {
    return (
        <TableRow onClick={() => onFlowSelect(flow)}>
            <TableCell component="th" scope="row">
                {flow.id}
            </TableCell>
            <TableCell>{flow.name}</TableCell>
            <TableCell>{flow.report}</TableCell>
        </TableRow>
    );
};

export default FlowItem;
