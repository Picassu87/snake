import random
import time
import math
from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
from PIL import Image

WIDTH = 40  # size of the arena
HEIGHT = 40  # should be divisible by 4
GRID_SIZE = 14  # should be even
SCALING_FACTOR = 0.65  # for the score displays
SPEED = 0.025
ANIMATION_SPEED = 5
FONT = "Courier"
SNAKE_COLORS = ("lime", "red", "yellow", "blue")
STARTING_DIRECTIONS = ("down", "up", "left", "right")
STARTING_POSITIONS = ((WIDTH/4*GRID_SIZE, HEIGHT/4*GRID_SIZE),
                      (-WIDTH/4*GRID_SIZE, -HEIGHT/4*GRID_SIZE),
                      (WIDTH/4*GRID_SIZE, -HEIGHT/4*GRID_SIZE),
                      (-WIDTH/4*GRID_SIZE, HEIGHT/4*GRID_SIZE))
MAX_SPEED = 1
MIN_SPEED = 7
KEYS = (
    ("Right", "Up", "Left", "Down"),  # Player 1
    ("d", "w", "a", "s"),  # Player 2
    ("0", "o", "l", "p"),  # Player 3
    ("j", "y", "g", "h")  # Player 4
)
VALUE_FOODS = [  # Middle values should divide the highest value
    {"size": GRID_SIZE/2, "shape": "circle", "color": "pink", "effect": "", "value": 1},
    {"size": GRID_SIZE/2, "shape": "circle", "color": "orange", "effect": "", "value": 2},
    {"size": GRID_SIZE, "shape": "circle", "color": "pink", "effect": "", "value": 5},
    {"size": GRID_SIZE, "shape": "circle", "color": "orange", "effect": "", "value": 10},
    {"size": 2*GRID_SIZE, "shape": "triangle", "color": "gold", "effect": "triforce", "value": 30},
]
EFFECT_FOODS = [
    {"size": GRID_SIZE, "shape": "turtle", "color": "green", "effect": "range up", "value": "Range Up",
     "copies": 5, "timer": 10},
    {"size": GRID_SIZE, "shape": "turtle", "color": "random", "effect": "speed up", "value": "Speed Up",
     "copies": 5, "timer": 6},
    {"size": GRID_SIZE, "shape": "circle", "color": "purple", "effect": "poison", "value": "Poison",
     "copies": 2, "timer": 0},
]

screen = Screen()
screen.setup(WIDTH*GRID_SIZE+100, HEIGHT*GRID_SIZE+300)
screen.bgcolor("black")
screen.title("The Snake Game")
screen.tracer(0)

def format_score(score):
    score_list = []
    if len(str(score)) < 3:
        for _ in range(3-len(str(score))):
            score_list.append(" ")
        for digit in str(score):
            score_list.append(digit)
        return "".join(score_list)
    else:
        return str(score)

num_of_players = int(screen.numinput("How many players?", "Choose between 1 and 4: ", 1, 1, 4))
snakes = []
for i in range(num_of_players):
    name = screen.textinput(f"Player {i+1}", "Choose name: ")
    # speed = screen.numinput(f"Player {i+1}: Select speed between {MAX_SPEED}-{MIN_SPEED}",
    #                         f"{MAX_SPEED} = fastest, {MIN_SPEED} = slowest", 1, MAX_SPEED, MIN_SPEED)
    snake = Snake(size=3, width=GRID_SIZE, color=SNAKE_COLORS[i], shape="square", starting_pos=STARTING_POSITIONS[i],
                  starting_dir=STARTING_DIRECTIONS[i], max_speed=MAX_SPEED, min_speed=MIN_SPEED, name=name, number=i+1)
    snake.scoreboard.show_text(
        f"{snake.name}: {format_score(snake.scoreboard.score)}", "center", FONT,
        round(1.5*GRID_SIZE/num_of_players**(1/4)),
        ((2*(i + 1) / (num_of_players + 1) - 1) * GRID_SIZE * WIDTH * SCALING_FACTOR, (HEIGHT+3) * GRID_SIZE/2)
    )
    snakes.append(snake)

high_scores = []
if num_of_players == 1:
    snakes[0].scoreboard.clear()
    snakes[0].scoreboard.show_text(f"{snakes[0].name}:  0", "center", FONT, GRID_SIZE,
                                   (-GRID_SIZE * WIDTH / 4, (HEIGHT+3) * GRID_SIZE/2))
    high_scoreboard = Scoreboard("gold")
    with open("data.txt") as data:
        high_score_data = list(data)
    for line in high_score_data:
        split_line = line.split(',')
        split_line[1] = split_line[1].rstrip('\n')
        high_scores.append(split_line)
    high_scoreboard.show_text(
        f"High score: {high_scores[0][0]} ({high_scores[0][1]})", "center",
        FONT, GRID_SIZE, (GRID_SIZE * WIDTH / 4, (HEIGHT+3) * GRID_SIZE/2)
    )

