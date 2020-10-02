#adds ranking to ratings csv. Ranking is on a scale from 0-1, 0 being the lowest and 1 being the highest

import csv

#reads in data ot a lst of lsts
ratings = []

with open('short_ratings.csv','r') as csvfile:
    file = csv.reader(csvfile)
    headers = next(file)
    for line in file:
        userID = int(line[0])
        movieID = int(line[1])
        rating = float(line[2])
        time = line[3]
        ratings.append([userID,movieID,rating,time])

#counts number of independent ratings for each user

#each dict will use the UserID as a key, then it will be a lst of a number of ratings & lst of each indiviudal rating
num_reviews_by_user = {}

for rating in ratings:
    userID = int(rating[0])
    value = float(rating[2])
    if userID in num_reviews_by_user:
        num_reviews_by_user[userID][0] += 1
        if value in num_reviews_by_user[userID][1]:
            continue
        else:
            num_reviews_by_user[userID][1].append(value)
    else:
        num_reviews_by_user[userID] = [1,[value]]
#finds rating -> ranking scores
review_dict_all = {}
for user in num_reviews_by_user:
    ID = user
    review_count = num_reviews_by_user[user][1][0]
    different_score_count = len(num_reviews_by_user[user][1])
    unique_scores = num_reviews_by_user[user][1]
    unique_scores.sort()
    rating_dict = {}
    rating_dict[unique_scores[0]] = 0
    rating_dict[unique_scores[len(unique_scores) - 1]] = 1
    n = len(unique_scores) - 1
    step = 1/n
    rank = step
    for i in range(len(unique_scores)-2):
        i = i+1
        rating_dict[unique_scores[i]] = rank
        rank += step
    review_dict_all[ID] = rating_dict

headers.append('Ranking')
with open('short_ratings_rankings.csv','w',newline='') as csvfile2:
        short_file = csv.DictWriter(csvfile2, fieldnames=headers)
        short_file.writeheader()
        for line in ratings:
            rating = review_dict_all[int(line[0])][float(line[2])]
            short_file.writerow({headers[0]: line[0],headers[1]: line[1],headers[2]: line[2],headers[3]: line[3], headers[4]:rating})