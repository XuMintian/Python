import json

def save_records(records):
    with open ("bmi_records.json", "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)

def load_records():
    try:
        with open ("bmi_records.json","r",encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
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