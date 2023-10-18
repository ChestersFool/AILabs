import math
import random
from tkinter import *


def get_x_and_y(event):
    global lasx, lasy
    lasx, lasy = event.x, event.y


def draw_smth(event):
    global lasx, lasy
    canvas.create_oval(event.x - 3, event.y - 3, event.x + 3, event.y + 3, fill='black')
    # canvas.create_line(lasx, lasy, event.x, event.y, width=5)
    lasx, lasy = event.x, event.y


def read_vectors_file():
    # read the file
    f = open("models.txt", "r")
    i = 0

    for line in f:
        vector = line.split(' ')
        digit = vector.pop(len(vector) - 1).replace('\n', '')
        vectors_from_file[i] = [vector, float(digit)]
        i = i + 1

    f.close()
    # print("\n\n", vectors)


def write_vector_file():
    read_vector_canvas()

    digit = text.get("1.0", "end-1c")

    # write to the file
    f = open("models.txt", "a")
    f.write(' '.join(map(str, vector_normalized)))
    f.write(' ' + digit + '\n')
    f.close()

    vectors_from_file[random.randint(2000, 10000)] = [vector_normalized, digit]


def read_vector_canvas():
    pixels_color_matrix = get_matrix_pixels()
    vector = []

    for i in range(int(canvas_height / segment_height)):
        for j in range(int(canvas_width / segment_width)):
            vector.append(get_segment(pixels_color_matrix, i, j))

    print("canvas vector: ", vector)

    # vector_normalized = []
    max_vec = max(vector)
    vector_normalized.clear()

    for elem in vector:
        vector_normalized.append(elem / max_vec)

    print("canvas normalized vector: ", vector_normalized)


def get_matrix_pixels():
    pixels_color_matrix = []
    for i in range(canvas_height):
        pixels_color_array = []
        for j in range(canvas_width):
            color = get_pixel_color(j, i)
            if color == 'white':
                color = 0
            else:
                color = 1
            pixels_color_array.append(color)
            # print(color, end="")
        # print()
        pixels_color_matrix.append(pixels_color_array)

    return pixels_color_matrix


def get_pixel_color(x, y):
    # canvas use different coordinates than turtle
    # y = -y
    # find IDs of all objects in rectangle (x, y, x, y)
    ids = canvas.find_overlapping(x, y, x, y)
    # if found objects
    if ids:
        # get ID of last object (top most)
        index = ids[-1]
        # get its color
        color = canvas.itemcget(index, "fill")
        # if it has color then return it
        if color:
            return color
    # if there was no object then return "white" - background color in turtle
    return "white"  # default color


def get_segment(pixels_color_matrix, row, col):
    black_pixels = 0
    for i in range(segment_height):
        for j in range(segment_width):
            color = pixels_color_matrix[i + row * segment_height][j + col * segment_width]
            if color == 1:
                black_pixels += 1

    return black_pixels


def average_vectors():
    amount_of_each_digit = []
    vectors = []

    for i in range(0, 10):
        amount_of_each_digit.append(0)
        sum_vector = []

        for key, vector in vectors_from_file.items():
            if int(vector[1]) != int(i):
                continue

            amount_of_each_digit[i] += 1
            k = 0

            for elem in vector[0]:
                try:
                    sum_vector[k] += float(elem)
                    k += 1
                except IndexError:
                    sum_vector.append(0)
                    sum_vector[k] = float(elem)
                    k += 1

        vectors.append(sum_vector)

    for i in range(0, 10):
        if amount_of_each_digit[i] == 0:
            continue

        for j in range(len(vectors[i])):
            vectors[i][j] /= amount_of_each_digit[i]
        i += 1

    new_vectors = {}
    for i in range(0, 10):
        if amount_of_each_digit[i] == 0:
            continue
        new_vectors[i] = [vectors[i], i]

    return new_vectors


def search_digit():
    read_vector_canvas()

    # print(vectors_from_file)
    new_vectors = average_vectors()
    print(new_vectors)
    # get distance
    # search suitable
    # distance - digit
    dist = {}
    minimum = 1000

    # you can change new_vectors to vectors_from_file
    for key, vector in new_vectors.items():
        dist_elem = 0

        for i in range(len(vector[0])):
            d = math.pow(float(vector[0].__getitem__(i)) - vector_normalized.__getitem__(i), 2)
            dist_elem += d

        if dist_elem < minimum:
            minimum = dist_elem

        dist[dist_elem] = float(vector[1])

    # print(dist)
    print("Answer: ", dist.get(minimum))
    answer = "Answer: " + str(int(dist.get(minimum)))
    answer_lbl.config(text=answer)


def clear_canvas():
    canvas.delete('all')


lasx, lasy = 0, 0
canvas_width, canvas_height = 120, 210
segment_width, segment_height = 30, 30
vector_normalized = []
# digit - vector
vectors_from_file = {}
read_vectors_file()

app = Tk()
app.configure(bg='grey')
app.geometry("400x400")

canvas = Canvas(app, bg='white', height=canvas_height, width=canvas_width)
canvas.place(x=(400 - canvas_width) / 2, y=(400 - canvas_height) / 2)
canvas.bind("<Button-1>", get_x_and_y)
canvas.bind("<B1-Motion>", draw_smth)

# btn = Button(text="write", command=read_vector_canvas)
# btn.place(x=10, y=330)

write_btn = Button(text='write', command=write_vector_file)
write_btn.place(x=80, y=330)

text = Text(height=1, width=4)
text.place(x=120, y=330)

clear_btn = Button(text="clear", command=clear_canvas)
clear_btn.place(x=160, y=330)

search_digit_btn = Button(text="search", command=search_digit)
search_digit_btn.place(x=200, y=330)

answer_lbl = Label(text="Answer: ")
answer_lbl.place(x=250, y=330)

app.mainloop()
# Знаходити середній вектор по кожній цифрі (групі)
