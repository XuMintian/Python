import json

DATA_FILE="bmi_records_test.json"

def save_records(records):
    with open (DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)

def load_records():
    try:
        with open (DATA_FILE,"r",encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def get_number(prompt, minimum, maximum):
    while True:

        try:
            number = float(input(prompt))

            if number > 0:
                if minimum <= number <= maximum:
                    return number
                else:
                    print(f"Please enter a number between {minimum} and {maximum}")
            else:
                print("Please enter a positive number.")

        except ValueError:
            print("That is not a valid number. Please enter a number.")
    
def get_bmi_category(bmi):
    if bmi < 18.5:
        return "underweight"
    elif bmi < 24:
        return "normal weight"
    elif bmi < 28:
        return "overweight"
    else:
        return "obese"

def calculate_bmi(height, weight):

    height_m = height / 100
    bmi = weight / (height_m * height_m) 
    return bmi

def archive(height, weight, bmi, result):

    person={
        "height":height,
        "weight":weight,
        "bmi":bmi,
        "result":result
    }

    return person


people=load_records()

answer = "y"

while answer.strip().lower() in ["y", "yes"]:

    height = get_number("Enter your height (cm) :", 50, 250)

    weight = get_number("Enter your weight (kg) :", 10, 300)

    bmi = calculate_bmi(height, weight)

    print("Your BMI is :", round(bmi,2))

    result = get_bmi_category(bmi)

    print(f"You are {result}")

    people.append(archive(height, weight, bmi, result))

    answer = input("Do you want to calculate another BMI? (y/n) :")

average=sum(person["bmi"] for person in people)/len(people)

bmi_values = []

for person in people:
    bmi_values.append(person["bmi"])

highest_bmi = max(bmi_values)

highest_people=[]

for index, person in enumerate(people, start=1):
    if person["bmi"] == highest_bmi:
        
        highest_people.append({
            "index": index,
            "person": person
        })

highest_person_number = len(highest_people)

print(
    "Highest BMI record:\n"
    f"There are {highest_person_number} matching records:\n"
)

for highest_person in highest_people:

    print(
        "=====================================\n"
        f"Record No. {highest_person['index']}\n"
        f"Height: {highest_person['person']['height']}\n"
        f"Weight: {highest_person['person']['weight']}\n"
        f"BMI: {round(highest_person['person']['bmi'],2)}\n"
        f"Category: {highest_person['person']['result']}\n"
        "=====================================\n"
    )


for index , person in enumerate(people, start=1):
    print(
        index, 
        round(person["bmi"], 2)
        )

print(f"Average BMI: {round(average, 2)}")

key=input("Do you want to print personal information? (y/n):")

if key.strip().lower() in ["y", "yes"]:

    for index, person in enumerate(people, start=1):
        print(
            index, 
            f"Height:{person['height']}, Weight:{person['weight']}," 
            f"BMI:{round(person['bmi'],2)}, Category:{person['result']}"
            )
        
save_records(people)
print("Record saved successfully.")