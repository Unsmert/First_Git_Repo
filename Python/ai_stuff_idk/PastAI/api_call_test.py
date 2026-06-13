from google import genai

client = genai.Client(api_key= "AIzaSyDrQ99Qq8dc9PaTY7ACXBZmUjZ6s_qoYa0")

address = "Richmond, VA 23220"
response = client.models.generate_content(
    model="gemini-2.5-flash", contents=f"""Currently, there is a boil water advisory at {address}. For the 
    Eastern Henrico Government Center at Virginia 23223, 
    the Walmart Supercenter at 11400 W Broad St, Glen Allen, VA 23060, 
    and the Target at 11290 W Broad St, Glen Allen, VA 23060, 
    use information from the web, such as traffic, time, and news to predict the probability that each location will be able to provide water in the case of a boil water advisory. 
    Return the results as a json file in with the keys EHGC, walmart, and target conaining a single float value from 0 to 1 representing the probability that each location will be able to provide water. 
    There should be nothing else in the response other than the json file.""",
)

print(response.text)

while True:
    message = input()
    if message.lower() in ["exit", "quit"]:
        break
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=message,
    )

    print(response.text)


