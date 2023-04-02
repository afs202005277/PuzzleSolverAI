from time import sleep

import pygame
import analysis
from view import *

'''
This code implements the main game loop for a sliding puzzle game. 
The game can be played either by a human or by a computer using different algorithms, 
including uninformed (BFS, DFS and Iterative Deepening) and informed search algorithms 
(Greedy, A* and Weighted A*).
'''
def main_loop():
    screen = pygame_init()
    last_col = None
    last_row = None
    moving_piece_index = None
    hint_rect = None
    puzzle = analysis.medium_map()
    game_state = 'main_menu'
    first_click = True
    path = None
    algo = None
    informed = None
    heuristic = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if game_state == 'main_menu':
                draw_start_menu(screen)

                keys = pygame.key.get_pressed()
                if keys[pygame.K_c]:
                    game_state = 'choose_diff_computer'
                    game_over = False
                if keys[pygame.K_SPACE]:
                    game_state = 'choose_diff_human'
                    game_over = False

            if game_state == 'choose_diff_human':
                draw_difficulties(screen)

                keys = pygame.key.get_pressed()
                # Change when more levels are implemented
                if keys[pygame.K_1]:
                    game_state = 'playing_human'
                    puzzle = analysis.easy_map()
                elif keys[pygame.K_2]:
                    puzzle = analysis.medium_map()
                    game_state = 'playing_human'
                elif keys[pygame.K_3]:
                    puzzle = analysis.hard_map()
                    game_state = 'playing_human'

            elif game_state == "choose_diff_computer":
                draw_difficulties(screen)

                keys = pygame.key.get_pressed()
                # Change when more levels are implemented
                if keys[pygame.K_1]:
                    game_state = 'choose_algo'
                    puzzle = analysis.easy_map()
                elif keys[pygame.K_2]:
                    puzzle = analysis.medium_map()
                    game_state = 'choose_algo'
                elif keys[pygame.K_3]:
                    puzzle = analysis.hard_map()
                    game_state = 'choose_algo'

            elif game_state == "choose_algo":
                draw_algos(screen)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        game_state = 'playing_computer'
                        informed = False
                        algo = analysis.breadth_first_search
                    elif event.key == pygame.K_2:
                        game_state = 'playing_computer'
                        informed = False
                        algo = analysis.depth_first_search
                    elif event.key == pygame.K_3:
                        game_state = 'playing_computer'
                        informed = False
                        algo = analysis.iterative_deepening_search
                    elif event.key == pygame.K_4:
                        game_state = 'choose_heu'
                        informed = True
                        algo = analysis.greedy_search
                    elif event.key == pygame.K_5:
                        game_state = 'choose_heu'
                        informed = True
                        algo = analysis.a_star_search
                    elif event.key == pygame.K_6:
                        game_state = 'choose_heu'
                        informed = True
                        algo = analysis.weighted_a_star_search

            elif game_state == "choose_heu":
                draw_heuristics(screen)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        game_state = 'playing_computer'
                        heuristic = analysis.h1
                    elif event.key == pygame.K_2:
                        game_state = 'playing_computer'
                        heuristic = analysis.h2
                    elif event.key == pygame.K_3:
                        game_state = 'playing_computer'
                        heuristic = analysis.h3
                    elif event.key == pygame.K_4:
                        game_state = 'playing_computer'
                        heuristic = analysis.h4
                    elif event.key == pygame.K_5:
                        game_state = 'playing_computer'
                        heuristic = analysis.h5
                    elif event.key == pygame.K_6:
                        game_state = 'playing_computer'
                        heuristic = analysis.h6
                    elif event.key == pygame.K_7:
                        game_state = 'playing_computer'
                        heuristic = analysis.h7
                    elif event.key == pygame.K_8:
                        game_state = 'playing_computer'
                        heuristic = analysis.h8
            elif game_state == "playing_computer":
                if not informed:
                    sol = algo(puzzle, analysis.gameOver, analysis.get_child_states)
                else:
                    sol = algo(puzzle, analysis.gameOver, analysis.get_child_states, heuristic)
                path = analysis.get_solution_path(sol[0])
                show_ai_path(path)

                game_state = "main_menu"

            elif game_state == 'playing_human':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        start_pos = pygame.mouse.get_pos()
                        if hint_rect.collidepoint(start_pos):
                            if first_click:
                                sol = analysis.weighted_a_star_search(puzzle, analysis.gameOver, analysis.get_child_states, analysis.h4)
                                path = analysis.get_solution_path(sol[0])
                                analysis.movedPiece(path[0], path[1]).toggle_highlight()
                                first_click = False

                            else:
                                if analysis.gameOver(path[1]):
                                    puzzle.move_piece_delta(puzzle.objectivePiece.id, 0, 3)
                                    game_state = "end_screen"
                                else:
                                    puzzle = path[1]
                                path = None
                                first_click = True

                        last_col = puzzle.getColIndex(start_pos[0])
                        last_row = puzzle.getRowIndex(start_pos[1])
                        tmp = [idx for idx, piece in enumerate(pieces) if is_colliding(piece, start_pos)]
                        if len(tmp) == 1:
                            moving_piece_index = tmp[0]
                            if not first_click:
                                puzzle.getPiece(moving_piece_index).toggle_highlight(True)
                            else:
                                puzzle.getPiece(moving_piece_index).toggle_highlight()
                            path = None
                            first_click = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == pygame.BUTTON_LEFT:
                        if moving_piece_index is None:
                            continue
                        end_pos = pygame.mouse.get_pos()

                        new_col = puzzle.getColIndex(end_pos[0])
                        new_row = puzzle.getRowIndex(end_pos[1])
                        puzzle.move_piece_delta(moving_piece_index, new_col - last_col, new_row - last_row)
                        puzzle.getPiece(moving_piece_index).toggle_highlight()
                        start_pos = None
                        if analysis.gameOver(puzzle):
                            puzzle.move_piece_delta(moving_piece_index, 0, 3)
                            game_state = "end_screen"
                        moving_piece_index = None

                if moving_piece_index is not None:
                    current_pos = pygame.mouse.get_pos()

                    new_col = puzzle.getColIndex(current_pos[0])
                    new_row = puzzle.getRowIndex(current_pos[1])
                    delta_col = new_col - last_col
                    delta_row = new_row - last_row
                    puzzle.move_piece_delta(moving_piece_index, delta_col, delta_row)
                    last_col += delta_col
                    last_row += delta_row

                screen.fill(analysis.BG_COLOR)
                pygame.draw.rect(screen, analysis.GAME_BACKGROUND_COLOR,
                                 pygame.Rect(analysis.GAME_WIDTH_START, analysis.GAME_HEIGHT_START, analysis.GAME_WIDTH_SIZE, analysis.GAME_HEIGHT_SIZE),
                                 border_radius=5)
                pieces = puzzle.drawPieces(screen)
                draw_moves(screen, puzzle.getMoves())
                hint_rect = hint_button(screen)
                pygame.display.flip()
                pygame.display.update()
            elif game_state == 'end_screen':
                draw_end_screen(screen, puzzle)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_m]:
                    game_state = 'main_menu'
                    last_col = None
                    last_row = None
                    moving_piece_index = None
                    puzzle = analysis.easy_map()
                    game_over = False

if __name__ == '__main__':
    main_loop()