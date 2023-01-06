import { FETCH_ALL, CREATE, UPDATE, DELETE, FETCH_BY_SEARCH, START_LOADING, END_LOADING, LIKE } from '../constants/actionTypes';

const beersReducer =  (state = { isLoading: true, beers: [] }, action) => {
    switch (action.type) {
        case START_LOADING:
            return {
                ...state,
                isLoading: true
            };
        case END_LOADING:
            return {
                ...state,
                isLoading: false
            };
        case FETCH_ALL:
            return {
                ...state,
                beers: action.payload.data,
                currentPage: action.payload.currentPage,
                numberOfPages: action.payload.numberOfPages
            }
        case FETCH_BY_SEARCH:
            return {
                ...state,
                beers: action.payload.data,
            }
        case LIKE:
            return { ...state, beers: state.beers.map((beer) => (beer._id === action.payload._id ? action.payload : beer)) };
        case CREATE:
            return { ...state, beers: [...state.beers, action.payload] };
        case UPDATE:
            return { ...state, beers: state.beers.map((beer) => (beer._id === action.payload._id ? action.payload : beer)) };
        case DELETE:
            return { ...state, beers: state.beers.filter((beer) => beer._id !== action.payload) };
        default:
            return state;
    }
};

export default beersReducer;