import pymongo
from decouple import config
from pymongo import MongoClient
import re

mongo_con = config('MONGO_CLIENT')


class Mongo:
    def __init__(self):
        self.cluster = MongoClient(mongo_con)
        self.regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    def find_email(self, email: str):
        db = self.cluster["weatherapp"]
        collection = db["emails"]
        results = collection.find_one({"email": f"{email}"})
        try:
            ls = results['email']
            return ls
        except:
            ls = 'Not found!!'
            return ls

    def post_email(self, email: str, loc: str):
        post = {"email": email, "location": loc}
        db = self.cluster["weatherapp"]
        collection = db["emails"]
        try:
            collection.insert_one(post)
            return 'Added!!'
        except:
            return 'Some error occurred !!'

    def get_all_content(self):
        db = self.cluster["weatherapp"]
        collection = db["emails"]
        results = collection.find({})
        return results

    def check_email(self, email: str):
        if re.fullmatch(self.regex, email):
            return 'Valid Email'
        else:
            return 'Invalid Email'


def main():
    mongoemail = Mongo()

    results = mongoemail.find_email("adesh.senapati10@gmail.com")
    #mongoemail.post_email(post)

    print(results)


if __name__ == "__main__":
    main()


