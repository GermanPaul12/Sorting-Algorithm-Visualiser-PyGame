import pygame
import random
import math
import time 
pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('comicsans', 30)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)
        self.time_taken = 0

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))

    sorting_line1 = "I - Insertion Sort | B - Bubble Sort | M - Merge Sort"
    sorting_line2 = "Q - Quick Sort | T - Tim Sort"  # Split into two lines
    sorting = draw_info.FONT.render(sorting_line1, 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 75))
    
    sorting_line2_render = draw_info.FONT.render(sorting_line2, 1, draw_info.BLACK)  # Render the second line
    draw_info.window.blit(sorting_line2_render, (draw_info.width/2 - sorting_line2_render.get_width()/2 , 110))  # Adjust Y position
    
    time_display = draw_info.FONT.render(f"Time: {draw_info.time_taken:.6f} seconds", 1, draw_info.BLACK)
    draw_info.window.blit(time_display, (draw_info.width/2 - time_display.get_width()/2 , 140))  # Adjust Y position

    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
                        draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i] 

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst


def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst
    start_time = pygame.time.get_ticks()

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield
        draw_info.time_taken = (pygame.time.get_ticks() - start_time) / 1000.0
        yield

    return lst

def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst
    start_time = pygame.time.get_ticks()

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield
        draw_info.time_taken = (pygame.time.get_ticks() - start_time) / 1000.0
        yield

    return lst

def merge_sort(draw_info, ascending=True):
    def merge(arr, left, mid, right):
        temp = []
        i, j = left, mid + 1

        while i <= mid and j <= right:
            if (arr[i] <= arr[j] and ascending) or (arr[i] >= arr[j] and not ascending):
                temp.append(arr[i])
                i += 1
            else:
                temp.append(arr[j])
                j += 1

        while i <= mid:
            temp.append(arr[i])
            i += 1
        while j <= right:
            temp.append(arr[j])
            j += 1

        for idx, val in enumerate(temp):
            arr[left + idx] = val
            draw_list(draw_info, {left + idx: draw_info.GREEN}, True)
        
        yield

    def merge_sort_recursive(arr, left, right):
        if left < right:
            mid = (left + right) // 2
            yield from merge_sort_recursive(arr, left, mid)
            yield from merge_sort_recursive(arr, mid + 1, right)
            yield from merge(arr, left, mid, right)

    lst = draw_info.lst
    start_time = pygame.time.get_ticks()

    yield from merge_sort_recursive(lst, 0, len(lst) - 1)

    draw_info.time_taken = (pygame.time.get_ticks() - start_time) / 1000.0

    return lst

def quick_sort(draw_info, ascending=True):
    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            if (arr[j] <= pivot and ascending) or (arr[j] >= pivot and not ascending):
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        draw_list(draw_info, {i + 1: draw_info.GREEN, high: draw_info.RED}, True)
        yield

        return i + 1

    def quick_sort_recursive(arr, low, high):
        if low < high:
            pi = yield from partition(arr, low, high)
            yield from quick_sort_recursive(arr, low, pi - 1)
            yield from quick_sort_recursive(arr, pi + 1, high)

    lst = draw_info.lst
    start_time = pygame.time.get_ticks()

    yield from quick_sort_recursive(lst, 0, len(lst) - 1)

    draw_info.time_taken = (pygame.time.get_ticks() - start_time) / 1000.0

    return lst

def tim_sort(draw_info, ascending=True):
    def insertion_sort(arr, left=0, right=None):
        if right is None:
            right = len(arr) - 1
        
        for i in range(left + 1, right + 1):
            key_item = arr[i]
            j = i - 1

            while j >= left and (arr[j] > key_item if ascending else arr[j] < key_item):
                arr[j + 1] = arr[j]
                j -= 1
                draw_list(draw_info, {j + 1: draw_info.GREEN, j + 2: draw_info.RED}, True)
                yield
            arr[j + 1] = key_item
            draw_list(draw_info, {j + 1: draw_info.GREEN}, True)
            yield
    
    def merge(arr, left, mid, right):
        len1, len2 = mid - left + 1, right - mid
        left_arr, right_arr = arr[left:mid + 1], arr[mid + 1:right + 1]

        i, j, k = 0, 0, left

        while i < len1 and j < len2:
            if (left_arr[i] <= right_arr[j] and ascending) or (left_arr[i] >= right_arr[j] and not ascending):
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1
            draw_list(draw_info, {k - 1: draw_info.GREEN}, True)
            yield

        while i < len1:
            arr[k] = left_arr[i]
            i += 1
            k += 1
            draw_list(draw_info, {k - 1: draw_info.GREEN}, True)
            yield

        while j < len2:
            arr[k] = right_arr[j]
            j += 1
            k += 1
            draw_list(draw_info, {k - 1: draw_info.GREEN}, True)
            yield
    
    lst = draw_info.lst
    start_time = pygame.time.get_ticks()
    
    min_run = 32
    n = len(lst)
    
    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        yield from insertion_sort(lst, start, end)
    
    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min(n - 1, mid + size)
            yield from merge(lst, left, mid, right)
        size *= 2
    
    draw_info.time_taken = (pygame.time.get_ticks() - start_time) / 1000.0

    return lst


def main():
    run = True
    clock = pygame.time.Clock()
    speed = 1  # Adjust the speed value to control animation speed
    
    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(1000, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithms = {
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort,
        "Tim Sort": tim_sort,  # Add TimSort here
        # Add more sorting algorithms here
    }
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    start_time = 0
    last_frame_time = time.time()

    while run:
        clock.tick(10)

        if sorting:
            if start_time == 0:
                start_time = time.time()

            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
                start_time = 0
        else:
            current_time = time.time()
            if current_time - last_frame_time >= 1 / speed:
                last_frame_time = current_time
                draw(draw_info, sorting_algo_name, ascending)
                pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithms[sorting_algo_name](draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_m and not sorting:
                sorting_algo_name = "Merge Sort"
            elif event.key == pygame.K_q and not sorting:
                sorting_algo_name = "Quick Sort"
            elif event.key == pygame.K_t and not sorting:
                sorting_algo_name = "Tim Sort"  # Add this line for TimSort
            # Add more keys for other sorting algorithms

    pygame.quit()

if __name__ == "__main__":
    main()




