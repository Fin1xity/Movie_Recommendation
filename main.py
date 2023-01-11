import pygame as pg
import pygame.freetype
import numpy as np
import pandas as pd
import difflib 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def main():
    screen = pg.display.set_mode((374, 466))
    font = pg.font.Font("Resources\\Modeseven-L3n5.ttf", 20)
    clock = pg.time.Clock()
    pg.display.set_caption('Movie Recommendation')
    icon = pg.image.load("Resources\\logo2.png")
    pg.display.set_icon(icon)
    input_box = pg.Rect(90, 370, 100, 27)
    color_inactive = pg.Color('#212325')
    color_active = pg.Color('#ABABAB')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                
                if input_box.collidepoint(event.pos):
                
                    active = not active
                else:
                    active = False
              
                color = color_active if active else color_inactive
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        #text = ''
                        return text
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        bg_color = pg.image.load("Resources\\gii1.png")
        screen.blit(bg_color,(0,0))
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pg.draw.rect(screen, color, input_box, 2)
        pg.display.flip()
        clock.tick(30)

        



def prin(text=''):
    pg.init()
    screen = pg.display.set_mode((374, 466))
    font2= pygame.freetype.Font("Resources\\Modeseven-L3n5.ttf", 13)
    pg.display.set_caption('Movie Recommendation')
    icon = pg.image.load("Resources\\logo2.png")
    pg.display.set_icon(icon)
    running =  True
    a = text
    
    movies_data = pd.read_csv("Resources\\movies.csv")
    selected_features = ['genres','keywords','tagline','cast','director']
    for feature in selected_features:
        movies_data[feature] = movies_data[feature].fillna('')
    combined_features = movies_data['genres']+' '+movies_data['keywords']+' '+movies_data['tagline']+' '+movies_data['cast']+' '+movies_data['director']
    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(combined_features)
    similarity = cosine_similarity(feature_vectors)
    name_list = movies_data['title'].tolist()
    close_match = difflib.get_close_matches(a,name_list)
    close = close_match[0]
    index_of_movie = movies_data[movies_data.title == close]['index'].values[0]
    similarity_score = list(enumerate(similarity[index_of_movie]))
    sorted_simmilar_movies = sorted(similarity_score,key = lambda x:x[1], reverse = True)
    i = 1
    d = ["1.","2.","3.","4.","5.","6.","7.","8.","9.","10."]
    len = 10
    loc = 135
    x = 50
    screen.fill((255,255,255))
    bg_color = pg.image.load("Resources\\yui2.png")
    screen.blit(bg_color,(0,0))
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            else:
                for movie in sorted_simmilar_movies:
                    index = movie[0]
                    title_from_index = movies_data[movies_data.index==index]['title'].values[0]
                    if (i<=10):
                        #print(i, '.',title_from_index)
                        text_surface, rect = font2.render(d[i-1], "#FFDD64")
                        screen.blit(text_surface, (x, loc))
                        text_surface, rect = font2.render(title_from_index, "#FFDD64")
                        screen.blit(text_surface, (x+25, loc))
                        loc = loc+25
                        i+=1
        
        pg.display.flip()






if __name__ == '__main__':
    pg.init()
    a = main()
    prin(a)
    pg.quit()