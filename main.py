from src.query import query_database, natural_language_to_sql

def main():
    print("Welcome to Super Stat Melee!")
    print("Data provided by Liquipedia (https://liquipedia.net)")
    print("This application uses content from Liquipedia, licensed under CC-BY-SA 3.0.")
    print("Type 'quit' to exit.")

    while True:
        user_input = input("\nEnter your query: ")

        if user_input.lower() == 'quit':
            print("Thank you for using Super Stat Melee. Goodbye!")
            break

        try:
            sql_query = natural_language_to_sql(user_input)

            if sql_query:
                results = query_database(sql_query)  
                if results:
                    for result in results:
                        if len(result) == 2:  
                            print(f"{result[0]}: {result[1]}")
                        else:
                            print(result)
                else:
                    print("No results found for your query.")
            else:
                print("I'm sorry, I couldn't understand that query. Could you rephrase it?")

        except Exception as e:
            print(f"An error occurred while processing your query: {e}")
            print("Please try again with a different query.")

if __name__ == "__main__":
    main()