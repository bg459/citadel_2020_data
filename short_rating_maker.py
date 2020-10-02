#this file will create a short list of rankings with the x movies that have  most ratings

import csv

number_of_movies = 700
min_user_reviews = 10

#counts how many reviews there are from each customer and about each movie. Adds ratings to lst

customer_counts = {}
movie_counts = {}

rating_count = 0

all_ratings = []

print('Getting Data from CSV')
with open('ratings.csv','r') as csvfile: #ADJUST THIS LINE TO YOUR LOCAL FILE LOCATION
    long_file = csv.reader(csvfile)
    headers = next(long_file)
    print(headers)
    for line in long_file:
        all_ratings.append(line)
        if int(line[0]) in customer_counts:
            customer_counts[int(line[0])] += 1
        else:
            customer_counts[int(line[0])] = 1

        if int(line[1]) in movie_counts:
            movie_counts[int(line[1])] += 1
        else:
            movie_counts[int(line[1])] = 1
        rating_count +=1 

#Creates rating set for ratings whose user published more than x reviews
print("Number of Ratings: ", len(all_ratings))
print('Removing reviews from users with small number of ratings')
ratings_sans_low_user = []

for rating in all_ratings:
    if customer_counts[int(rating[0])] >= min_user_reviews:
        ratings_sans_low_user.append(rating)
print("Number of Ratings after removal: ",len(ratings_sans_low_user))
#finds # of reviews of each movie

movie_num_reviews = {}

for rating in ratings_sans_low_user:
    if int(rating[1]) in movie_num_reviews:
        movie_num_reviews[int(rating[1])] += 1
    else:
        movie_num_reviews[int(rating[1])] = 1

#calculates min number of reviews needed to be included
num_movies_included = len(movie_num_reviews)

min_reviews = 2000 #Guess, go with low estimate
adjustment_factor = 1 #higher number will be quicker, lower will yield estimate closer to what you want


movie_num_reviews_intermediate1 = movie_num_reviews
movie_num_reviews_intermediate2 = {}

min_reviews = 10000 #Guess 
adjustment_factor = 50  #goes slower if your estimate is 

print('Finding minimum number of reviews needed to be included')

if (len(movie_num_reviews)) >= number_of_movies:
    while num_movies_included < number_of_movies: 
        print("Started with an overestimate, adjusting by -",adjustment_factor)
        for movie in movie_num_reviews_intermediate1:
            if movie_num_reviews_intermediate1[movie] >= min_reviews:
                movie_num_reviews_intermediate2[int(movie)] = movie_num_reviews_intermediate1[movie]
        num_movies_included = len(movie_num_reviews_intermediate2)
        movie_num_reviews_intermediate1 = movie_num_reviews_intermediate2
        movie_num_reviews_intermediate2 = {}
        min_reviews -= adjustment_factor
    while num_movies_included > number_of_movies: 
        print("Have an underestimate, adjusting by +",adjustment_factor)
        for movie in movie_num_reviews_intermediate1:
            if movie_num_reviews_intermediate1[movie] >= min_reviews:
                movie_num_reviews_intermediate2[int(movie)] = movie_num_reviews_intermediate1[movie]
        num_movies_included = len(movie_num_reviews_intermediate2)
        
        if adjustment_factor > 1:
            if num_movies_included < number_of_movies:
                min_reviews -= adjustment_factor
                for movie in movie_num_reviews_intermediate1:
                    if movie_num_reviews_intermediate1[movie] >= min_reviews:
                        movie_num_reviews_intermediate2[int(movie)] = movie_num_reviews_intermediate1[movie]
                num_movies_included = len(movie_num_reviews_intermediate2)
                adjustment_factor -= 1
                print('Overestimated min number of reviews, adjusting by -',adjustment_factor)
        
        movie_num_reviews_intermediate1 = movie_num_reviews_intermediate2
        movie_num_reviews_intermediate2 = {}
        min_reviews += adjustment_factor
    print(' \n Number of Required Reviews to Be Included', min_reviews)
else:
    print('Minimum number of moviews is greater than number of movies remaining')
    min_reviews = 0

#creates new CSV with desired number of movies

final_ratings = []
for rating in ratings_sans_low_user:
    if movie_num_reviews[int(rating[1])] >= min_reviews:
        final_ratings.append(rating)
print("Number of ratings included: ",len(final_ratings))

print('Removing ratings from users that do not have at least 2 unique ratings')
num_reviews_by_user = {}
intermediate_ratings = []
for rating in final_ratings:
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
for rating in final_ratings:
    if len(num_reviews_by_user[int(rating[0])][1]) < 2:
        continue
    else:
        intermediate_ratings.append(rating)
final_ratings = intermediate_ratings


print('Removing reviews from users with small number of ratings again.')
user_counts2 = {}
for rating in final_ratings:
    if rating[0] in user_counts2:
        user_counts2[rating[0]] +=1
    else:
        user_counts2[rating[0]] = 1
final_final_ratings = []
for rating in final_ratings:
    if user_counts2[rating[0]] >= min_user_reviews:
        final_final_ratings.append(rating)


print('Total reviews:', len(final_final_ratings))
print('Writing to CSV')
with open('short_ratings.csv','w',newline='') as csvfile2:
        short_file = csv.DictWriter(csvfile2, fieldnames=headers)
        short_file.writeheader()
        for line in final_final_ratings:
            short_file.writerow({headers[0]: line[0],headers[1]: line[1],headers[2]: line[2],headers[3]: line[3]})
print('Done')