# Create food legend and list of all foods
food_list = []
legend_foods = []
triforces = [
    [],
    [],
    []
]
for i in range(len(VALUE_FOODS)):
    legend_food = Food(VALUE_FOODS[i]["size"], VALUE_FOODS[i]["shape"], VALUE_FOODS[i]["color"],
                       VALUE_FOODS[i]["effect"], VALUE_FOODS[i]["value"], 0)
    legend_food.setpos(((2*(i + 1) / (len(VALUE_FOODS) + 1) - 1) * GRID_SIZE * WIDTH * SCALING_FACTOR
                        - (22+legend_food.size/2), -HEIGHT * GRID_SIZE/2 - 40))
    if legend_food.effect == "triforce" and num_of_players > 1:
        for j in range(num_of_players):
            triforce1 = legend_food.clone()
            triforce1.setpos(((2*(j + 1) / (num_of_players + 1) - 1) * GRID_SIZE * WIDTH * SCALING_FACTOR-GRID_SIZE,
                                 (HEIGHT+7) * GRID_SIZE/2))
            triforces[0].append(triforce1)
            triforce2 = legend_food.clone()
            triforce2.setpos(
                ((2 * (j + 1) / (num_of_players + 1) - 1) * GRID_SIZE * WIDTH * SCALING_FACTOR + GRID_SIZE,
                 (HEIGHT + 7) * GRID_SIZE / 2))
            triforces[1].append(triforce2)
            triforce3 = legend_food.clone()
            triforce3.setpos(
                ((2 * (j + 1) / (num_of_players + 1) - 1) * GRID_SIZE * WIDTH * SCALING_FACTOR,
                 (HEIGHT + 10.5) * GRID_SIZE / 2))
            triforces[2].append(triforce3)
    legend_food.st()
    legend_foods.append(legend_food)
    legend_value = Scoreboard("white")
    legend_value.show_text(f"= {VALUE_FOODS[i]['value']}", "left", FONT, GRID_SIZE*3//2,
                           ((2*(i + 1) / (len(VALUE_FOODS) + 1) - 1) * GRID_SIZE * WIDTH * SCALING_FACTOR - 7,
                            -HEIGHT * GRID_SIZE/2 - 53))
for i in range(len(EFFECT_FOODS)):
    legend_food = Food(EFFECT_FOODS[i]["size"], EFFECT_FOODS[i]["shape"], EFFECT_FOODS[i]["color"],
                       EFFECT_FOODS[i]["effect"], EFFECT_FOODS[i]["value"], EFFECT_FOODS[i]["timer"])
    legend_food.setpos(((2*(i + 1) / (len(EFFECT_FOODS) + 1) - 1) * GRID_SIZE * WIDTH * SCALING_FACTOR*1.2
                        - (42+legend_food.size/2), -HEIGHT * GRID_SIZE/2 - 80))
    legend_food.st()
    legend_foods.append(legend_food)
    legend_value = Scoreboard("white")
    legend_value.show_text(f"= {EFFECT_FOODS[i]['value']}", "left", FONT, GRID_SIZE*3//2,
                           ((2*(i + 1) / (len(EFFECT_FOODS) + 1) - 1) * GRID_SIZE * WIDTH * SCALING_FACTOR*1.2 - 32,
                            -HEIGHT * GRID_SIZE/2 - 91))
