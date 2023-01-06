import { combineReducers } from 'redux';

import posts from './beers';
import auth from './auth';

export default combineReducers({ posts, auth });