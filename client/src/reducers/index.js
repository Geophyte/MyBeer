import { combineReducers } from 'redux';

import beers from './beers';
import auth from './auth';

export default combineReducers({ beers, auth });