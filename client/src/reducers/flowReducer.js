import _ from 'lodash';
import { 
    CREATE_FLOW,
    FETCH_FLOWS,
    FETCH_FLOW,
    DELETE_FLOW,
    EDIT_FLOW,
} from "../actions/types";

export default (state = {}, action) => {
    switch (action.type) {
        case FETCH_FLOWS:
            return { ...state, ..._.mapKeys(action.payload.flows, 'id') };

        case FETCH_FLOW:
            return { ...state, [action.payload.id]: action.payload };

        case CREATE_FLOW:
            return { ...state, [action.payload.id]: action.payload };

        case EDIT_FLOW:
            return { ...state, [action.payload.id]: action.payload };

        case DELETE_FLOW:
            return _.omit(state, action.payload);

        default:
            return state;
    }
};