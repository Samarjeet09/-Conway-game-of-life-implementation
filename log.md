# conway game of life implementation challenge
ok so this file is going to be like a log book of how i am attempting the problem so i can look back 
---
## 1. Lets first understand the conways game of life

- we follow these basic rules for each cell
1. Any live cell with <b> fewer than two live neighbors dies</b>, as if by underpopulation.
2. Any live cell with <b>two or three live neighbors lives on</b> to the next generation.
3. Any live cell with <b>more than three live neighbors dies</b>, as if by overpopulation.
4. Any dead cell with <b>exactly three live neighbors becomes a live cell</b>, as if by reproduction.

[reference_video](https://www.youtube.com/watch?v=ouipbDkwHWA)

## 2. ok first lets make a window and make cells 
so i want to have a basic window with a grid pattern which later i will call each box of grid my cell
 - so we were able to make a grid using for loops and rect objects in pygame
 - also if we store them in a dict , we have ids of each rect 

## 3. Next lets detect mouse clicks and colour these rects /cells

 

