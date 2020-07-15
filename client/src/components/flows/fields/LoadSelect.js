import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

const useStyles = makeStyles((theme) => ({
  formControl: {
        margin: theme.spacing(1.25),
        width: 450,
  },
}));

export default function SimpleSelect() {
    const classes = useStyles();
    const [loadMode, setLoadMode] = React.useState('Append');

    const handleChange = (event) => {
        setLoadMode(event.target.value);
    };

    return (
        <FormControl className={classes.formControl}>
            <InputLabel id="demo-simple-select-label">Choose Load Mode</InputLabel>
            <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                value={loadMode}
                onChange={handleChange}
            >
                <MenuItem value="Append">Append</MenuItem>
                <MenuItem value="Replace">Replace</MenuItem>
            </Select>
        </FormControl>
    );
};
  