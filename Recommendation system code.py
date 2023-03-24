##Upload and Reading Dataset
import pandas as pd

movies = pd.read_csv('D:\\DataSets\\movies.csv')
movies.head(2)

#movies.info()



###Dropping not required columns
required_columns =['title','original_title', 'tagline', 'keywords', 'overview', 'genres', 'cast', 'director']
movies = movies[required_columns]
movies.isna().sum()


movies.fillna(' ', inplace=True)
movies.isna().sum()


#movies.iloc[1]



###Create movie CONTENT
movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['director'] = movies['director'].apply(lambda x: x.replace(" ","") )


##Converting List to Strings
movies['genres'] = movies['genres'].apply(lambda x: ','.join(map(str, x)))
movies['keywords'] = movies['keywords'].apply(lambda x: ','.join(map(str, x)))
movies['cast'] = movies['cast'].apply(lambda x: ','.join(map(str, x)))


movies['content'] = movies['title'] + ' ' + movies['overview'] + ' ' + movies['keywords'] + ' ' + movies['cast'] + ' ' + movies ['director']
movies['content']



###Natural Language Processing
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(max_features=1000)
movie_vectors = vectorizer.fit_transform(movies['content'].values) 



###Cosine Similarity
from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(movie_vectors)

similarity_df = pd.DataFrame(similarity)
#similarity_df


from tkinter import *

def show_data():
    txt.delete(0.0, 'end')
    moviee = ent.get()

    movies_index = movies[movies['title'] == moviee].index[0]    
    distances = similarity[movies_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    i=0
    j=0
    List = [None]*10
    for element in movies_list:
        s = movies.iloc[element[0]].title
        List[j] = s
        j+=1

        if i>=10:
            break
    
    for x in range(len(movies_list)-1,-1,-1):
        t="\n"
        txt.insert(0.0, List[x])
        txt.insert(0.0,t)

    movies.title.head(10)



root = Tk()
root.geometry("410x300")


l1 = Label(root, text="Enter a Movie Name: ")
l2 = Label(root, text="Top Ten Suggestions for you: ")

ent = Entry(root)

l1.grid(row=0)
l2.grid(row=2)

ent.grid(row=0, column=1)

txt = Text(root, width=50, height=13, wrap=WORD)
txt.grid(row=3, columnspan=2, sticky=W)

bttn = Button(root, text="Search", bg="purple", fg="white", command=show_data)
bttn.grid(row=1, columnspan=2)
root.mainloop()
