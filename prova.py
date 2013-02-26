from imdb import IMDb
ia = IMDb()



for person in ia.search_person('Mel Gibson'):
    print person.personID, person['name']