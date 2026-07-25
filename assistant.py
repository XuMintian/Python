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

def show_menu():
    print("\n===== BMI Assistant =====\n")
    print("1. Add BMI record")
    print("2. Show all records")
    print("3. Show summary")
    print("4. Save and quit\n")

# ===========================================================
# ===========================================================

people=load_records()

while True:
    show_menu()

    try:
        choice = int(input("Choose an option: "))
        if choice == 1:

            answer = "y"

            while answer.strip().lower() in ["y", "yes"]:

                height = get_number("\nEnter your height (cm) :", 50, 250)

                weight = get_number("\nEnter your weight (kg) :", 10, 300)

                bmi = calculate_bmi(height, weight)

                print("\nYour BMI is :", round(bmi,2))

                result = get_bmi_category(bmi)

                print(f"\nYou are {result}\n")

                people.append(archive(height, weight, bmi, result))

                answer = input("\nDo you want to calculate another BMI? (y/n) :")

            print("\nRecord saved successfully.\n")

        elif choice == 2:
            if not people:
                print("\nNo records yet\n")
                continue
            for index, person in enumerate(people, start=1):
                    
                    print(
                        index, 
                        f"\nHeight:{person['height']}, \nWeight:{person['weight']}," 
                        f"\nBMI:{round(person['bmi'],2)}, \nCategory:{person['result']}"
                        )

        elif choice == 3:
            if not people:
                print("\nNo records yet\n")
                continue
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
                "\nHighest BMI record:\n"
                f"\nThere are {highest_person_number} matching records:\n"
            )

            for highest_person in highest_people:

                print(
                    "\n=====================================\n"
                    f"\nRecord No. {highest_person['index']}\n"
                    f"\nHeight: {highest_person['person']['height']}\n"
                    f"\nWeight: {highest_person['person']['weight']}\n"
                    f"\nBMI: {round(highest_person['person']['bmi'],2)}\n"
                    f"\nCategory: {highest_person['person']['result']}\n"
                    "\n=====================================\n"
                )

            print("\nAll records:\n")

            for index , person in enumerate(people, start=1):
                print(
                    index, 
                    round(person["bmi"], 2)
                    )
                
            average=sum(person["bmi"] for person in people)/len(people)
            print(f"\nAverage BMI: {round(average, 2)}")

        elif choice == 4:
            save_records(people)
            print("\nRecord saved successfully.\n")
            break
        else:
            print ("\nPlease enter a valid number\n")
    except ValueError:
        print ("\nPlease enter a valid number\n")






   
