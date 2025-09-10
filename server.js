const mongoose = require('mongoose');
mongoose.connect('mongodb://localhost:27017/messfeed', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});
