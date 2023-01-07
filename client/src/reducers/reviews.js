import { FETCH_ALL, CREATE, UPDATE, DELETE, FETCH_BY_SEARCH, START_LOADING, END_LOADING, LIKE } from '../constants/actionTypes';

const reviewsReducer =  (state = { isLoading: true, reviews: [] }, action) => {
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
                reviews: action.payload.data,
                currentPage: action.payload.currentPage,
                numberOfPages: action.payload.numberOfPages
            }
        case FETCH_BY_SEARCH:
            return {
                ...state,
                reviews: action.payload.data,
            }
        case LIKE:
            return { ...state, reviews: state.reviews.map((beer) => (beer._id === action.payload._id ? action.payload : beer)) };
        case CREATE:
            return { ...state, reviews: [...state.reviews, action.payload] };
        case UPDATE:
            return { ...state, reviews: state.reviews.map((beer) => (beer._id === action.payload._id ? action.payload : beer)) };
        case DELETE:
            return { ...state, reviews: state.reviews.filter((beer) => beer._id !== action.payload) };
        default:
            return state;
    }
};

export default reviewsReducer;