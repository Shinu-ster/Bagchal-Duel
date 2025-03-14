from menu.start_menu import main_menu, game_mode_menu, choose_side

def main():
    choice = main_menu()
    
    if choice == "play":
        mode = game_mode_menu()
        side = choose_side()
        print(f"Starting game: Mode={mode}, Side={side}")
        # Call your game logic here based on mode and side
    
    elif choice == "rules":
        print("Displaying Rules...")
        # Implement your rules screen here

if __name__ == "__main__":
    main()
