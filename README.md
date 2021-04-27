# :white_check_mark:The Forum Filter:negative_squared_cross_mark:

## About Project
Project aim is to create a tool that recognizes **toxic behaviour** in any given comment.
Tool is built as an AI that evaluates input based on experience gained from database it was trained on. 
## Database
Data used in teaching our AI comes from a competition on Kaggle:\
:point_down::point_down::point_down:\
[Toxic Comment Classification Challenge](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/overview)\
\
Database is made of 160 000 comments from Wikipedia that were evaluated by humans as toxic or non-toxic.
Around 10% of those records are marked as toxic.

## Implemented Systems
1. At first we extract each word in our database and adjust a proper numeric value based on frequency of this word in toxic comments.
2. Based on numeric values we now calculate the toxicity levels of given text/comment. Those values are calculated globally throughout the whole comment and locally in small groups.
With those values prepared we make a decision whether the text is toxic or not.
3. To get the best results we implemented a heuristic algorithm. With this algorithm we can look for the most optimal thresholds for decision making.

## File Preview

 `PrepareDB.py` is a script that changes `Comments.csv` database into the `Dictionary.csv` with proper toxicity levels  
 \
 `CalculateToxicity.py` is our tool that calculates the toxicity of given text and return decision: `TOXIC` or `NON-TOXIC`\
 \
 `TrainDB.py` uses smaller (1000 records) database `toxicBoardToTraining.csv` to find optimal threshold for decision made in `CalculateToxicity.py`\
 \
 `Comments.csv` core database, consists of comment of different lenght. Those comments are evaluated whether they are toxic. \
 \
 `Dictionary.csv` is a database prepared by us. It consists of a list of word with their correct toxicity level.

## Roadmap

- [x] **Start** 
- [x] **PrepareDB**
- [x] **CalculateToxicity** 
- [x] **TrainDB** 
- [ ] **GUI**  :point_left: *We are currently working on this*
- [ ] **Speech-to-text**
- [ ] **Finish**
