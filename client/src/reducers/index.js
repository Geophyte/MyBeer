import { combineReducers } from 'redux';

import beers from './beers';
import auth from './auth';
import reviews from './reviews';

export default combineReducers({ beers, auth, reviews });