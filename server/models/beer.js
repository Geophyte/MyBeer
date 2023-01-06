import mongoose from 'mongoose';

const beerSchema = mongoose.Schema({
    title: String,
    message: String,
    name: String,
    creator: String,
    categories: [String],
    selectedFile: String,
    likes: {
        type: [String],
        default: []
    },
    createdAt: {
        type: Date,
        default: new Date()
    }
});

const Beer = mongoose.model('Beer', beerSchema);

export default Beer;