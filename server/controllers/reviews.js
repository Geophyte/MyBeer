import mongoose from "mongoose";
import Review from "../models/review.js";

/* export const getBeers = async (req, res) => {
    const { page } = req.query;

    try {
        const LIMIT = 8;
        const startIndex = (Number(page) -1)*LIMIT; // startIndex of every page
        const total = await Beer.countDocuments({});

        const beers = await Beer.find().sort({ _id: -1 }).limit(LIMIT).skip(startIndex);

        res.status(200).json({ data: beers, currentPage: Number(page), numberOfPages: Math.ceil(total/LIMIT) });
    } catch (error) {
        res.status(404).json({ message: error.message });
    }
}

 */

export const getReviews = async (req, res) => {
    //const { searchQuery, categories } = req.query

    try {
        //const title = new RegExp(searchQuery, 'i'); // ignore size of letters (Test=TEST=TeST)

        const reviews = await Review.find();
        console.log(reviews)

        res.json({ data: reviews });
    } catch (error) {
        res.status(404).json({ message: error.message });
    }
}

export const createReview = async (req, res) => {
    const review = req.body;
    console.log("dodawanie dzaiła")

    const newReview = new Review({ ...review, creator: req.userId, createdAt: new Date().toISOString() });
    try {
        await newReview.save();

        res.status(201).json(newReview);
    } catch (error) {
        res.status(409).json({message: error.message });
    }
}

export const updateReview = async (req, res) => {
    const { id: _id } = req.params;
    const review = req.body;

    if(!mongoose.Types.ObjectId.isValid(_id)) return res.status(404).send('No review with that id');

    const updatedReview = await review.findByIdAndUpdate(_id, { ...review, _id }, { new: true });
    
    res.json(updatedReview);
}

export const deleteReview = async (req, res) => {
    const { id } = req.params;

    if(!mongoose.Types.ObjectId.isValid(id)) return res.status(404).send('No review with that id');

    await Review.findByIdAndDelete(id);

    res.json({ message: 'review deleted successfully' });
}