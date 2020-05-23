import { combineReducers } from 'redux';
import { reducer as formReducer } from 'redux-form';
import authReducer from './authReducer';
import flowReducer from './flowReducer';

export default combineReducers({
    auth: authReducer,
    form: formReducer,
    flows: flowReducer,
});