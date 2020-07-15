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
    const [parser, setParser] = React.useState('Pandas');

    const handleChange = (event) => {
        setParser(event.target.value);
    };

    return (
        <FormControl className={classes.formControl}>
            <InputLabel id="demo-simple-select-label">Choose Parser</InputLabel>
            <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                value={parser}
                onChange={handleChange}
            >
                <MenuItem value="Pandas">Pandas</MenuItem>
            </Select>
        </FormControl>
    );
};
  