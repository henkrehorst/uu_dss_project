from dotenv import load_dotenv

if "__main__" == __name__:
    print("Start data loading...")
    # Load env variables
    load_dotenv('.env')

    print("Data loading finished!")