for food in VALUE_FOODS:
    for _ in range(VALUE_FOODS[-1]["value"]//food["value"]):
        food_list.append(Food(food["size"], food["shape"], food["color"], food["effect"], food["value"], 0))
for food in EFFECT_FOODS:
    for _ in range(food["copies"]):
        food_list.append(Food(food["size"], food["shape"], food["color"], food["effect"], food["value"], food["timer"]))

def change_food_location(moving_food, current_snakes):
    food_on_snake = True
    location = (0, 0)
    while food_on_snake:
        location = (random.randint(-WIDTH*GRID_SIZE//2 + 2*round(moving_food.size),
                                   WIDTH*GRID_SIZE//2 - 2*round(moving_food.size)),
                    random.randint(-HEIGHT*GRID_SIZE//2 + 2*round(moving_food.size),
                                   HEIGHT*GRID_SIZE//2 - 2*round(moving_food.size)))
        food_on_snake = False
        for cs in current_snakes:
            for seg in cs.body:
                if seg.distance(location) <= moving_food.size/2 + snake.width/math.sqrt(2):
                    food_on_snake = True
                    break
    moving_food.setpos(location)

def spawn_random_food():
    no_hidden_foods = True
    for F in food_list:
        if not F.isvisible():
            no_hidden_foods = False
    if not no_hidden_foods:
        random_food = random.choice(food_list)
        while random_food.isvisible():
            random_food = random.choice(food_list)
        food_list[food_list.index(random_food)].st()
        change_food_location(food_list[food_list.index(random_food)], snakes)

images = []
for i in range(36):
    with Image.open(f"./bg_images/frame_{i}.gif") as image:
        image = image.resize((WIDTH*GRID_SIZE, HEIGHT*GRID_SIZE))
        image.save(f"./resized_images/rs_frame_{i}.gif", "gif")
    images.append(f"./resized_images/rs_frame_{i}.gif")
    screen.addshape(images[i])
countdown = Scoreboard("white")
countdown.shape(images[0])
countdown.st()
Scoreboard("white").draw_arena((WIDTH*GRID_SIZE, HEIGHT*GRID_SIZE), GRID_SIZE)
screen.update()
for i in range(3):
    countdown.show_text(f"{3-i}", "center", FONT, GRID_SIZE*2, (0, 0))
    time.sleep(30 * SPEED)
    countdown.clear()
game_over = False
all_dead = False
turn_count = 0
timer = Scoreboard("red")
timer.show_text(f"{timer.score}", "center", FONT, GRID_SIZE, (1, HEIGHT*GRID_SIZE/2))
while not game_over and not all_dead:
    for image in images:
        if turn_count % ANIMATION_SPEED == 0 and turn_count/ANIMATION_SPEED % 36 == images.index(image):
            countdown.shape(image)
    if turn_count % 500 == 0:
        spawn_random_food()
    turn_count += 1
    screen.update()
    time.sleep(SPEED)
    frequency = round(1/SPEED)
    if turn_count % frequency == 0:
        timer.score += 1
        timer.update(f"{timer.score}")
    for snake in snakes:
        if snake.range_timer > 0:
            snake.range_timer -= 1
            if snake.range_timer == 0:
                snake.range = snake.width/2
                print(f"{snake.name} range back to normal")
        if snake.speed_timer > 0:
            snake.speed_timer -= 1
            if snake.speed_timer == 0:
                snake.speed = (snake.max_speed+snake.min_speed)//2
                print(f"{snake.name} speed back to normal")
        if turn_count % snake.speed == 0 and not snake.dead:
            commands = [snake.turn_right, snake.turn_up, snake.turn_left, snake.turn_down]
            screen.listen()
            for i in range(4):
                screen.onkeypress(commands[i], KEYS[snakes.index(snake)][i])
            snake.move()
            snake.has_turned = False
            for s in snakes:
                for segment in s.body:
                    if math.fabs(snake.body[0].xcor() - segment.xcor()) < snake.width/2 + s.width/2-1\
                            and math.fabs(snake.body[0].ycor() - segment.ycor()) < snake.width/2 + s.width/2-1:
                        if segment == snake.body[0]:
                            continue
                        snake.dead = True
                        snake.undo_move()
                        if num_of_players > 1:
                            if s == snake:
                                print(f"{snake.name} hit themselves.")
                            else:
                                print(f"{snake.name} hit Player {s.name}.")
                        else:
                            print("You hit yourself.")
            if not (-WIDTH*GRID_SIZE/2+snake.width/2 < round(snake.body[0].xcor())
                    < WIDTH*GRID_SIZE/2-snake.width/2) \
                    or not (-HEIGHT*GRID_SIZE/2+snake.width/2 < round(snake.body[0].ycor())
                            < HEIGHT*GRID_SIZE/2-snake.width/2):
                snake.dead = True
                snake.undo_move()
                if num_of_players > 1:
                    print(f"{snake.name} hit a wall.")
                else:
                    print("You hit a wall.")
            for food in food_list + legend_foods:
                if food.has_random_color:
                    food.color(random.random(), random.random(), random.random())
            for food in food_list:
                if food.isvisible():
                    if snake.body[0].distance(food) < snake.range + food.size/2:
                        if not isinstance(food.value, int):
                            if food.effect == "poison":
                                snake.dead = True
                                food.ht()
                                if num_of_players > 1:
                                    print(f"{snake.name} ate poison.")
                                else:
                                    print("You ate poison.")
                                screen.update()
                            elif food.effect == "range up":
                                snake.range = snake.width*2
                                snake.range_timer = round(food.timer/SPEED)
                                print(f"{snake.name} range up")
                            elif food.effect == "speed up":
                                if snake.speed == snake.max_speed+1:
                                    snake.speed -= 1
                                    snake.speed_timer = round(food.timer/SPEED)
                                    print(f"{snake.name} speed up by one stage")
                                elif snake.speed > snake.max_speed:
                                    snake.speed -= 2
                                    snake.speed_timer = round(food.timer/SPEED)
                                    print(f"{snake.name} speed up by two stages")
                        else:
                            snake.scoreboard.score += food.value
                            snake.scoreboard.update(f"{snake.name}:{format_score(snake.scoreboard.score)}")
                            if food.effect == "triforce" and num_of_players > 1:
                                snake.triforce += 1
                                for i in range(3):
                                    if snake.triforce == i+1:
                                        triforces[i][snakes.index(snake)].st()
                            if food.effect == "speed up" and snake.speed > snake.max_speed:
                                snake.speed -= 1
                                print(f"{snake.name} speed up by one stage")
                            if food.effect == "speed down" and snake.speed > snake.min_speed:
                                snake.speed += 1
                                print(f"{snake.name} speed down by one stage")
                            snake.grow()
                        food.ht()
                        is_leading = True
                        for s in snakes:
                            if snake.scoreboard.score < s.scoreboard.score:
                                is_leading = False
                        if snake.triforce >= 3 and is_leading:
                            game_over = True
                            screen.update()
                            Scoreboard("white").show_text(f"{snake.name} wins", "center", FONT, GRID_SIZE * 2, (0, 0))
                            print(f"{snake.name} wins.")
                        spawn_random_food()
    all_dead = True
    for snake in snakes:
        if not snake.dead:
            all_dead = False
            break

if all_dead:
    if num_of_players > 1:
        high_score = 0
        for snake in snakes:
            if snake.scoreboard.score >= high_score:
                high_score = snake.scoreboard.score
        winners = []
        for snake in snakes:
            if snake.scoreboard.score == high_score:
                winners.append(snake.name)
        print(f"Game over. Final scores:\n")
        for snake in snakes:
            print(f"{snake.name}: {snake.scoreboard.score}")
        if len(winners) > 1:
            for i in range(len(winners)):
                Scoreboard("white").show_text(f"{winners[i]}", "center", FONT, GRID_SIZE*2,
                                              (0, GRID_SIZE*(len(winners)-2*i)))
            Scoreboard("white").show_text("tie for win", "center", FONT, GRID_SIZE*2, (0, -GRID_SIZE*len(winners)))
            print(f"\n{', '.join(winners)} tie for win.")
        else:
            Scoreboard("white").show_text(f"{winners[0]} wins", "center", FONT, GRID_SIZE*2, (0, 0))
            print(f"\nPlayer {winners[0]} wins.")
    else:
        game_over_text = Scoreboard("white")
        bad_score = True
        ranking = 0
        for i in range(len(high_scores)):
            if snakes[0].scoreboard.score > int(high_scores[i][0]):
                bad_score = False
                ranking = i
                high_scores.insert(i, [snakes[0].scoreboard.score, snakes[0].name])
                if i == 0:
                    game_over_text.show_text("HIGH SCORE", "center", FONT, GRID_SIZE * 3, (0, 0))
                    print(f"Game over. Your final score is {snakes[0].scoreboard.score}. High score!")
                else:
                    game_over_text.show_text("GAME OVER", "center", FONT, GRID_SIZE * 3, (0, 0))
                    print(f"Game over. Your final score is {snakes[0].scoreboard.score}.")
                break
        if bad_score:
            high_scores.append([snakes[0].scoreboard.score, snakes[0].name])
            ranking = len(high_scores)
            game_over_text.show_text("GAME OVER", "center", FONT, GRID_SIZE * 3, (0, 0))
            print(f"Game over. Your final score is {snakes[0].scoreboard.score}.")
        if len(high_scores) > 100:
            high_scores.pop()
        time.sleep(2)
        game_over_text.clear()
        game_over_text.show_text("HIGH SCORES:", "center", FONT, GRID_SIZE * 3, (0, GRID_SIZE * 9))
        for i in range(10):
            if i == ranking:
                Scoreboard(snakes[0].color).show_text(f"{high_scores[i][1]}: {high_scores[i][0]}", "center", FONT,
                                                        GRID_SIZE * 2, (0, GRID_SIZE * 2 * (3.5 - i)))
            else:
                try:
                    Scoreboard("white").show_text(f"{high_scores[i][1]}: {high_scores[i][0]}", "center", FONT,
                                                  GRID_SIZE * 2, (0, GRID_SIZE * 2 * (3.5 - i)))
                except IndexError:
                    pass
        with open("data.txt", "w") as data:
            data.write(f"{high_scores[0][0]},{high_scores[0][1]}\n")
        with open("data.txt", "a") as data:
            for i in range(1, len(high_scores)):
                data.write(f"{high_scores[i][0]},{high_scores[i][1]}\n")


screen.exitonclick()
