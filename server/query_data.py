from server.models import UserRatings

data = [mr.make_list() for mr in UserRatings.query.all()]

print(data)