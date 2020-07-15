import _ from 'lodash';
import { 
    FETCH_SOURCES,
} from "../actions/types";

export default (state = {}, action) => {
    switch (action.type) {
        case FETCH_SOURCES:
            return { ...state, ..._.mapKeys(action.payload.sources, 'name') };

        default:
            return state;
    }
};