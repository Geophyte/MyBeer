import express from 'express';

import { createReview, getReviews } from '../controllers/reviews.js';
import auth from '../middleware/auth.js';

const router = express.Router();

router.post('/', auth, createReview);
router.get('/', auth, getReviews);





/* router.get('/search', getBeersBySearch);
router.get('/', getBeers);

router.patch('/:id', auth, updateBeer);
router.delete('/:id', auth, deleteBeer);
router.patch('/:id/likeBeer', auth, likeBeer); */

export default router;