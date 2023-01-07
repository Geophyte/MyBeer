import mongoose from 'mongoose';

const reviewSchema = mongoose.Schema({
    title: String,
    message: String,
    name: String,
    creator: String,
    beer: String,
    createdAt: {
        type: Date,
        default: new Date()
    }
});

const Review = mongoose.model('Review', reviewSchema);

export default Review;