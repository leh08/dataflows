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
    const [store, setStore] = React.useState('Redshift');

    const handleChange = (event) => {
        setStore(event.target.value);
    };

    return (
        <FormControl className={classes.formControl}>
            <InputLabel id="demo-simple-select-label">Choose Store</InputLabel>
            <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                value={store}
                onChange={handleChange}
            >
                <MenuItem value="Redshift">Redshift</MenuItem>
            </Select>
        </FormControl>
    );
};
  