import model
from model import User, Movie, Rating, session
import csv
from datetime import datetime

def load_users(session):
    with open('seed_data/u.user', 'rb') as csvfile:
        userreader = csv.reader(csvfile, delimiter = '|')
        for userrow in userreader:
            u = User() 
            u.id = userrow[0]
            u.age = userrow[1]
            u.gender = userrow[2]
            u.occupation = userrow[3]
            u.zipcode = userrow[4]
            u.email = None
            u.password = None

            session.add(u)




# def load_movies(session):
#     with open('seed_data/u.item', 'rb') as csvfile:
        
#         moviereader = csv.reader(csvfile, delimiter = '|')
#         # moviereader = csv.Sniffer().sniff(csvfile.read(), delimiters='|')
#         for movierow in moviereader:
#             m = Movie()
#             m.id = movierow[0].decode("latin-1")
#             m.name = movierow[1][:-7].decode("latin-1")
#             m.released_at = movierow[2]
#             empty = [None,'',""," "]
#             if m.released_at not in empty:
#                 m.released_at = datetime.strptime(m.released_at, '%d-%b-%Y')
#             else:
#                 m.released_at = datetime.strptime("01-Jan-1900", '%d-%b-%Y')
#             m.imbd_url = movierow[4].decode("latin-1")

#             session.add(m)





    #         movie id | movie title | release date | video release date |
    #           IMDb URL | unknown | Action | Adventure | Animation |
    #           Children's | Comedy | Crime | Documentary | Drama | Fantasy |
    #           Film-Noir | Horror | Musical | Mystery | Romance | Sci-Fi |
    #           Thriller | War | Western |

    # pass

# def load_ratings(session):
#     with open('seed_data/u.data', 'rb') as csvfile:
#         ratingsreader = csv.reader(csvfile, delimiter = "\t")
#         for ratingrow in ratingsreader:
#             r = Rating()
#             r.id = None
#             r.user_id = ratingrow[0]
#             r.movie_id = ratingrow[1]
#             r.rating = ratingrow[2]

#             session.add(r)



def main(session):
    load_users(session)
    # load_movies(session)
    # load_ratings(session)

    session.commit()

if __name__ == "__main__":
    s= model.session
    main(s)
